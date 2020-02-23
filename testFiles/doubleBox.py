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
s = gBox(10,10,10)
m = gMaterial('Air')
o1 = gObject(s,m,[0,0,0],rotation)
v.addObject(o1)
o2 = gObject(s,m,[20,20,0],rotation)
v.addObject(o2)
show_object(v.shape2show())
#v.exportVol("/tmp/file.gdml")
#display.DisplayShape(gVol, update=True )
#start_display()
