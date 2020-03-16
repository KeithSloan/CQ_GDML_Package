import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

#rotation = ['angle', 30,0,0]
rotation = None

v1 = gVol("world")
v2 = gVol('Dummy')
v1.addVol(v2)
s1 = gBox(['World_Box',100,100,100])
s2 = gBox(["box1",10,10,10])
m = gMaterial('G4_AIR0x55d123d17ea0')
# gObject(Name,Solid,Material,Position,Rotation)
v1.addObject(gObject("world",s1,m,None,None))
# gObject(Name,Solid,Material,Position,Rotation)
v2.addObject(gObject("one",s2,m,['pos1',20,25,0],rotation))
v2.addObject(gObject("two",s2,m,None,rotation))
show_object(v1.object2show())
v1.exportVol("./exportedGDML/doubleBox.gdml")