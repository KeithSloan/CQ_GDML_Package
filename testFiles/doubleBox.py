import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

rotation = 0

#display, start_display, add_menu, add_function_to_menu = init_display()

v = gVol("world")
s = gBox("box1",10,10,10)
m = gMaterial('G4_AIR0x55d123d17ea0')
o1 = gObject(s,m,None,rotation)
v.addObject(o1)
o2 = gObject(s,m,[20,25,0],rotation)
v.addObject(o2)
show_object(v.shape2show())
v.exportVol("/tmp/file.gdml")