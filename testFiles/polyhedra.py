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
num = 8
#zplane rmin, rmax,z
zplanes = [[1,9,10],[3,5,12]]

print("Start")
v = gVol("world")
s = gPolyhedra('poly1',num,zplanes,angle)
m = gMaterial('G4_AIR0x55d123d17ea0')
# gObject(Name,Solid,Material,Position,Rotation)
o = gObject("o1",s,m,None,None)
# Add Object to Volume
v.addObject(o)
#print("Show")
show_object(v.object2show())
#v.exportVol("./exportedGDML/polyhedra.gdml")