import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

#rotation = ['angle1',45,0,0]
rotation = None
position = ['pos1',10,20,30]

print("Start")
v1 = gVol("world")
v2 = gVol("Dummy")
v1.addVol(v2)
sw = gBox(['world',1000,1000,1000])
s1 = gBox(['box_1',10,40,50])
m = gMaterial('G4_AIR0x55d123d17ea0')
# gObject(Name,Solid,Material,Position,Rotation)
ow = gObject('ow',sw,m,None,None)
o1 = gObject('o1',s1,m,position,rotation)
v1.addObject(ow)
v2.addObject(o1)
print("Show")
show_object(v1.object2show())
v1.exportVol("./exportedGDML/singleBox.gdml")