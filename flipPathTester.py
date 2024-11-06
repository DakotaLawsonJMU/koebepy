from koebe.algorithms.flipPatherOld import *
from koebe.algorithms.incrementalConvexHull import randomConvexHullE3, incrConvexHull, orientationPointE3
from koebe.algorithms.tutteEmbeddings import tutteEmbeddingE2
from koebe.geometries.euclidean3 import PointE3
from koebe.graphics.pngMaker import PngMaker


def testTriToCanon():
    # Generate a random triangulation using convex hull
    tri = randomConvexHullE3(8)
    tri.outerFace = tri.faces[0]
    tutteGraph = tutteEmbeddingE2(tri)

    # Genereate image for before any flips
    png = PngMaker(tutteGraph)
    png.generateEmbeddingPNG("./flipTests/canon/canonTestBefore.png")

    # Generate the flip path
    path, dtri = triToCanonical(tri)

    tutteGraph = tutteEmbeddingE2(dtri)
    png = PngMaker(tutteGraph)
    png.generateEmbeddingPNG("./flipTests/canon/canonTestAfter.png")

    # Generate an image for every flip in the path
    # i = 0
    # for edge in path:
    #     flip(edge)
    #     tutteGraph = tutteEmbeddingE2(tri)
    #     png = PngMaker(tutteGraph)
    #     filename = "./flipTests/canon/" + str(i) + ".png"
    #     png.generateEmbeddingPNG(filename)
    #     i += 1


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
    png.generateEmbeddingPNG("./flipTests/tri/triA")

    png = PngMaker(tutteGraphB)
    png.generateEmbeddingPNG("./flipTests/tri/triB")

    # Generate the flip path
    path = calculateFlipPath(triA, triB)

    # Generate an image for every flip in the path
    i = 0
    for edge in path:
        flip(edge)
        tutteGraph = tutteEmbeddingE2(tri)
        png = PngMaker(tutteGraph)
        filename = "./flipTests/tri/" + str(i) + ".png"
        png.generateEmbeddingPNG(filename)
        i += 1

def testFlip():
    # Sample 5 points to make the simplest flipable triangulation
    tri = randomConvexHullE3(8)
    tri.outerFace = tri.outerFace = tri.faces[0]
    tutteGraph = tutteEmbeddingE2(tri)

    # Genereate image for before the flip
    png = PngMaker(tutteGraph)
    png.generateEmbeddingPNG("./flipTests/flipTestBefore.png")

    # Find a flipable edge and flip it
    for edge in tri.edges:
        ends = edge.endPoints()
        if (ends[0] not in tri.boundaryVerts() and ends[1] not in tri.boundaryVerts()):
            flip(edge)
            break

    # Regenerate Embedding
    tutteGraph = tutteEmbeddingE2(tri)

    # Generate image for after the flip
    png = PngMaker(tutteGraph)
    png.generateEmbeddingPNG("./flipTests/flipTestAfter.png")


def main():
    testTriToCanon()

if __name__ == "__main__":
    main()