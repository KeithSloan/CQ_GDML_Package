import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

# Angle [startPhi, deltaPhi, units]
angle =[0,45,'Deg']
# radius [min, max]
r1_base = [0,20]
r2_top =[0,4]
z = 25

print("Start")
v = gVol("world")
s = gCone('cone1',r1_base, r2_top, z, angle)
m = gMaterial('G4_AIR0x55d123d17ea0')
o = gObject("o1",s,m,None,None)
v.addObject(o)
#print("Show")
show_object(v.object2show())
#v.exportVol("/tmp/file.gdml")