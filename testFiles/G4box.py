import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

rotation = 0

v1 = gVol("World")
v2 = gVol("Dummy")
v1.addVol(v2)
s1 = gBox("WorldBox",2000,2000,2000)
s2 = gBox("box",600,800,1200)
m = gMaterial('G4_AIR0x55d123d17ea0')
o1 = gObject(s1,m,None,rotation)
v1.addObject(o1)
o2 = gObject(s2,m,None,rotation)
v2.addObject(o2)
show_object(v1.shape2show())
v1.exportVol("/tmp/file.gdml")