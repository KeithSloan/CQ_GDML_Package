from cadquery import Shape
from OCC.Core.gp import gp_Ax2, gp_Pnt, gp_Dir
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

ret = BRepPrimAPI_MakeBox(gp_Ax2(gp_Pnt(.0,.0, .0), gp_Dir(0, 0, 1)), 1.0, 2.0, 3.0).Shape()

# show_object needs a CadQuery object
result = Shape.cast(ret)

show_object(result)