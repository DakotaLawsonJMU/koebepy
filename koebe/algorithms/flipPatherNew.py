from ..datastructures.dcel import DCEL, Edge

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
    cToB = triToCanonical(triB)
    cToB.reverse()

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
    
    # Pick an a and b
    outerFace = dTri.boundaryVerts()
    a = outerFace[0]
    b = outerFace[1]

    # This is necessary for the is canon check to work
    a.neighborsA = True
    b.neighborsB = True

    # Label all verts neighbor status
    aNeighbors = a.neighbors()
    bNeighbors = b.neighbors()
    for vert in dTri.verts:
        vert.neighborsA = vert in aNeighbors
        vert.neighborsB = vert in bNeighbors

    firstIter = True
    while not isCanonical(dTri):
        # Find a face uwv such that u and w are neighbors of a (or b) while v is not
        for uw in dTri.edges:
            endPts = uw.endPoints()
            u = endPts[0]
            w = endPts[1]

            # If this edge was just flipped skip it
            if (not firstIter and uw == path[-1]):
                continue

            # If this edge includes either a or b skip it
            if (u is a or u is b or w is a or w is b):
                continue
            
            # Both end points of the edge must neighbor a or b to be a canidate edge
            bothNeighborA = u.neighborsA and w.neighborsA
            bothNeighborB = u.neighborsB and w.neighborsB

            # If u and w are both neighbors of a, check if there is a v that does not neighbor a
            shouldFlipEdge = False
            if bothNeighborA:
                for face in uw.incidentFaces():
                    for v in face.vertices():
                        if not v.neighborsA:
                            flipTarget = v
                            shouldFlipEdge = True

            if shouldFlipEdge:
                break

            # If u and w are both neighbors of b, check if there is a v that does not neighbor b
            if bothNeighborB:
                for face in uw.incidentFaces():
                    for v in face.vertices():
                        if not v.neighborsB:
                            flipTarget = v
                            shouldFlipEdge = True

            if shouldFlipEdge:
                break

        print("flip")

        # Add uw to path
        path.append(uw)

        # Flip the edge uw
        flip(uw)

        aNeighbors = a.neighbors()
        bNeighbors = b.neighbors()
        flipTarget.neighborsA = flipTarget in aNeighbors
        flipTarget.neighborsB = flipTarget in bNeighbors
        u.neighborsA = u in aNeighbors
        u.neighborsB = u in bNeighbors
        w.neighborsA = w in aNeighbors
        w.neighborsB = w in bNeighbors

        firstIter = False

    return path, dTri

    
def isCanonical(tri: DCEL):
    """Checks if a given triangulation is the canonical triangle. 
    
    Args:
        tri: The triangulation.
    
    Returns:
        True if the triangulation is the canonical triangle.
    """
    
    for vert in tri.verts:
        if not vert.neighborsA:
            return False
    
    return True


def flip(edge: Edge):
    """Flips the shared edge of two triangulations. 
    
    Args:
        tri: The triangulation.
        edge: The edge to flip
    
    Returns:
        True if the flip was successful.
    """
    he = edge.aDart
    twin = he.twin

    a = he.origin
    b = he.dest
    c = he.next.dest
    d = twin.next.dest

    bc = he.next
    ca = he.next.next
    ad = twin.next
    db = twin.next.next

    abc = he.face
    abd = twin.face

    he.origin = c
    c.aDart = he
    bc.next = he
    he.prev = bc
    he.next = db
    db.prev = he
    db.next = bc
    bc.prev = db
    abc.aDart = he
    bc.face = abc
    db.face = abc
    b.aDart = bc

    twin.origin = d
    d.aDart = twin
    ad.next = twin
    twin.prev = ad
    twin.next = ca
    ca.next = ad
    ad.prev = ca
    ca.prev = twin
    abd.aDart = twin
    ca.face = abd
    ad.face = abd
    a.aDart = ad
