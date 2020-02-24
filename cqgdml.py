import OCC
import cadquery as cq

def writeHdr(fp) :
    fp.write('<?xml version="1.0" encoding="UTF-8" standalone="no" ?>')
    fp.write('<gdml xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:noNamespaceSchemaLocation="http://service-spi.web.cern.ch/service-spi/app/releases/GDML/schema/gdml.xsd"') 
    fp.write("\n")
    fp.write('<define/>')
    fp.write("\n")

def writeSolids(fp,solidList) :
    fp.write('<solids>\n')
    for s in solidList :
        s.writeSolid(fp)
    fp.write('</solids>\n')   

class gVol:    
      def __init__(self,name) :
          self.Name = name
          self.Objects = []
          self.SubVols = []
          #Combined shape of objects
          self.Shape = None 

      def shape2show(self) :
          return(self.Shape)

      def addObject(self,obj) :
          self.Objects.append(obj)
          shape = obj.getShape()
          if self.Shape != None :
             combined = self.Shape.add(shape)
             self.Shape = combined
          else :
             self.Shape = shape 

      def addVol(self,vol) :
          self.SubVols.append(vol)

      def exportVol(self, name, subvol = False ) :
          fp = open(name,"w")
          writeHdr(fp)
          print("Export Volume")
          if subvol == False : 
             # For now append Materials.xml
             print("Export Materials")
             from pathlib import Path
             mats = Path('./materials.xml').read_text()
             fp.write(mats)

             # Now deal with solids
             print("Export Solids")
             solidList = []
             solidNames = []
             self.getSolids(solidNames,solidList,True)
             print(solidNames)
             writeSolids(fp,solidList)

          # Now deal with structure
          fp.write('<structure>')
          fp.write('<volume name ="'+str(self.Name)+'">'
          # if more than one object have to output as vols & physvol
          numObj = len(self.Objects)
          if numObj == 1 :       
             self.Objects[0].exportObj(fp)
          elif numObj > 1 :
              # Ouput physvols
              for o in self.Objects :
                  fp.write('<physvol name="PV"'+o.Name+'">')
                  fp.write('<volumeref ref="LV'+o.Name+'">')
                  fp.write('</physvol>')
              fp.write('</volume>')
              # Now output LV's    
              for o in self.Objects :
                  fp.write('<volume name ="LV"'+o.Name+'">')
                  fp.write('<solidref ref="'+o.Solid.Name+'">')
                  fp.write('<materialref ref="'o.Solid.Material.Name+'">')
              fp.write('</volume>')
          for v in self.SubVols :
              fp.write('<physvol name="PV"'+v.Name+'">')
              fp.write('<volumeref ref="LV'+v.Name+'">')
              fp.write('</physvol>')
          fp.write('</volume>')
          fp.write('</structure>')

          fp.write('<setup name = "Default" version "1.0">')
          fp.write('<world ref="'+self.Name+'"/>')
          fp.write('</setup>')
          fp.close()

      def getSolids(self,nameList, solidList, subvol=True) :
          if len(self.SubVols) > 0 :
             for v in self.SubVols :
                 v.getSolids(nameList,solidList,True)
          
          if len(self.Objects) > 0 :
             for o in self.Objects :
                 solid = o.getSolid()
                 if solid != None :
                    name = solid.getName()
                    if name not in nameList :
                       nameList.append(name)
                       solidList.append(solid)


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
      def __init__(self,solid,material,position,rotation):
          self.Solid = solid
          self.Material = material
          self.Position = position
          self.Rotation = rotation

      def getShape(self):
          print("Get Object Shape")
          shape = self.Solid.getShape()
          if ( self.Position == [0,0,0] or self.Position == None ) :
             return(shape)
          else :
             print("Translate position") 
             fshape = shape.translate(cq.Vector(self.Position))
             return(fshape)

      def getMaterial(self, matList ) : 
          name = self.Material.getName()
          if name not in matList :
             matList.append(name)
             print(name)

      def getSolid(self) :
          return(self.Solid)

      def exportObj(self,fp) :
          print("Export Obj")
          fp.write('materialref ref="'+self.Material.Name+'"/>'
          fp.write('solidred ref="'+self.Solid.Name'"/>')        

class gBox :
      def __init__(self,name,x,y,z) :
           self.name = name
           self.x = x
           self.y = y
           self.z = z
           #self.shape = BRepPrimAPI_MakeBox(x,y,z).Shape()

      def getName(self) :
          return(self.name)

      def writeSolid(self,fp) :
          fp.write('<box name='+str(self.name)+' x="'+ \
                    str(self.x)+' y="'+str(self.y)+' z="'+str(self.z)+'/>\n')

      def getShape(self) :
          import cadquery as cq
          print("Get Shape gBox")
          return( cq.Workplane('XY').box(self.x,self.y,self.z))
