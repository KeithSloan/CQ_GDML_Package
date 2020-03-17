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
i.e. Objects can be placed in volumes and the export will deal with Physical & Logical Volumes.

So to handle this and still export a valid gdml file the rules are 

  * World/Root volume must have a single object
  
  * Other volumes may have more that one object and the 
  
       * gdml export will create a GDML volume LV{object_name} for each object.
       * physvol's PV{object_name} will be created for each of these volumes

So when programming just have to remember world volume - single object
other volumes may have more that one object. 


  * Volume 
    
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

## Display
The cq-editor has the ability to switch between solid and wireframe.
If you want to display in solid then you may want to use

      show_object(v2.object2show())

Where v2 is the volume below the world volume v1 which in solid would hide the volumes
it contains.

## Uses
 
   PythonOCC
   
 ## Development Notes
 
 based on gdml.xsd
 
 * **'Volumes'**
 
    * **Must** have a **solid & material ref**
 
 * **PhysVol** 
 
     * Must contain **volref** ( or file ) 
     * volref **must not** be same as current volume name
     * May contain **position** or **position ref**
     * May contain **rotation** or **rotation ref**
 
