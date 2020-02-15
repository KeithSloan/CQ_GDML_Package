import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

position = 0
rotation = 0

#display, start_display, add_menu, add_function_to_menu = init_display()

v = gVol("world")
s = gBox(10,10,10)
m = gMaterial('Air')
o = gObject(s,m,position,rotation)
v.addObject(o)
v.show()
#v.exportVol("/tmp/file.gdml")
#display.DisplayShape(gVol, update=True )
#start_display()
