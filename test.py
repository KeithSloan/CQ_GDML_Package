import cadquery
import cqgdml

v = gVol("world")
s = gBox(10,10,10)
m = gMaterial('Air')
o = gObject(s,m,position,rotation)
v.add(o)
v.export("/tmp/file.gdml")
