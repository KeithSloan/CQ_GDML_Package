# CQ-GDML-Module
Extension to Cad Query to allow program creation of GDML models

## Aim
Provide the function to allow cad-query to create GDML Models.

## Design Point
Must be easier to program than specify via GDML

## Structure
I find GDML volumes a bit confusing so am going to diverge a bit

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
  
## Uses
 
   PythonOCC
