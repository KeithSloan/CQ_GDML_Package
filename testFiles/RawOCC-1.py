import cadquery as cq

# need for reload
import importlib
#import cqgdml
import cqgdml
importlib.reload(cqgdml)
from cqgdml import *

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
ret = cq.CQ(BRepPrimAPI_MakeBox(100., 100., 100.).Shape())
show_object(ret)
#show_object(v.shape2show())
#v.exportVol("/tmp/file.gdml")