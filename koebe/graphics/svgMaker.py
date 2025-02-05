import cairo

class SvgMaker:
    
    def __init__(self, packing):
        self.packing = packing

    
    # could add custom colors easily
    # to add groups it would take some work you can use this library to edit the svg and add group tags 
    # around the appropriate areas https://docs.python.org/3/library/xml.etree.elementtree.html


    # Generates an svg from the provided packing
    # @param self the SvgMaker object that stores the packing
    # @param saveLocation the location where you want the svg to be saved
    # @param drawCircles turn on and off circle drawing
    # @param drawH2Graph turn on and off the hyperbolic graph
    # @param drawE2Graph turn on and off the euclidian graph
    def generateSVG(self, saveLocation="../a.svg", drawCircles=True, drawH2Graph=True, drawE2Graph=True):
        surface = cairo.SVGSurface(saveLocation, 1028, 1028)
        surface.restrict_to_version(cairo.SVG_VERSION_1_2)
        ctx = cairo.Context(surface)
        ctx.scale(512, 512)
        ctx.set_source_rgb(0, 0, 0)
        ctx.set_line_width(0.005)
        ctx.translate(1, 1)

        # draw circles
        if drawCircles:
            ctx.arc(0, 0, 1, 0, 7)
            ctx.stroke()

            for v in self.packing.verts:
                curCirc = v.data.toPoincareCircleE2()
                ctx.arc(curCirc.center.x, curCirc.center.y, curCirc.radius, 0, 7)
                ctx.stroke()

            ctx.set_line_width(0.004)
            ctx.set_source_rgb(255, 0, 0)

        # draw H2 Graph
        if drawH2Graph:
            visited = set()
            for v in self.packing.verts:
                curPoint = v.data.center.toPointE2()
                ctx.move_to(curPoint.x, curPoint.y)
                neighbors = v.neighbors()
                for n in neighbors:
                    if n in visited:
                        continue
                    curNeighbor = n.data.center.toPointE2()
                    ctx.line_to(curNeighbor.x, curNeighbor.y)
                    ctx.move_to(curPoint.x, curPoint.y)
                visited.add(v)
            ctx.stroke()

        ctx.set_source_rgb(0, 0, 255)

        # draw E2 Graph
        if drawE2Graph:
            visited = set()
            for v in self.packing.verts:
                curPoint = v.data.toPoincareCircleE2()
                ctx.move_to(curPoint.center.x, curPoint.center.y)
                neighbors = v.neighbors()
                for n in neighbors:
                    if n in visited:
                        continue
                    curNeighbor = n.data.toPoincareCircleE2()
                    ctx.line_to(curNeighbor.center.x, curNeighbor.center.y)
                    ctx.move_to(curPoint.center.x, curPoint.center.y)
                visited.add(v)
            ctx.stroke()

        surface.flush()
        surface.finish()
        