import OCC

class gObject(self,solid,position,rotation,material) :
      def __init__(self,name) :
          self.Name = name

class gVol(self,name) :    

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

class gMaterial(self, name) :    
      def __init__(self,name) :
          self.Name = name

class gBox(x,y,z) :
      def __init__(self,x,y,z) :
           self.x = x
           self.y = y
           self.z = z
           self.shape = BRepPrimAPI_MakeBox(x,y,z).Shape()
