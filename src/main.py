import FreeCAD as App
import Part

doc = App.newDocument("PartTest")

box = Part.makeBox(10, 20, 30)
Part.show(box)

doc.recompute()
