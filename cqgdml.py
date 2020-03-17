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

####################
# Global Functions #
####################
# position is list of (name, x, y, z) 
def getPosition(pos) :
    if pos != None :
       val = pos[1:] 
       print(pos[1:])
       if val != [0,0,0] : 
          return val
    else :
       return False
      
def getPositionValue(pos) :
    print("Get Value")
    print(pos)
    if pos != None :
       val = pos[1:] 
       print(pos[1:]) 
       return (val)
    else :
       return [0,0,0]
      
def getPositionName(pos) :
    if pos != None :
       return pos[0]
    else :
       # Need to make unique 
       return('pos1') 

def getRotation(rot) :
    print("Get Rotation")
    print(rot)
    if rot != None :
        if rot[1:] != [0,0,0] : 
           return rot
    else :
       return False

def getRotationName(rot) :
    print("Get Rotation Name")
    print(rot)
    if rot != None :
       print(rot) 
       return rot[0] 
    else :
       return "Default-Rot"

class Error(Exception) :
    ''' Base class for other exceptions'''
    pass

class World_Volume_Must_Have_One_Object(Error) :
    ''' Raised if world volume does not have a single object'''
    pass


class gVol:    
    import lxml.etree  as ET
    
    def __init__(self,name,wire=False) :
        from OCC.Core.BRep import BRep_Builder
        from OCC.Core.TopoDS import TopoDS_Compound
        self.Name = name
        self.Wire = wire
        self.Objects = []
        self.SubVols = []
        #Combined shape of objects
        self.Compound = TopoDS_Compound() 
        self.Builder = BRep_Builder()
        self.Builder.MakeCompound(self.Compound)

    def object2show(self) :
        from cadquery import Shape
        print("Vol Object to Show")
        vs = self.shape2show()
        print("Return Vol Object")             
        return(Shape.cast(vs))

    def shape2show(self) :
        print("Vol Object to Show")
        if len(self.SubVols) > 0 :
           print("Get SubVols")
           for v in self.SubVols :
              svShape = v.shape2show()
              if svShape != None :
                 self.Builder.Add(self.Compound,svShape)
        print("Return Vol Shape")             
        return(self.Compound)

    def addObject(self,obj) :
        from OCC.Core.BRep import BRep_Builder
        from OCC.Core.TopoDS import TopoDS_Compound
        print("Add Object")
        self.Objects.append(obj)
        shape = obj.getShape()
        print("Got shape")
        print(shape)
        self.Builder.Add(self.Compound, shape)
        print("Shape added to Compound")

    def addVol(self,vol) :
        self.SubVols.append(vol)

    def exportLV(self, obj, name):
        import lxml.etree  as ET
        vol = ET.SubElement(structure,'volume', {'name': name})
        if obj != None :
           ET.SubElement(vol, 'materialref', {'ref': obj.getMaterialName()})
           ET.SubElement(vol, 'solidref', {'ref': obj.getSolidName()})
        return(vol)

    def exportObjectPosRot(self, obj, pvol):
        import lxml.etree  as ET
        #print("Get position")
        #print(obj.Position)
        pos = getPosition(obj.Position)
        #print(pos)
        if pos != False :
           posName = getPositionName(obj.Position)
           ET.SubElement(pvol, 'positionref', {'ref': posName})
           ET.SubElement(define, 'position',{'name': posName, \
              'unit':'mm', 'x': str(pos[0]), 'y':str(pos[1]), \
              'z':str(pos[2]) }) 

        print("get Rotation Value")
        rot = getRotation(obj.Rotation)
        print(rot)
        if rot != False :
           print("Export Rotation")
           #rotName = getRotationName(o.Rotation)
           ET.SubElement(pvol, 'rotationref', {'ref': rot[0]})
           ET.SubElement(define, 'rotation',{'name': rot[0], \
              'unit':'degree', 'x': str(rot[1]), 'y':str(rot[2]), \
              'z':str(rot[3])})

    def exportVolRef(self, vol, pvName, volref) :
        import lxml.etree  as ET
        pvol = ET.SubElement(vol, 'physvol', {'name' : pvName})
        ET.SubElement(pvol,'volumeref',{'ref': volref})
        return(pvol)

    def exportVolStructure(self, Parent, Name):
        # physvol must have volumeref
        # volumeref cannot refer to this volume
        # world volume must have single object
        import lxml.etree  as ET
        print("Export Volume Structure")

        # Need to export SubVols first
        subref = None
        numSub = len(self.SubVols)
        print("Num Sub Vols : "+str(numSub))
        if numSub > 0 :
           print("Deal with subVols")
           for o in self.SubVols :
               print("Export Sub Volume")
               subref = o.exportVolStructure(Name, o.Name)
        
        numObj = len(self.Objects)
        if numObj == 1 :
           obj = self.Objects[0]
           if obj.checkPosRot() == True :
              # As need Physvol and cannot refer to this volume.
              volName = 'Dummy'+obj.Name
              dvol = self.exportLV(obj ,volName)
              vol  = self.exportLV(None, Name)
              pvName = 'PV'+obj.Name
              pvol = self.exportVolRef(vol, pvName, volName)
              self.exportObjectPosRot(obj, pvol)
              retName = volName

           else :
              # No Physvol needed just output Volume 
              vol = self.exportLV(obj, Name)
              retName = Name
        if Parent == None : # Is this the world/root volume
           if numObj == 0 or numObj > 1 :
              raise World_Volume_Must_Have_One_Object 

        if numObj > 1 :
           print("More than One Object")
           # Output Object volumes first
           for obj in self.Objects :
               lvName = 'LV'+obj.Name
               lvol = self.exportLV(obj, lvName)
           # Output this Volume
           vol = ET.SubElement(structure, 'volume', {'name': Name })
           # now output physvol's
           for obj in self.Objects :
               pvName = 'PV'+obj.Name
               lvName = 'LV'+obj.Name
               pvol = self.exportVolRef(vol, pvName, lvName)
               if obj.checkPosRot() == True :
                  self.exportObjectPosRot(obj, pvol)
           retName = Name       
         
        if subref != None :
           # Do we have to export reference to subvolume
           self.exportVolRef(vol, 'PV'+retName, subref)
        
        return(retName)

    def exportVol(self, filename ) :
        import lxml.etree  as ET

        print("Export Volume")
        #attr_qname = etree.QName(
        gdml = ET.Element('gdml')
        #gdml = ET.Element('gdml',nsmap={
        #    'xsi':xsi:noNamespaceSchemaLocation="http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd" 
        global define
        define = ET.SubElement(gdml, 'define')
        #ent  = ET.Entity("materials")
        #materials = ET.SubElement(gdml, 'materials')
        #materials.append(ent)
        materials = ET.parse("./materials.xml").getroot()
        gdml.append(materials)
        
        # Now deal with solids
        solids = ET.SubElement(gdml, 'solids')
        print("Export Solids")
        solidNames = []
        self.getSolids(solids, solidNames,True)

        global structure
        structure = ET.SubElement(gdml, 'structure')
        setup = ET.SubElement(gdml, 'setup', {'name': 'Default', 'version': '1.0'})
        ET.SubElement(setup,'world', {'ref':self.Name})

        # Now deal with structure
        # if more than one object have to output as vols & physvol
        print("Export Volume")

        # Deal with this Volume and any subVols
        print("Volume : "+self.Name)
        self.exportVolStructure(None, self.Name)
        
        indent(gdml)
        print("Write GDML file")
        #with open(filename, "w", encoding='UTF-8') as xf:
        #    doc_type = """<?xml version="1.0" encoding="UTF-8"i standalone="no" ?>"""
        #    tostring = ET.tostring(gdml).decode('utf-8')
        #    file = f"{doc_type}{tostring}"
        #    xf.write(file)
        ET.ElementTree(gdml).write(filename)
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
          # Must save position as defined as maybe None
          # which effect export of GDML
          self.Position = position
          self.Rotation = rotation 
    
      def checkPosRot(self) : 
          # needed to check for physVol
          print("Check pos & rot")
          print(self.Position)
          print(self.Rotation)
          pos = getPosition(self.Position)
          print(pos)
          rot = getRotation(self.Rotation)
          print(rot)
          if pos != False or rot != False :
             print("Have a pos or rot")
             return True
          else :
             return False 

      def getShape(self):
          print("Get Object Shape")
          pos = getPositionValue(self.Position)
          print(pos)
          # Pass correct Position to Solid
          shape = self.Solid.getShape(pos, self.Rotation)
          return(shape)

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
      
class gSector :
      def __init__(self, sectorParms) :
          from math import pi
          from OCC.Core.gp import gp_Ax1, gp_Pnt, gp_Dir
          
          self.Start = sectorParms[0]
          self.Delta = sectorParms[1]
          self.Aunit = sectorParms[2]
          self.RevAxis = gp_Ax1(gp_Pnt(0,0,0), gp_Dir(0,0,1))
          self.Pi = pi
          self.TwoPi = 2*(pi)

      def getStart(self) :
          # get Start in Radians
          if self.Aunit == 'rad' :
             return self.Start
          else :
             return self.Start * self.TwoPi / 360

      def getDelta(self) :
          # get Delta in Radians
          if self.Aunit == 'rad' :
             return self.Delta
          else : 
             return self.Delta * self.TwoPi / 360

      def getAunit(self) :
          return self.Aunit

      def less90(self) :
          if self.getDelta() < self.Pi :
             return True 

      def completeRev(self) :
          print("Test if complete rev")
          if self.Delta == 360 and self.Units == 'deg' :
             return True
          if self.Delta == self.TwoPi and self.Units == 'rad' :
             return True
          return False

      def makeRect(self,r,h) :

          from OCC.Core.gp import gp_Pnt
          from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeWire
          from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeEdge
          from OCC.BRepBuilderAPI import BRepBuilderAPI_MakeFace

          print("Make Rect")
          wire = BRepBuilderAPI_MakeWire()
          print("Make Points")
          p1 = gp_Pnt(0,0,0)
          p2 = gp_Pnt(r,0,0)
          p3 = gp_Pnt(r,0,h)
          p4 = gp_Pnt(0,0,h)
          print("make Edges")
          wire.Add(BRepBuilderAPI_MakeEdge(p1,p2).Edge())
          wire.Add(BRepBuilderAPI_MakeEdge(p2,p3).Edge())
          wire.Add(BRepBuilderAPI_MakeEdge(p3,p4).Edge())
          wire.Add(BRepBuilderAPI_MakeEdge(p4,p1).Edge())
          print("Make Face")
          face = BRepBuilderAPI_MakeFace(wire.Wire()).Face()
          print("Return Face")
          return face

      def rotate(self,shape) :
          from OCC.Core.gp import gp_Trsf
          from OCC.BRepBuilderAPI import BRepBuilderAPI_Transform

          trns = gp_Trsf()
          trns.SetRotation(self.RevAxis,self.getStart())
          brep_trns = BRepBuilderAPI_Transform(shape, trns, False)
          brep_trns.Build()
          shape = brep_trns.Shape()
          return shape

      def makeCylSection(self,r,h) :
          print("makeCylSection")
          import cadquery as cq
          from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
          from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeRevol
          
          rect = self.makeRect(r,h)
          print("rect made")
          print(self.getDelta())
          shape = BRepPrimAPI_MakeRevol(rect,self.RevAxis, \
                         self.getDelta()).Shape()
          return shape

      def makeCut(self,r,h,shape) :
          from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut
          cyl = self.makeCylSection(r,h)
          cut = BRepAlgoAPI_Cut(shape, cyl).Shape()
          return cut

      def makeCommon(self,r,h,shape) :
          from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Common
          cyl = self.makeCylSection(r,h)
          common = BRepAlgoAPI_Common(cyl, shape).Shape()
          return common

class gBox :
      def __init__(self,boxParms) :
           self.Name = boxParms[0]
           self.BoxParms = boxParms[1:]

      def getName(self) :
          return(self.Name)
      
      def exportSolid(self,solids) :
          
          import lxml.etree  as ET
          print("Export box")

          parms = self.BoxParms 
          ET.SubElement(solids, 'box', {'name': self.Name,
                             'x': str(parms[0]), \
                             'y': str(parms[1]), \
                             'z': str(parms[2]), \
                             'lunit': 'mm'})


      def getShape(self, pos, rotation) :
          # Note: passed Position and Rotation should be valid
          import cadquery as cq
          from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir
          from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
          print("Get Shape gBox")
          print(self.BoxParms)
          parms = self.BoxParms
          print("Pos")
          print(pos)
          x = pos[0] - parms[0]/2
          y = pos[1] - parms[1]/2
          z = pos[2] - parms[2]/2
          ret = BRepPrimAPI_MakeBox(gp_Ax2(gp_Pnt(x,y,z), \
                  gp_Dir(0., 0., 1.)),\
                  parms[0],parms[1],parms[2]).Shape()
          return(ret)

class gCone :
      def __init__(self,name, r1, r2, z, sector) :
           self.Name = name
           self.R1 = r1
           self.R2 = r2
           self.Z  = z
           self.Sector = None
           if sector != None :
              self.Sector = gSector(sector)

      def getName(self) :
          return(self.Name)
      
      def exportSolid(self,solids) :
          
          import lxml.etree  as ET
          print("Export Cone")

          ET.SubElement(solids, 'cone', {'name': self.Name,
                             'rmin1': str(self.R1[0]), \
                             'rmax1': str(self.R1[1]), \
                             'rmin2': str(self.R2[0]), \
                             'rmax2': str(self.R2[1]), \
                             'startphi' : str(self.Sector.getStart()), \
                             'deltaphi' : str(self.Sector.getDelta()), \
                             'z': str(self.Z), \
                             'aunit' : 'rad',
                             'lunit': 'mm'})


      def getShape(self, pos, rotation) :
          import cadquery as cq
          from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir
          from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCone
          from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut

          print("Get Shape gCone")
          x = pos[0]
          y = pos[1]
          z = pos[2]
          cone1 = BRepPrimAPI_MakeCone(gp_Ax2(gp_Pnt(x,y,z), \
                  gp_Dir(0, 0, 1)),\
                  self.R1[1], self.R2[1], self.Z).Shape()
          if (self.R1[0] != 0 or self.R2[0] != 0 ) :
             cone2 = BRepPrimAPI_MakeCone(gp_Ax2(gp_Pnt(x,y,z), \
                  gp_Dir(0, 0, 1)),\
                  self.R1[0], self.R2[0], self.Z).Shape()
             cone1 = BRepAlgoAPI_Cut(cone1, cone2).Shape()
          if self.Sector != None :
             if self.Sector.completeRev() == False :
                print("Need to section")
                if self.Sector.less90() == True :
                   print("Common")
                   shape = self.Sector.makeCommon(self.R1[1], self.Z, cone1) 
                else :
                   print("Cut") 
                   shape = self.Sector.makeCut(self.R1[1], self.Z, cone1)
                if self.Sector.getStart() == 0 :
                   return shape
                else :
                   return self.Sector.rotate(shape)
          print("Cone Shape")
          print(cone1)
          return(cone1)

class gTube :
      def __init__(self,name, radius, z, sector) :
           self.Name   = name
           self.Radius = radius
           self.Z  = z
           self.Sector = None
           if sector != None :
              self.Sector = gSector(sector)

      def getName(self) :
          return(self.Name)
      
      def exportSolid(self,solids) :
          
          import lxml.etree  as ET
          print("Export Tube")

          if self.Angle != None :
             ET.SubElement(solids, 'tube', {'name': self.Name,
                             'rmin': str(self.Radius[0]), \
                             'rmax': str(self.Radius[1]), \
                             'z': str(self.Z), \
                             'startphi':str(self.Sector.getStart()), \
                             'deltaphi':str(self.Sector.getDelta()), \
                             'aunit': str(self.Sector.getAunit()), \
                             'lunit': 'mm'})

          else :
             ET.SubElement(solids, 'tube', {'name': self.Name,
                             'rmin': str(self.Radius[0]), \
                             'rmax': str(self.Radius[1]), \
                             'z': str(self.Z), \
                             'lunit': 'mm'})


      def getShape(self, pos, rotation) :
          import cadquery as cq
          from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir
          from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
          from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut

          print("Get Shape gTube")
          x = pos[0]
          y = pos[1]
          z = pos[2]
          tube1 = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x,y,z), \
                  gp_Dir(0, 0, 1)),\
                  self.Radius[1], self.Z).Shape()
          if self.Radius[0] != 0 :
             tube2 = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x,y,z), \
                     gp_Dir(0, 0, 1)),\
                     self.Radius[0], self.Z).Shape()
             tube1 = BRepAlgoAPI_Cut(tube1, tube2).Shape()
          #if self.Angle != None :
          #   if self.Angle.completeRev() == False :
          #      print("Sub Cylinder section")
          #print("Cone Shape")
          return(tube1)

class gPolyhedra :
      def __init__(self,name, num, zplanes, angle) :
           self.Name    = name
           self.Num     = num
           self.Zplanes = zplanes
           self.Angle = None
           if angle != None :
              self.Angle = gAngle(angle)

      def getName(self) :
          return(self.Name)
      
      def exportSolid(self,solids) :
          
          import lxml.etree  as ET
          print("Export Tube")

          if self.Angle != None :
             poly = ET.SubElement(solids, 'polyhedra', {'name': self.Name,
                             'numsides': str(self.Num), \
                             'startphi':str(self.angle.getStart()), \
                             'deltaphi':str(self.angle.getDelta()), \
                             'aunit': str(self.angle.getAunit()), \
                             'lunit': 'mm'})
             print(len(self.Zplanes))
             for i in self.Zplanes :
                 print(i)
                 ET.SubElement(poly,'zplane',{'rmin=':str(i[0]), \
                                             'rmax=':str(i[1]), \
                                             'z=':str(i[2])})


      def getShape(self, pos, rotation) :
          import cadquery as cq
          from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir
          #from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCylinder
          from OCC.Core.BRepAlgoAPI import BRepAlgoAPI_Cut

          print("Get Shape gPolyhwdra")
          x = pos[0]
          y = pos[1]
          z = pos[2]
          #tube1 = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x,y,z), \
          #        gp_Dir(0, 0, 1)),\
          #        self.Radius[1], self.Z).Shape()
          #if self.Radius[0] != 0 :
          #   tube2 = BRepPrimAPI_MakeCylinder(gp_Ax2(gp_Pnt(x,y,z), \
          #           gp_Dir(0, 0, 1)),\
          #           self.Radius[0], self.Z).Shape()
          #   tube1 = BRepAlgoAPI_Cut(tube1, tube2).Shape()
          #if self.Angle != None :
          #   if self.Angle.completeRev() == False :
          #      print("Sub Cylinder section")
          #print("Cone Shape")
          #return(tube1)

