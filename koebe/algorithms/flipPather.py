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
    # Find the flip path between each trianguation and the canonical triangulation
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