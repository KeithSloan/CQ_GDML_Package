import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

# Sector [startPhi, deltaPhi, units]
sector =[20,90,'deg']
# radius [min, max]
radius = [10,20]
z = 25

v1 = gVol('World')
v2 = gVol('Dummy')
v1.addVol(v2)
sw = gBox(['WorldBox',100,100,100])
st = gTube('tube',radius,z,sector)
m = gMaterial('G4_AIR0x55d123d17ea0')
# object 'name', shape, material, position, rotation
v1.addObject(gObject('o1',sw,m,None,None))
# Add Object to Volume
v2.addObject(gObject('t1',st,m,None,None))
#print("Show")
#show_object(v1.object2show())
show_object(v2.object2show())
v1.exportVol("./exportedGDML/tube.gdml")