import OCC
import cadquery as cq

class gVol:    
      def __init__(self,name) :
          self.Objects = []
          self.SubVols = []
          self.Name = name

      def shape2show(self) :
          import cadquery as cq
          cq.Workplane.combine(self)
          return(cq.first(self))

      def addStack(self) :
          # Add to stack
          if len(self.SubVols) > 0 :
             print("Show Volume")
             for i in self.SubVols :
                 i.addStack()

          if len(self.Objects) > 0 :
             print("Show Objects")
             for i in self.Objects :
                 i.addStack()
              
      def addObject(self,obj) :
          self.Objects.append(obj)

      def addVol(self,vol) :
          self.SubVols.append(vols)

      def exportVol(self,name) :
          for v in self.SubVols :
            v.exportVol(name)

          for o in self.Objects :    
            o.exportObj()

      #def toFreeCAD():    

class gMaterial:    
      def __init__(self,name) :
          self.Name = name

class gObject:
      def __init__(self,solid,material,position,rotation):
          self.Solid = solid
          self.Material = material
          self.Position = position
          self.Rotation = rotation

      def addStack(self):
          print("Add Object")
          self.Solid.addStack(self.Position, self.Rotation)

      def exportObj(name):
          print("Export Obj")

class gBox :
      def __init__(self,x,y,z) :
           self.x = x
           self.y = y
           self.z = z
           #self.shape = BRepPrimAPI_MakeBox(x,y,z).Shape()

      def addStack(self, position, rotation) :
          import cadquery as cq
          print("Stack gBox")
          cq.add = cq.Workplane('XY').box(self.x,self.y,self.z)
