import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

rotation = ['angle', 30,0,0]

print("Start")
v = gVol("world")
s = gBox(["box1",10,10,10])
m = gMaterial('G4_AIR0x55d123d17ea0')
o1 = gObject("one",s,m,None,None)
v.addObject(o1)
o2 = gObject("two",s,m,['pos1',20,25,0],rotation)
v.addObject(o2)
show_object(v.shape2show())
v.exportVol("/tmp/file.gdml")