from ..datastructures.dcel import DCEL


def calculateFlipPath(triA: DCEL, triB: DCEL):
    """Computes the flip path between any two triangulations. 
    (The resulting triangulation will be a combinatorialy equivilent triangulation to triB not triB itself)
    
    Args:
        triA: The starting triangulation.
        triB: The ending triangulation.
    
    Returns:
        the flip path between triA and triB.
    """
    # Find the flip path between each trianguation and the canonical triangulation (c)
    aToC = triToCanonical(triA)
    bToC = triToCanonical(triB)
    cToB = bToC[::-1]

    # return the concat of aToC with the reverse of bToC (cToB) 
    return aToC + cToB

def triToCanonical(tri: DCEL):
    """Computes the flip path between any triangulation and the canonical triangulation. 
    
    Args:
        tri: The starting triangulation.
    
    Returns:
        the flip path between triA and the canonical triangulation.
    """
    # To transform a given triangulation into the canonical one, we fix an outer face and pick two of its
    # vertices, say a and b, to become the dominant vertices in the canonical triangulation. If a is not adjacent
    # to all other vertices, there exists a face uwv such that u and w are neighbours of a, while v is not. We flip the edge uw.

    # Duplicate the DECL so we can be destructive during this algorithm
    dTri = tri.duplicate()

    # Init path
    path = []
    
    # First we start by picking a node for a and b
    outerFace = dTri.boundaryVerts()
    a = outerFace[0]
    b = outerFace[1]

    while True:
        # Identify w
        w = 0

        # Check if we are done
        if (w in outerFace): break

        # Identify u
        u = 0

        # Find the face uwv
        uwv = 0

        # Find the complimentary face of edge uw
        uwk = 0

        # Flip the edge uw

        # Add edge uw to the path
        pass

    return path
