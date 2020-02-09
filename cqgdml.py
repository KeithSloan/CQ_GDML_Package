import OCC

class gVol:    
      def __init__(self,name) :
          self.Objects = []
          self.SubVols = []
          self.Name = name
       
      def addObject(self,obj) :
          append(self.Objects(obj))

      def addVol(self,vol) :
          append(self.SubVols(vols))

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

class gBox :
      def __init__(self,x,y,z) :
           self.x = x
           self.y = y
           self.z = z
           #self.shape = BRepPrimAPI_MakeBox(x,y,z).Shape()
