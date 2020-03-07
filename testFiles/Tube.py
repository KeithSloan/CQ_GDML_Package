import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

# Angle [startPhi, deltaPhi, units]
angle =[0,45,'deg']
# radius [min, max]
rad = [10,20]
z = 25

print("Start")
v = gVol("world")
s = gTube('Tube1',rad,z,angle)
m = gMaterial('G4_AIR0x55d123d17ea0')
# gObject(Name,Solid,Material,Position,Rotation)
o = gObject("o1",s,m,None,None)
# Add Object to Volume
v.addObject(o)
#print("Show")
show_object(v.object2show())
#v.exportVol("/tmp/file.gdml")