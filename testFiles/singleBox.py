import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

rotation = ['angle1',45,0,0]
position = ['box1',10,20,30]

print("Start")
v = gVol("world")
s = gBox(position)
m = gMaterial('G4_AIR0x55d123d17ea0')
o = gObject("o1",s,m,None,rotation)
v.addObject(o)
print("Show")
show_object(v.shape2show())
v.exportVol("/tmp/file.gdml")