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
        aNeighbors = a.neighbors()

        # Find u, w, and v where u and w are adjacent to a and v is not
        v = None
        for aNeighbor in aNeighbors:
            if aNeighbor == b:
                continue

            for uNeighbor in aNeighbor.neighbors():
                if uNeighbor == b:
                    continue

                u = None
                v = None
                if uNeighbor not in aNeighbors:
                    u = aNeighbor
                    v = uNeighbor
                    w = None
                    vNeighbors = v.neighbors()
                    for vNeighbor in vNeighbors:
                        if (vNeighbor != u and a in vNeighbor.neigbors()):
                            w = vNeighbor
                            break
                    
                    if w != None:
                        break
            
            if v != None and u != None and w != None:
                break

        # If a is adjacent to all verticies in tri then tri is the canonical triangulation
        if v == None:
            break

        # Find the faces uwv and uwa
        for face in dTri.faces():
            if all(x in face.vertices() for x in [u, w, v]):
                uwv = face
                continue
            if all(x in face.vertices() for x in [u, w, a]):
                uwa = face
                continue

        # Flip the edge uw
        

    return path
