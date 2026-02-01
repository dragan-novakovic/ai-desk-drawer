import FreeCAD as App
import FreeCADGui as Gui
import Part

doc = App.newDocument("DeskMountingBrackets")

# Dimensions (in mm)
bracket_length = 450        # Length along desk
bracket_width = 40          # Width of mounting surface
bracket_thickness = 3       # Metal thickness
mounting_flange_height = 30 # Height of vertical flange for slide attachment
slide_offset = 15           # Distance from desk edge

# Create left mounting bracket
# Horizontal mounting plate (attaches to underside of desk)
left_horizontal = Part.makeBox(bracket_width, bracket_length, bracket_thickness)

# Vertical flange (for drawer slide attachment)
left_vertical = Part.makeBox(bracket_thickness, bracket_length, mounting_flange_height)
left_vertical.translate(App.Vector(bracket_width - bracket_thickness, 0, -mounting_flange_height))

# Combine
left_bracket = left_horizontal.fuse(left_vertical)

# Create right mounting bracket (mirror of left)
right_horizontal = Part.makeBox(bracket_width, bracket_length, bracket_thickness)
right_vertical = Part.makeBox(bracket_thickness, bracket_length, mounting_flange_height)
right_vertical.translate(App.Vector(0, 0, -mounting_flange_height))

right_bracket = right_horizontal.fuse(right_vertical)
right_bracket.translate(App.Vector(600, 0, 0))  # Position on opposite side

# Screw holes for mounting to desk (on horizontal plates)
screw_diameter = 5  # M5 screws for desk mounting
desk_screw_positions = [
    # Left bracket holes
    (10, 50, 0),
    (30, 50, 0),
    (10, bracket_length / 2, 0),
    (30, bracket_length / 2, 0),
    (10, bracket_length - 50, 0),
    (30, bracket_length - 50, 0),
]

# Add screw holes to left bracket
for x, y, z in desk_screw_positions:
    hole = Part.makeCylinder(screw_diameter / 2, bracket_thickness * 2)
    hole.translate(App.Vector(x, y, -bracket_thickness / 2))
    left_bracket = left_bracket.cut(hole)

# Add screw holes to right bracket (mirrored)
for x, y, z in desk_screw_positions:
    hole = Part.makeCylinder(screw_diameter / 2, bracket_thickness * 2)
    hole.translate(App.Vector(600 + x, y, -bracket_thickness / 2))
    right_bracket = right_bracket.cut(hole)

# Screw holes for drawer slides (on vertical flanges)
slide_screw_positions = [
    (50,),
    (150,),
    (250,),
    (350,),
]

for (y,) in slide_screw_positions:
    # Left bracket slide holes
    hole_left = Part.makeCylinder(screw_diameter / 2, bracket_thickness * 2)
    hole_left.rotate(App.Vector(bracket_width - bracket_thickness, y, -mounting_flange_height / 2), App.Vector(0, 1, 0), 90)
    hole_left.translate(App.Vector(bracket_width - bracket_thickness * 1.5, 0, 0))
    left_bracket = left_bracket.cut(hole_left)
    
    # Right bracket slide holes
    hole_right = Part.makeCylinder(screw_diameter / 2, bracket_thickness * 2)
    hole_right.rotate(App.Vector(600, y, -mounting_flange_height / 2), App.Vector(0, 1, 0), 90)
    hole_right.translate(App.Vector(600 - bracket_thickness / 2, 0, 0))
    right_bracket = right_bracket.cut(hole_right)

# Combine both brackets
brackets = left_bracket.fuse(right_bracket)

# Create the object in FreeCAD
obj = doc.addObject("Part::Feature", "MountingBrackets")
obj.Shape = brackets

# Set color to metal gray
Gui.ActiveDocument.getObject(obj.Name).ShapeColor = (0.7, 0.7, 0.75)

doc.recompute()
Gui.SendMsgToActiveView("ViewFit")
