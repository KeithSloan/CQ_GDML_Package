import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

# Sector [startPhi, deltaPhi, units]
sector =[0,125,'deg']
# radius [min, max]
r1_base = [10,20]
r2_top =[2,4]
z = 25

v1 = gVol("world")
s1 = gBox(['worldBox',100,100,100])
m = gMaterial('G4_AIR0x55d123d17ea0')
v1.addObject(gObject('wo',s1,m,None,None))
v2 = gVol('Dummy')
v1.addVol(v2)
scone = gCone('cone1',r1_base, r2_top, z, sector)
# gObject(Name,Solid,Material,Position,Rotation)
o2 = gObject('oc',scone,m,None,None)
v2.addObject(o2)
#v2.addObject(gObject('oc',scone,m,None,None))
#show world volume
#show_object(v1.object2show())
#show volumes below world
show_object(v2.object2show())
#export world volume
#v1.exportVol("./exportedGDML/cone.gdml")