from cadquery import Shape
from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeCone

ret = BRepPrimAPI_MakeCone(gp_Ax2(gp_Pnt(.0,.0, .0), gp_Dir(0, 0, 1)),6,4,20).Shape()

# show_object needs a CadQuery object
result = Shape.cast(ret)

show_object(result)