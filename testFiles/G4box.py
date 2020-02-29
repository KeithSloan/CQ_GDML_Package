import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

b1 = ["WorldBox",2000,2000,2000]
b2 = ["box",600,800,1200]

v1 = gVol("World")
v2 = gVol("Dummy")
v1.addVol(v2)
s1 = gBox(b1)
s2 = gBox(b2)
m = gMaterial('G4_AIR0x55d123d17ea0')
o1 = gObject("o1",s1,m,None,None)
v1.addObject(o1)
o2 = gObject("o2",s2,m,None,None)
v2.addObject(o2)
show_object(v1.shape2show())
v1.exportVol("/tmp/file.gdml")