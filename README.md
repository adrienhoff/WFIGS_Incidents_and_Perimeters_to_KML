# WFIGS_Incidents_and_Perimeters_to_KML
Writes WFIGS Incidents and Perimeters to KML from ArcGIS Feature Service for use in Google Earth using QGIS python console. Uses ArcGIS styling from the drawingInfo.json. Opens the KML and writes the placemark name and symbology in GE format.  

![image](https://github.com/user-attachments/assets/f1f4b259-830c-4ac3-9e80-d23c9bd18bbd)


# QGIS - ArcGIS FeatureService to KML


1\. With QGIS open, launch the python console from the Plugins Tab.

![](https://colony-recorder.s3.amazonaws.com/files/2025-07-07/933f657a-f0f3-43f4-ac20-c3009e7e5c85/stack_animation.webp)


2\. Open a new file.\
Load the python scripts provided: WFIGS_Incidents.py and WFIGS_Interagency_Perimeters.py

![](https://colony-recorder.s3.amazonaws.com/files/2025-07-07/1d06bdf7-81bd-4140-9573-86e72e7865f2/stack_animation.webp)


3\. Update the outpath to a folder on your system, ensure you include the kml file name as desired. See below for example. Use "/" in place of "\\" in the file path.

![](https://ajeuwbhvhr.cloudimg.io/https://colony-recorder.s3.amazonaws.com/files/2025-07-07/315a3898-1e0e-402b-907d-2f3c81c1c9e9/ascreenshot.jpeg?tl_px=544,430&br_px=1920,1200&force_format=jpeg&q=100&width=1120.0&wat=1&wat_opacity=1&wat_gravity=northwest&wat_url=https://colony-recorder.s3.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=664,397)


4\. Click Run.

![](https://ajeuwbhvhr.cloudimg.io/https://colony-recorder.s3.amazonaws.com/files/2025-07-07/4f29816c-4803-4453-ae59-233991b30774/ascreenshot.jpeg?tl_px=506,319&br_px=1883,1088&force_format=jpeg&q=100&width=1120.0&wat=1&wat_opacity=1&wat_gravity=northwest&wat_url=https://colony-recorder.s3.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,277)


5\. Points display in QGIS. A KML was also exported in your file path.

![](https://ajeuwbhvhr.cloudimg.io/https://colony-recorder.s3.amazonaws.com/files/2025-07-07/42418443-8fb1-4171-92d4-e5d5b44311e9/ascreenshot.jpeg?tl_px=544,102&br_px=1920,871&force_format=jpeg&q=100&width=1120.0&wat=1&wat_opacity=1&wat_gravity=northwest&wat_url=https://colony-recorder.s3.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=669,276)


6\. Now do the same for Perimeters.

![](https://ajeuwbhvhr.cloudimg.io/https://colony-recorder.s3.amazonaws.com/files/2025-07-07/434534f2-f84d-4239-b286-dd5a9f517d18/ascreenshot.jpeg?tl_px=544,364&br_px=1920,1133&force_format=jpeg&q=100&width=1120.0&wat=1&wat_opacity=1&wat_gravity=northwest&wat_url=https://colony-recorder.s3.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=637,277)


7\. Replace the path and file name in the "OUT_KML_PATH" value.

![](https://ajeuwbhvhr.cloudimg.io/https://colony-recorder.s3.amazonaws.com/files/2025-07-07/c97bedba-23cc-4a63-a0ba-55c4a054044e/ascreenshot.jpeg?tl_px=544,430&br_px=1920,1200&force_format=jpeg&q=100&width=1120.0&wat=1&wat_opacity=1&wat_gravity=northwest&wat_url=https://colony-recorder.s3.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=540,458)


8\. Click run.

![](https://ajeuwbhvhr.cloudimg.io/https://colony-recorder.s3.amazonaws.com/files/2025-07-07/65f00bbc-f157-42d7-9cdd-738451266962/ascreenshot.jpeg?tl_px=509,316&br_px=1885,1085&force_format=jpeg&q=100&width=1120.0&wat=1&wat_opacity=1&wat_gravity=northwest&wat_url=https://colony-recorder.s3.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=524,277)


9\. The Perimeter layer is added in QGIS. Zoom in to inspect the perimeters.

![](https://ajeuwbhvhr.cloudimg.io/https://colony-recorder.s3.amazonaws.com/files/2025-07-07/d5aad71d-b03e-4810-9813-8b0556bea881/user_cropped_screenshot.webp?tl_px=272,215&br_px=1648,984&force_format=jpeg&q=100&width=1120.0)


10\. Open and refresh the location of your exported KML.

![](https://ajeuwbhvhr.cloudimg.io/https://colony-recorder.s3.amazonaws.com/files/2025-07-07/1d6af76b-dcdd-4e5b-b3c3-c1cb0dceed90/ascreenshot.jpeg?tl_px=0,0&br_px=1376,769&force_format=jpeg&q=100&width=1120.0&wat=1&wat_opacity=1&wat_gravity=northwest&wat_url=https://colony-recorder.s3.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=147,31)


11\. Perimeters were exported to KML directly. Incident Points were zipped in KMZ and also exported in KML. This is due to a need for packaging the proper symbology. Both the KML and KMZ should work in Google Earth.

![](https://ajeuwbhvhr.cloudimg.io/https://colony-recorder.s3.amazonaws.com/files/2025-07-07/413ab96b-51c6-423d-a0a6-b4a70e4bf5e9/ascreenshot.jpeg?tl_px=0,0&br_px=1376,769&force_format=jpeg&q=100&width=1120.0&wat=1&wat_opacity=1&wat_gravity=northwest&wat_url=https://colony-recorder.s3.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=289,143)


12\. Double-click the incident KML or KMZ and the perimeter KML

![](https://ajeuwbhvhr.cloudimg.io/https://colony-recorder.s3.amazonaws.com/files/2025-07-07/a990f11e-7e1a-4f71-b838-b87192240f6f/ascreenshot.jpeg?tl_px=0,0&br_px=1376,769&force_format=jpeg&q=100&width=1120.0&wat=1&wat_opacity=1&wat_gravity=northwest&wat_url=https://colony-recorder.s3.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=274,172)


13\. If Google Earth is your default, the KML/KMZ will open here. Otherwise you can drag the files in as well.

![](https://ajeuwbhvhr.cloudimg.io/https://colony-recorder.s3.amazonaws.com/files/2025-07-07/00d2ce2a-d63e-4829-af59-92261822277e/ascreenshot.jpeg?tl_px=0,0&br_px=1376,769&force_format=jpeg&q=100&width=1120.0&wat=1&wat_opacity=1&wat_gravity=northwest&wat_url=https://colony-recorder.s3.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=-18,201)


14\. After loading incident points, observe their symbology and naming structure in the left panel. Prescription Fires are yellow, Wildfires are red. They will also be scaled based on incident size.

![](https://ajeuwbhvhr.cloudimg.io/https://colony-recorder.s3.amazonaws.com/files/2025-07-07/8a6761ed-909b-4b3c-820f-48585a164eb5/ascreenshot.jpeg?tl_px=0,0&br_px=1376,769&force_format=jpeg&q=100&width=1120.0&wat=1&wat_opacity=1&wat_gravity=northwest&wat_url=https://colony-recorder.s3.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=-21,207)


15\. Open the Perimeters KML

![](https://ajeuwbhvhr.cloudimg.io/https://colony-recorder.s3.amazonaws.com/files/2025-07-07/f359b91a-05d3-458d-a79a-7164cf7ab5d0/ascreenshot.jpeg?tl_px=0,0&br_px=1376,769&force_format=jpeg&q=100&width=1120.0&wat=1&wat_opacity=1&wat_gravity=northwest&wat_url=https://colony-recorder.s3.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=280,150)


16\. Turn off the incident points at first to see the perimeters more clearly.

![](https://ajeuwbhvhr.cloudimg.io/https://colony-recorder.s3.amazonaws.com/files/2025-07-07/af9ea299-13de-45e4-aa8e-a32e9e2cde91/ascreenshot.jpeg?tl_px=0,0&br_px=1376,769&force_format=jpeg&q=100&width=1120.0&wat=1&wat_opacity=1&wat_gravity=northwest&wat_url=https://colony-recorder.s3.amazonaws.com/images/watermarks/FB923C_standard.png&wat_pad=-8,207)


17\. Zoom in to see the individual polygons.
Click one to view attributes.

![](https://colony-recorder.s3.amazonaws.com/files/2025-07-07/04a6c4c2-a64a-4398-b1c9-aacef897f664/stack_animation.webp)


18\. Enable both layers to compare. The large prescription fires may have corresponding perimeters. Both will be yellow for Rx.

![](https://colony-recorder.s3.amazonaws.com/files/2025-07-07/b0970835-8555-40ac-ac53-78f8e9c4572c/stack_animation.webp)


