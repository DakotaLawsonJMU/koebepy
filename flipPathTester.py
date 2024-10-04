from koebepy.koebe.algorithms.flipPather import *
from koebepy.koebe.algorithms.incrementalConvexHull import randomConvexHullE3, incrConvexHull, orientationPointE3
from koebepy.koebe.algorithms.tutteEmbeddings import tutteEmbeddingE2
from koebepy.koebe.geometries.euclidean3 import PointE3
from koebepy.koebe.graphics.pngMaker import PngMaker


def testTriToCanon():
    # Generate a random triangulation using convex hull
    tri = randomConvexHullE3(8)
    tri.outerFace = tri.faces[0]
    tutteGraph = tutteEmbeddingE2(tri)

    # Genereate image for before any flips
    png = PngMaker(tutteGraph)
    png.generateEmbeddingPNG("../flipTests/canon/canonTestBefore")

    # Generate the flip path
    path = triToCanonical(tri)

    # Generate an image for every flip in the path
    i = 0
    for edge in path:
        flip(edge)
        tutteGraph = tutteEmbeddingE2(tri)
        png = PngMaker(tutteGraph)
        filename = "../flipTests/canon/" + i + ".png"
        png.generateEmbeddingPNG(filename)
        i += 1


def testTriToTri():
    # Generate 2 random triangulations using convex hull
    triA = randomConvexHullE3(8)
    triA.outerFace = triA.faces[0]
    tutteGraphA = tutteEmbeddingE2(triA)

    triB = randomConvexHullE3(8)
    triB.outerFace = triB.faces[0]
    tutteGraphB = tutteEmbeddingE2(triB)

    # Genereate image for before any flips
    png = PngMaker(tutteGraphA)
    png.generateEmbeddingPNG("../flipTests/tri/triA")

    png = PngMaker(tutteGraphB)
    png.generateEmbeddingPNG("../flipTests/tri/triB")

    # Generate the flip path
    path = calculateFlipPath(triA, triB)

    # Generate an image for every flip in the path
    i = 0
    for edge in path:
        flip(edge)
        tutteGraph = tutteEmbeddingE2(tri)
        png = PngMaker(tutteGraph)
        filename = "../flipTests/canon/" + i + ".png"
        png.generateEmbeddingPNG(filename)
        i += 1

def testFlip():
    # Sample 4 points to make the simplest triangulation
    points = [PointE3(1, 0, -1), PointE3(-1, 0, -1), PointE3(0, 1, -1), PointE3(0, -1, -1)]
    tri = incrConvexHull(points, orientationPointE3)
    tri.outerFace = tri.outerFace = tri.faces[0]
    tutteGraph = tutteEmbeddingE2(tri)

    # Genereate image for before the flip
    png = PngMaker(tutteGraph)
    png.generateEmbeddingPNG("../flipTests/flipTestBefore")

    # Find the center edge and flip it
    verts = tri.verts
    for edge in tri.edges:
        ends = edge.endPoints()
        if (ends[0] == verts[0] and ends[1] == verts[2]) or (ends[0] == verts[0] and ends[1] == verts[2]):
            flip(edge)
            break

    # Generate image for after the flip
    png = PngMaker(tutteGraph)
    png.generateEmbeddingPNG("../flipTests/flipTestAfter")


def main():
    testFlip()
    testTriToCanon()
    testTriToTri()

if __name__ == "__main__":
    main()