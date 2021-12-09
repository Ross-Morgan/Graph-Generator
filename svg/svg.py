import svgwrite


drawing = svgwrite.Drawing("new.svg", profile="tiny")
drawing.add(drawing.line((0, 0), (10, 0), stroke=svgwrite.rgb(10, 10, 16, "%")))
drawing.save(pretty=True, indent=4)
