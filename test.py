import cadquery
import cqgdml

position = 0
rotation = 0

v = gVol("world")
s = gBox(10,10,10)
m = gMaterial('Air')
o = gObject(s,m,position,rotation)
v.add(o)
v.export("/tmp/file.gdml")
