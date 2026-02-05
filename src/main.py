import FreeCAD as App
import FreeCADGui as Gui
import Part

# --- CONFIGURATION (Adjust for your specific desk) ---
h = 80.0        # Total drop height
w = 60.0        # Width (widened slightly for better stability)
d_top = 50.0    # Depth of the top mounting plate
t = 8.0         # Thickness (increased for maximum stiffness)
g_size = 45.0   # Height/Depth of the triangle supports
g_thick = 6.0   # Thickness of the support ribs
hole_r = 2.7    # Hole radius (approx 5.5mm diameter for a standard screw)

def create_fixed_bracket():
    # Setup Document
    doc = App.activeDocument()
    if not doc:
        doc = App.newDocument("Fixed_Slider_Bracket")

    # 1. Main L-Shape Body
    top_plate = Part.makeBox(w, d_top, t)
    side_plate = Part.makeBox(w, t, h)
    side_plate.translate(App.Vector(0, 0, -h + t))
    
    # 2. Outer-Edge Reinforcement Gussets
    # Create the triangle face
    p1 = App.Vector(0, t, 0)
    p2 = App.Vector(0, g_size, 0)
    p3 = App.Vector(0, t, -g_size)
    rib_face = Part.Face(Part.makePolygon([p1, p2, p3, p1]))
    
    # Left rib (Flush with the left edge)
    rib_left = rib_face.extrude(App.Vector(g_thick, 0, 0))
    rib_left.translate(App.Vector(0, 0, t))
    
    # Right rib (Flush with the right edge)
    rib_right = rib_face.extrude(App.Vector(g_thick, 0, 0))
    rib_right.translate(App.Vector(w - g_thick, 0, t))

    # Fuse the structural parts together
    body = top_plate.fuse(side_plate).fuse(rib_left).fuse(rib_right)

    # 3. Single Central Holes
    # Top Mounting Hole (Centered)
    h_top = Part.makeCylinder(hole_r, t + 2, App.Vector(w/2, d_top/2, -1))
    
    # Side Slider Hole (Centered)
    h_side = Part.makeCylinder(hole_r, t + 2, App.Vector(w/2, t + 1, -h/2))
    h_side.rotate(App.Vector(w/2, 0, -h/2), App.Vector(1, 0, 0), 90)

    # Final Boolean Cut to make the holes
    final_part = body.cut(h_top).cut(h_side)

    # 4. Push to Gui
    obj = doc.addObject("Part::Feature", "Clean_Bracket")
    obj.Shape = final_part
    
    doc.recompute()
    
    # Adjust the camera to see the result
    Gui.activeDocument().activeView().viewAxometric()
    Gui.SendMsgToActiveView("ViewFit")
    print("Bracket Fixed: Supports moved to edges, central hole cleared.")

create_fixed_bracket()