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
    bToC = triToCanonical(triB)
    cToB = bToC.reverse()

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

    aNeighbors = a.neighbors()
    bNeighbors = b.neighbors()
    for vert in dTri.verts:
        vert.neighborsA = vert in aNeighbors
        vert.neighborsB = vert in bNeighbors

    while True:
        uw = None
        for edge in dTri.edges:
            endPts = edge.endPoints()
            if (endPts[0] == a or endPts[0] == b or endPts[1] == a or endPts[1] == b):
                continue
            bothNeighborA = endPts[0].neighborsA and endPts[1].neighborsA
            bothNeighborB = endPts[0].neighborsB and endPts[1].neighborsB
            if bothNeighborA and not bothNeighborB:
                next = False
                # Check that v is not adjacent to a,
                # and update v's neighbor status
                for face in uw.incidentFaces():
                    for v in face.verticies():
                        if v != a and v != uw.endPoints()[0] and v != uw.endPoints()[1]:
                            if v.neighborsA:
                                next = True
                                break
                            else:
                                v.neighborsA = True
                                break

                if next: continue
                uw = edge
                break
            if bothNeighborB and not bothNeighborA:
                next = False
                # Check that v is not adjacent to b,
                # and update v's neighbor status
                for face in uw.incidentFaces():
                    for v in face.verticies():
                        if v != b and v != uw.endPoints()[0] and v != uw.endPoints()[1]:
                            if v.neighborsB:
                                next = True
                                break
                            else:
                                v.neighborsB = True
                                break

                if next: continue
                uw = edge
                break


        # If there is no edge uw where its incedent faces are not auw and buw then dTri is the canonical tri
        if uw == None:
            break

        # Add uw to path
        path.append(uw)

        # Flip the edge uw
        flip(dTri, uw)

    return path


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
    he.dest = d
    c.aDart = he
    bc.next = he
    he.prev = bc
    he.next = db
    db.prev = he
    abc.aDart = he
    he.face = abc
    bc.face = abc
    db.face = abc
    b.aDart = bc

    twin.origin = d
    twin.dest = c
    d.aDart = twin
    ad.next = twin
    twin.prev = ad
    twin.next = ca
    ca.prev = twin
    abd.aDart = twin
    twin.face = abd
    ca.face = abd
    ad.face = abd
    a.aDart = ad
    
