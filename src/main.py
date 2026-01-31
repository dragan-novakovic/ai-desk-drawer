import FreeCAD as App
import FreeCADGui as Gui
import Part

doc = App.newDocument("PartTest")

box = Part.makeBox(10, 20, 30)
obj = doc.addObject("Part::Feature", "Box")
obj.Shape = box

# Set the box color to yellow
Gui.ActiveDocument.getObject(obj.Name).ShapeColor = (1.0, 1.0, 0.0)

doc.recompute()
Gui.SendMsgToActiveView("ViewFit")
