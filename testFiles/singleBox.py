import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

rotation = 0

v = gVol("world")
s = gBox("box1",10,10,10)
m = gMaterial('G4_AIR0x55d123d17ea0')
o = gObject("o1",s,m,None,rotation)
v.addObject(o)
show_object(v.shape2show())
v.exportVol("/tmp/file.gdml")