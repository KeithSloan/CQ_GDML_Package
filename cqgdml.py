import OCC

class gVol:    
      def __init__(self,name) :
          self.Objects = []
          self.SubVols = []
          self.Name = name

      def show(self) :
          for i in SubVols :
              i.show
          for i in self.Objects :
              i.show
              
      def addObject(self,obj) :
          objects = []
          objects.tappend(obj)

      def addVol(self,vol) :
          SubVols.append(vols)

      def export(self,name) :
          for v in self.SubVols :
            exportVol(v)

          for o in self.Objects :    
            exportObj(o)

      #def toFreeCAD():    

class gMaterial:    
      def __init__(self,name) :
          self.Name = name

class gObject:
      def __init__(self,solid,material,position,rotation):
          self.Solid = solid
          self.Material = material
          self.Position = position
          self.rotation = rotation

      def show():
          self.Solid.show(self.Position, self.Rotation)

class gBox :
      def __init__(self,x,y,z) :
           self.x = x
           self.y = y
           self.z = z
           #self.shape = BRepPrimAPI_MakeBox(x,y,z).Shape()

      def show(position, rotation) :
          shape = BRepPrimAPI_MakeBox(x,y,z).Shape()
          show_object(shape)
