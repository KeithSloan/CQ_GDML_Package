import OCC
import cadquery as cq

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

      def getShape(self):
          print("Get Object Shape")
          shape = self.Solid.getShape()
          if ( self.Position == [0,0,0] or self.Position == None ) :
             return(shape)
          else :
             print("Translate position") 
             fshape = shape.translate(cq.Vector(self.Position))
             return(fshape)

      def exportObj(name):
          print("Export Obj")

class gBox :
      def __init__(self,x,y,z) :
           self.x = x
           self.y = y
           self.z = z
           #self.shape = BRepPrimAPI_MakeBox(x,y,z).Shape()

      def getShape(self) :
          import cadquery as cq
          print("Get Shape gBox")
          return( cq.Workplane('XY').box(self.x,self.y,self.z))
