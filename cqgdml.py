import PythonOCC

class gdml() :

    def make(self) :
        # ????

    class gObject(self,solid,position,rotation,material) :
       def __init__(self,name) :

    class gVol(self,name) :    

       def __init__(self,name) :
           self.Objects = []
           self.SubVols = []
           self.Name = name
       
       def addObject(obj) :
           append(self.Objects(obj))

       def addVol(vol) :
           append(self.SubVols(vols))

       def export(name) :
           for v in self.SubVols :

           for o in self.Objects :    

       def toFreeCAD():    

    class gMaterial(self, name) :    
       def __init__(self,name) :

    class gBox(x,y,z) :
       def __init__(self,x,y,z) :
           #self.x = x
           #self.y = y
           #self.z = z
           self.shape = BRepPrimAPI_MakeBox(x,y,z).Shape()
