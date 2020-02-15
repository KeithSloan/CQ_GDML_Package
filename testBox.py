height = 60.0
width = 80.0
thickness = 10.0

# make the base
result = cq.Workplane("XY").box(height, width, thickness)

# Render the solid
show_object(result)
