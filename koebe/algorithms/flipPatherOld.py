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
    
    # First we start by picking a node for a and b
    outerFace = dTri.boundaryVerts()
    a = outerFace[0]
    b = outerFace[1]

    aNeighbors = a.neighbors()
    for vert in dTri.verts:
        if vert in aNeighbors:
            vert.neighborsA = True
        else:
            vert.neighborsA = False

    while True:
        # Find u, w, and v where u and w are adjacent to a and v is not
        v = None
        u = None
        w = None
        for vT in dTri.verts:
            if u != None:
                break
            if vT.neighborsA:
                continue
            for vNeigh in vT.neighbors(): # Could possibly do the set intersection here to combine work
                if u != None:
                    break
                if vNeigh == b or not vNeigh.neighborsA:
                    continue
                uT = vNeigh
                for uNeigh in uT.neighbors(): 
                    if uNeigh == b or not uT.neighborsA:
                        continue
                    if uNeigh in vT.neighbors():
                        w = uNeigh
                        u = uT
                        v = vT
                        break

        # If a is adjacent to all verticies in tri then tri is the canonical triangulation
        if v == None:
            break

        # Find the edge uw
        uw = None
        for dart in u.inDarts():
            if dart.origin == w:
                uw = dart

        # Add uw to path
        path.append(uw)

        # Flip the edge uw
        flip(uw)

    return path, dTri

def flip(edge):
    """Flips the shared edge of two triangulations. 
    
    Args:
        tri: The triangulation.
        edge: The edge to flip
    
    Returns:
        True if the flip was successful.
    """
    he = edge
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
