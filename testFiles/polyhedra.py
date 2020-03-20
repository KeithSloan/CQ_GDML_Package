import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

# Angle [startPhi, deltaPhi, units]
sector =[0,45,'deg']
# radius [min, max]
num = 8
#zplane rmin, rmax,z
zplanes = [[1,9,10],[3,5,12]]

v1 = gVol('world')
v2 = gVol('Dummy')
v1.addVol(v2)
sw = gBox(['Worldbox',100,100,100])
sp = gPolyhedra('poly1',num,zplanes,sector)
m = gMaterial('G4_AIR0x55d123d17ea0')
# gObject(Name,Solid,Material,Position,Rotation)
v1.addObject(gObject('wo',sw,m,None,None))
v2.addObject(gObject('po',sp,m,None,None))

#print("Show")
#show_object(v1.object2show())
show_object(v2.object2show())
#v1.exportVol("./exportedGDML/polyhedra.gdml")