# -*- coding: utf8 -*-
#**************************************************************************
#*                                                                        *
#*   Copyright (c) 2020 Keith Sloan <keith@sloan-home.co.uk>              *
#*                                                                        *
#*   This program is free software; you can redistribute it and/or modify *
#*   it under the terms of the GNU Lesser General Public License (LGPL)   *
#*   as published by the Free Software Foundation; either version 2 of    *
#*   the License, or (at your option) any later version.                  *
#*   for detail see the LICENCE text file.                                *
#*                                                                        *
#*   This program is distributed in the hope that it will be useful,      *
#*   but WITHOUT ANY WARRANTY; without even the implied warranty of       *
#*   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the        *
#*   GNU Library General Public License for more details.                 *
#*                                                                        *
#*   You should have received a copy of the GNU Library General Public    *
#*   License along with this program; if not, write to the Free Software  *
#*   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307 *
#*   USA                                                                  *
#*                                                                        *
#*   Acknowledgements :                                                   *
#*                                                                        *
#*                                                                        *
#**************************************************************************

import OCC
import cadquery as cq

#########################################################
# Pretty format GDML                                    #
#########################################################
def indent(elem, level=0):
    i = "\n" + level*"  "
    j = "\n" + (level-1)*"  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
        for subelem in elem:
            indent(subelem, level+1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = j
    else:
        if level and (not elem.tail or not elem.tail.strip()):
            elem.tail = j
    return elem

def writeHdr(fp) :
    fp.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>')
    fp.write('<gdml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd"') 


class gVol:    
    import lxml.etree  as ET
    
    def __init__(self,name,wire=False) :
        self.Name = name
        self.Wire = wire
        self.Objects = []
        self.SubVols = []
        #Combined shape of objects
        self.Shape = None 

    def shape2show(self) :
        print("Vol Shape to Show")
        vs = self.Shape
        if len(self.SubVols) > 0 :
           print("Get SubVols")
           for v in self.SubVols :
               svShape = v.shape2show()
               if svShape != None :
                  if vs != None :
                     combined = vs.add(svShape)
                     vs = combined
                  else :   
                     vs = svShape 
        print("Return Vol Shape")             
        return(vs)

    def addObject(self,obj) :
        print("Add Object")
        self.Objects.append(obj)
        shape = obj.getShape()
        if self.Shape != None :
           combined = self.Shape.add(shape)
           self.Shape = combined
        else :
           self.Shape = shape 

    def addVol(self,vol) :
        self.SubVols.append(vol)

    def exportPosition(self, define, pos) :    
        global POScount
        if pos != False :
           posName = 'Pos'+name+str(POScount)
           POScount += 1
           ET.SubElement(define, 'position', {'name': posName, 'unit': 'mm', \
                      'x': str(pos[0]), 'y': str(pos[1]), 'z':str(pos[2])})     

    def exportVol(self, filename, subvol = False ) :
        import lxml.etree  as ET

        print("Export Volume")
        if subvol == False :
           gdml = ET.Element('gdml') 
           define = ET.SubElement(gdml, 'define')
           structure = ET.SubElement(gdml, 'structure')
           setup = ET.SubElement(gdml, 'setup', {'name': 'Default', 'version': '1.0'})
           ET.SubElement(setup,'world', {'ref':self.Name})
           ent  = ET.Entity("materials")
           materials = ET.SubElement(gdml, 'materials')
           materials.append(ent)

           # Now deal with solids
           solids = ET.SubElement(gdml, 'solids')
           print("Export Solids")
           solidNames = []
           self.getSolids(solids, solidNames,True)

        # Now deal with structure
        # if more than one object have to output as vols & physvol
        print("Export Volume")
        vol = ET.SubElement(structure,'Volume', {'name': self.Name})
          
        numObj = len(self.Objects)
        if numObj == 1 :       
           o = self.Objects[0] 
           ET.SubElement(vol, 'materialref', {'ref': o.getMaterialName()})
           ET.SubElement(vol, 'solidref', {'ref': o.getSolidName()})
          
        elif numObj > 1 :
           # Ouput physvols
           for o in self.Objects :
               pvname = 'PV'+o.Name
               print('<physvol : '+pvname)
               pvol = ET.SubElement(vol,'volume', {'name': pvname})
               ET.SubElement(pvol, 'materialref', {'ref': o.getMaterialName()})
               ET.SubElement(pvol, 'solidref', {'ref': o.getSolidName()})

        for v in self.SubVols :
              pvname = 'PV'+v.Name
              print('<physvol : '+pvname)
              pvol = ET.SubElement(vol,'volume', {'name': pvname})
              ET.SubElement(pvol, 'materialref', {'ref': o.getMaterialName()})
              ET.SubElement(pvol, 'solidref', {'ref': o.getSolidName()})
              exportPosition(define, o.Position)

        indent(gdml)
        print("Write GDML file")
        #ET.ElementTree(gdml).write(filename)
        with open(filename, "w", encoding='UTF-8') as xf:
            doc_type = """<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE doc [
<!ENTITY materials SYSTEM "materials.xml">
]>"""
            tostring = ET.tostring(gdml).decode('utf-8')
            file = f"{doc_type}{tostring}"
            xf.write(file)
        print("GDML file written")

    def getSolids(self, solids, nameList, subvol=True) :
        print("Get Solids")
        if len(self.SubVols) > 0 :
           for v in self.SubVols :
               v.getSolids(solids, nameList, True)
          
        if len(self.Objects) > 0 :
           print("Volume Get Objects")
           for o in self.Objects :
               sld = o.getSolid()
               if sld != None :
                  print("Get name")
                  name = sld.getName()
                  print(name)
                  if name not in nameList :
                     nameList.append(name)
                     print("export Solid")
                     sld.exportSolid(solids)


    def exportMaterials(self, name, subvol = False ) :
        print("Export Materials")
        matList = []
        if len(self.SubVols) > 0 :
           for v in self.SubVols :
               mat = v.getMateials(matList,True)
               if mat != None :
                  matList.append(mat)

        print("Objects materials")
        if len(self.Objects) > 0 :
           for o in self.Objects :
               mat = o.getMaterial(matList)
               if mat != None :
                 matList.append(mat)

        print(matList)

    def getMaterials(self, matList, subvol = False ) :
        print("Get Materials")
        if subvol == True :
           if len(self.SubVols) > 0 :
              for s in self.SubVols : 
                  mat = s.getMaterials()
                  if mat != None :
                     matList.append(mat) 

        if len(self.Objects) > 0 :
           for o in self.Objects :
               mat = o.getMaterials()
               if mat != None :
                  matList.append(mat)

class gMaterial:    
      def __init__(self,name) :
          self.Name = name

      def getName(self) :
          return(self.Name)

class gObject:
      def __init__(self,name,solid,material,position,rotation):
          self.Name = name
          self.Solid = solid
          self.Material = material
          self.Position = position
          if rotation != None :
             self.Rotation = float(rotation)

      def getPosition(self) :
          if self.Position == [0,0,0] or self.Position == None :
             return(False)
          else :
             return self.Position

      def getShape(self):
          print("Get Object Shape")
          shape = self.Solid.getShape()
          if self.Rotation != None :
             print("Rotate Shape")
             # We are dealing with XY plane so rotate about z axis
             rshape = shape.rotate((.0,.0,.0),(.0,.0,.10), self.Rotation)
             print("Shape Rotated")
          else :   
             rshape = shape   
          if ( self.Position == [0,0,0] or self.Position == None ) :
             print("Null Position") 
             return(rshape)
          else :
             print("Translate position") 
             fshape =rshape.translate(cq.Vector(self.Position))
             return(fshape)

      def getMaterial(self, matList ) : 
          name = self.Material.getName()
          if name not in matList :
             matList.append(name)
             print(name)
      
      def getMaterialName(self) : 
          return(self.Material.getName())

      def getSolid(self) :
          return(self.Solid)

      def getSolidName(self) :
          return(self.Solid.getName())

      def exportObject(self,fp) :
          print("Export Obj")
          #fp.write('materialref ref="'+self.Material.Name+'"/>')
          #fp.write('solidred ref="'+self.Solid.Name+'"/>')        

class gBox :
      def __init__(self,name,x,y,z) :
           self.Name = name
           self.X = x
           self.Y = y
           self.Z = z
           #self.shape = BRepPrimAPI_MakeBox(x,y,z).Shape()

      def getName(self) :
          return(self.Name)

      def exportSolid(self,solids) :
          
          import lxml.etree  as ET
          print("Export box")

          ET.SubElement(solids, 'box', {'name': self.Name,
                             'x': str(self.X), \
                             'y': str(self.Y), \
                             'z': str(self.Z), \
                             'lunit': 'mm'})


      def getShape(self) :
          import cadquery as cq
          print("Get Shape gBox")
          return( cq.Workplane('XY').box(self.X,self.Y,self.Z))
