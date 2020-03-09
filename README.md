# CQ_GDML_Package

Extension to [CADQuery](https://github.com/CadQuery/cadquery) to allow program creation of GDML models using

1. [CQ-Editor](https://github.com/CadQuery/CQ-editor)
2. Jupyter
3. Standalone Python

## Install requirement
Make sure PYTHONPATH includes directory that contains cqgdml.py

Needs lxml module
install via 
    
   pip install lxml

## Aim
Provide the function to allow CADQuery to create GDML Models.

## Design Point
Must be easier to program than specify via GDML

## Structure
I find GDML volumes a bit confusing so am going to diverge a bit.
i.e. Objects can be placed in volumes and the export will deal with Physical & Logical Volumes

  * Volume ( GDML Logical Volume )
    
    Set of Objects
  
  * Object
     
     * Solid ptr
     * Position
     * Rotation
     * Material ptr
  
  * Solid
     
    * Graphics Object
     
  * Material
  
## Materials
The exported materials section does an imbed of the materials.xml file
  
## Uses
 
   PythonOCC
   
 ## Development Notes
 
 based on gdml.xsd
 
 * **'World Volume'**
 
    * May or may not have solid & material ref
 
 * **PhysVol** 
 
     * Must contain **volref** ( or file ) 
     * volref **must not** be same as current volume name
     * May contain **position** or **position ref**
     * May contain **rotation** or **rotation ref**
 
