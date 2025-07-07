import requests
import tempfile
import os
import zipfile
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET

from qgis.PyQt.QtGui import QColor
from qgis.core import (
    QgsVectorLayer,
    QgsProject,
    QgsMarkerSymbol,
    QgsRuleBasedRenderer,
    QgsVectorFileWriter
)

FEATURE_SERVICE_URL = (
    "https://services3.arcgis.com/T4QMspbfLg3qTGWY/"
    "arcgis/rest/services/WFIGS_Incident_Locations_Current/FeatureServer/0"
)
OUT_KML_PATH = ".../Current_NIFC_Incidents.kml" # <-- add your path and desired KML name. Use "/" vs "\" in your path 
NAME_FIELD    = "IncidentName"
ICON_DIR      = os.path.join(os.path.dirname(OUT_KML_PATH), "icons")
KMZ_PATH      = OUT_KML_PATH.replace(".kml", ".kmz")

os.makedirs(ICON_DIR, exist_ok=True)

resp = requests.get(
    f"{FEATURE_SERVICE_URL}/query",
    params={
        "where":"1=1",
        "outFields":"*",
        "f":"geojson",
        "returnGeometry":"true"
    }
)
geojson_path = os.path.join(tempfile.gettempdir(), "incident_points.geojson")
with open(geojson_path, "w", encoding="utf-8") as f:
    f.write(resp.text)

info = requests.get(f"{FEATURE_SERVICE_URL}?f=pjson").json()
renderer_json = info["drawingInfo"]["renderer"]

layer = QgsVectorLayer(geojson_path, "Incidents", "ogr")
if not layer.isValid():
    raise Exception("Layer failed to load")

category_styles = {
    c["value"]: QColor(*c["symbol"]["color"][:3])
    for c in renderer_json["uniqueValueInfos"]
}

size_bins = [
    (10000, float("inf"), 16),
    (7000, 9999.9, 12),
    (5000, 6999.9, 8),
    (2000, 4999.9, 6),
    (0, 1999.9, 4),
]

root_rule = QgsRuleBasedRenderer.Rule(None)
for idx, (cat_val, color) in enumerate(category_styles.items()):
    for bin_idx, (min_v, max_v, px) in enumerate(size_bins):
        symbol = QgsMarkerSymbol.createSimple({
            "name": "circle",
            "color": color.name(),
            "outline_color": "#FFFFFF",
            "outline_width": "0.75",
            "size": str(px)
        })
        expr = (
            f"\"IncidentTypeCategory\" = '{cat_val}'"
            f" AND \"IncidentSize\" >= {min_v}"
            f" AND \"IncidentSize\" <= {max_v}"
        )
        label = (
            f"{cat_val} | >{int(min_v):,}"
            if max_v==float("inf")
            else f"{cat_val} | {int(min_v):,}–{int(max_v):,}"
        )
        rule = QgsRuleBasedRenderer.Rule(symbol)
        rule.setFilterExpression(expr)
        rule.setLabel(label)
        root_rule.appendChild(rule)

renderer = QgsRuleBasedRenderer(root_rule)
layer.setRenderer(renderer)
layer.setDisplayExpression(f'"{NAME_FIELD}"')

for l in QgsProject.instance().mapLayersByName("Incidents"):
    QgsProject.instance().removeMapLayer(l)
QgsProject.instance().addMapLayer(layer)

options = QgsVectorFileWriter.SaveVectorOptions()
options.driverName        = "KML"
options.fileEncoding      = "UTF-8"
options.layerOptions      = [f"NameField={NAME_FIELD}"]
options.attributes        = list(range(len(layer.fields())))
options.onlySelectedFeatures = False

err = QgsVectorFileWriter.writeAsVectorFormatV2(
    layer, OUT_KML_PATH,
    QgsProject.instance().transformContext(),
    options
)
if err[0] != QgsVectorFileWriter.NoError:
    raise Exception(f"Export failed: {err}")
print("✅ Exported KML to", OUT_KML_PATH)

style_defs = []
for idx, (cat_val, color) in enumerate(category_styles.items()):
    sym = next(c for c in renderer_json["uniqueValueInfos"] if c["value"]==cat_val)["symbol"]
    fill = sym["color"]  # [R,G,B,A]
    for bin_idx, (_, _, px) in enumerate(size_bins):
        style_id = f"IconStyle{idx*len(size_bins)+bin_idx:02d}"
        scale = px / 4.0  # baseline px=4→scale=1.0
        style_defs.append((style_id, fill, scale, px))

for style_id, fill, _, px in style_defs:
    img = Image.new("RGBA", (int(px)+4, int(px)+4), (0,0,0,0))
    d = ImageDraw.Draw(img)
    d.ellipse((2,2,int(px)+2,int(px)+2), fill=tuple(fill), outline=(255,255,255,200))
    img.save(os.path.join(ICON_DIR, f"{style_id}.png"))

tree = ET.parse(OUT_KML_PATH)
root = tree.getroot()
ns   = {"kml":"http://www.opengis.net/kml/2.2"}
doc  = root.find("kml:Document", ns)

for pm in root.findall(".//kml:Placemark", ns):
    if pm.find("kml:name", ns) is None:
        val = pm.find('.//kml:SimpleData[@name="IncidentName"]', ns)
        if val is not None:
            name_el = ET.Element(f"{{{ns['kml']}}}name")
            name_el.text = val.text
            pm.insert(0, name_el)

for style_id, _, scale, _ in style_defs:
    style_el = ET.Element(f"{{{ns['kml']}}}Style", id=style_id)
    icon_style = ET.SubElement(style_el, f"{{{ns['kml']}}}IconStyle")
    ET.SubElement(icon_style, f"{{{ns['kml']}}}scale").text = str(scale)
    icon = ET.SubElement(icon_style, f"{{{ns['kml']}}}Icon")
    ET.SubElement(icon, f"{{{ns['kml']}}}href").text = f"icons/{style_id}.png"
    doc.insert(0, style_el)

style_lookup = {
    (cat_val, px): f"IconStyle{idx*len(size_bins)+bin_idx:02d}"
    for idx, (cat_val, _) in enumerate(category_styles.items())
    for bin_idx, (_,_,px) in enumerate(size_bins)
}

for pm in root.findall(".//kml:Placemark", ns):
    # 1) Inject <name> if missing
    if pm.find("kml:name", ns) is None:
        val = pm.find('.//kml:SimpleData[@name="IncidentName"]', ns)
        if val is not None and val.text:
            name_el = ET.Element(f"{{{ns['kml']}}}name")
            name_el.text = val.text
            pm.insert(0, name_el)

    cat_el = pm.find('.//kml:SimpleData[@name="IncidentTypeCategory"]', ns)
    if cat_el is None or not cat_el.text:
        continue
    cat_val = cat_el.text

    size_el = pm.find('.//kml:SimpleData[@name="IncidentSize"]', ns)
    try:
        size_val = float(size_el.text) if (size_el is not None and size_el.text) else 0.0
    except ValueError:
        size_val = 0.0

    bucket_px = next(
        px for (min_v, max_v, px) in size_bins
        if min_v <= size_val <= max_v
    )

    style_id = style_lookup.get((cat_val, bucket_px))
    if not style_id:
        continue

    old = pm.find("kml:styleUrl", ns)
    if old is not None:
        pm.remove(old)
    url = ET.Element(f"{{{ns['kml']}}}styleUrl")
    url.text = f"#{style_id}"
    pm.insert(1, url)

    inline = pm.find("kml:Style", ns)
    if inline is not None:
        pm.remove(inline)



tree.write(OUT_KML_PATH, encoding="UTF-8", xml_declaration=True)

with zipfile.ZipFile(KMZ_PATH, "w", zipfile.ZIP_DEFLATED) as kmz:
    kmz.write(OUT_KML_PATH, arcname="doc.kml")
    for fn in os.listdir(ICON_DIR):
        kmz.write(os.path.join(ICON_DIR, fn), arcname=f"icons/{fn}")

print("✅ Packaged KMZ at", KMZ_PATH)
