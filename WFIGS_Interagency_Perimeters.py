import requests
import tempfile
import os
from qgis.PyQt.QtGui import QColor
from qgis.core import (
    QgsVectorLayer,
    QgsProject,
    QgsSymbol,
    QgsRendererCategory,
    QgsCategorizedSymbolRenderer,
    QgsVectorFileWriter
)
import xml.etree.ElementTree as ET

FEATURE_SERVICE_URL = "https://services3.arcgis.com/T4QMspbfLg3qTGWY/ArcGIS/rest/services/WFIGS_Interagency_Perimeters_Current/FeatureServer/0"
OUT_KML_PATH = ".../Current_NIFC_Incidents.kml"
NAME_FIELD = "attr_IncidentName"

query_url = f"{FEATURE_SERVICE_URL}/query"
params = {
    "where": "1=1",
    "outFields": "*",
    "f": "geojson",
    "returnGeometry": "true"
}
response = requests.get(query_url, params=params)
geojson_path = os.path.join(tempfile.gettempdir(), "features.geojson")
with open(geojson_path, "w", encoding="utf-8") as f:
    f.write(response.text)

info_url = f"{FEATURE_SERVICE_URL}?f=pjson"
drawing_info = requests.get(info_url).json()["drawingInfo"]
renderer = drawing_info["renderer"]

layer = QgsVectorLayer(geojson_path, "Perimeters", "ogr")
if not layer.isValid():
    raise Exception("Layer failed to load")

field_name = renderer["field1"]
categories = []

for class_ in renderer["uniqueValueInfos"]:
    value = class_["value"]
    label = class_["label"]
    symbol_data = class_["symbol"]

    fill_color = QColor(*symbol_data["color"][:3])
    outline_color = QColor(*symbol_data["outline"]["color"][:3])
    outline_width = symbol_data["outline"].get("width", 0.5)

    symbol = QgsSymbol.defaultSymbol(layer.geometryType())
    symbol.setColor(fill_color)
    symbol.symbolLayer(0).setFillColor(fill_color)
    symbol.symbolLayer(0).setStrokeColor(outline_color)
    symbol.symbolLayer(0).setStrokeWidth(outline_width)

    category = QgsRendererCategory(value, symbol, label)
    categories.append(category)

categorized_renderer = QgsCategorizedSymbolRenderer(field_name, categories)
layer.setRenderer(categorized_renderer)

layer.setDisplayExpression(f'"{NAME_FIELD}"')

existing_layers = QgsProject.instance().mapLayersByName("Perimeters")
for l in existing_layers:
    QgsProject.instance().removeMapLayer(l)
QgsProject.instance().addMapLayer(layer)

options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName = "KML"
options.fileEncoding = "UTF-8"
options.layerOptions = [f'NameField={NAME_FIELD}']
options.attributes = list(range(len(layer.fields())))
options.onlySelectedFeatures = False

error = QgsVectorFileWriter.writeAsVectorFormatV2(
    layer,
    OUT_KML_PATH,
    QgsProject.instance().transformContext(),
    options
)

if error[0] != QgsVectorFileWriter.NoError:
    raise Exception(f"❌ Export failed: {error}")
else:
    print(f"✅ Exported KML to {OUT_KML_PATH}")

def rgba_to_abgr_kml(color):
    """Convert [R,G,B,A] or 'R,G,B,A' to KML ABGR format hex string."""
    if isinstance(color, str):
        parts = [int(p) for p in color.split(',')]
    else:
        parts = color
    r, g, b, a = parts
    return f"{a:02x}{b:02x}{g:02x}{r:02x}"

tree = ET.parse(OUT_KML_PATH)
root = tree.getroot()
ns = {'kml': 'http://www.opengis.net/kml/2.2'}

document = root.find('kml:Document', ns)
existing_styles = {}

for placemark in root.findall('.//kml:Placemark', ns):
    # === A. Inject <name> from attr_IncidentName
    name_tag = placemark.find('kml:name', ns)
    if name_tag is None:
        incident_name = placemark.find('.//kml:SimpleData[@name="attr_IncidentName"]', ns)
        if incident_name is not None:
            name_el = ET.Element('{http://www.opengis.net/kml/2.2}name')
            name_el.text = incident_name.text
            placemark.insert(0, name_el)

    cat = placemark.find('.//kml:SimpleData[@name="attr_IncidentTypeCategory"]', ns)
    if cat is None:
        continue
    cat_val = cat.text

    style_def = next((c for c in renderer["uniqueValueInfos"] if c["value"] == cat_val), None)
    if not style_def:
        continue

    fill_kml = rgba_to_abgr_kml(style_def["symbol"]["color"])
    outline_kml = rgba_to_abgr_kml(style_def["symbol"]["outline"]["color"])
    style_id = f"style_{cat_val}"

    if style_id not in existing_styles:
        style_el = ET.Element('{http://www.opengis.net/kml/2.2}Style', attrib={'id': style_id})

        line_style = ET.SubElement(style_el, '{http://www.opengis.net/kml/2.2}LineStyle')
        ET.SubElement(line_style, '{http://www.opengis.net/kml/2.2}color').text = outline_kml
        ET.SubElement(line_style, '{http://www.opengis.net/kml/2.2}width').text = "1.5"

        poly_style = ET.SubElement(style_el, '{http://www.opengis.net/kml/2.2}PolyStyle')
        ET.SubElement(poly_style, '{http://www.opengis.net/kml/2.2}color').text = fill_kml
        ET.SubElement(poly_style, '{http://www.opengis.net/kml/2.2}fill').text = "1"
        ET.SubElement(poly_style, '{http://www.opengis.net/kml/2.2}outline').text = "1"

        document.insert(0, style_el)
        existing_styles[style_id] = True

    existing_style_tag = placemark.find('kml:styleUrl', ns)
    if existing_style_tag is not None:
        placemark.remove(existing_style_tag)
    style_url_tag = ET.Element('{http://www.opengis.net/kml/2.2}styleUrl')
    style_url_tag.text = f"#{style_id}"
    placemark.insert(1, style_url_tag)

    inline_style = placemark.find('kml:Style', ns)
    if inline_style is not None:
        placemark.remove(inline_style)

tree.write(OUT_KML_PATH, encoding='UTF-8', xml_declaration=True)
print(f"✅ Patched KML with <name>, shared <Style>, and cleaned up inline styles.")
