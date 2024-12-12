import numpy as np
from scipy.linalg import null_space
from koebe.geometries.spherical2 import DiskS2

def edgeRow(edgeIdx, disks, edgeList):
    """Builds a row pair of the rigidity matrix given an i, j pair.
    
    Args:
        edgeIdx: The index of the edge in the edge list.
        disks: The list of all points and their associated disks.
        edgeList: The list of all edges in the packing.
    
    Returns:
        The row to be incerted into the rigidity matrix as an numpy array.
    """
    i, j = edgeList[edgeIdx]
    pi = tuple(disks[i])
    pj = tuple(disks[j])
    cij = [pj[0] - pi[0], pj[1] - pi[1], pj[2] - pi[2], pi[3] - pj[3]]
    cji = [pi[0] - pj[0], pi[1] - pj[1], pi[2] - pj[2], pj[3] - pi[3]]
    return np.array([
        cij if vIdx == i else
        cji if vIdx == j else
        [0,0,0,0]
        for vIdx in range(len(disks) - 1)
    ]).flatten()

def vertexPin(vIdx, disks):
    """Builds the necessary rows for the rigidity matrix that pin the given disk in place.

    Args:
        vIdx: The index of the disk to be pinned.
        disks: The list of all disks in the packing.

    Returns:
        The rows to be added to the rigidity matrix as a numpy array.
    """
    r1 = np.array([[1, 0, 0, 0] if i == vIdx else [0, 0, 0, 0] 
                   for i in range(len(disks) - 1)]).flatten()
    r2 = np.array([[0, 1, 0, 0] if i == vIdx else [0, 0, 0, 0] 
                   for i in range(len(disks) - 1)]).flatten()
    r3 = np.array([[0, 0, 1, 0] if i == vIdx else [0, 0, 0, 0] 
                   for i in range(len(disks) - 1)]).flatten()
    r4 = np.array([[0, 0, 0, 1] if i == vIdx else [0, 0, 0, 0] 
                   for i in range(len(disks) - 1)]).flatten()
    return np.array([r1, r2, r3, r4])

def rigidityMatrix(disks, edgeList, flipEdgeIdx, pinSet = None):
    """Builds the entire rigidity matrix for the packing, excluding the edge that is being
        flipped, and pins a few disks to prevent unwanted movements.
    
    Args:
        disks: The list of all disks in the packing.
        edgeList: The list of all edges in the packing.
        flipEdgeIdx: The index of the edge, in the edgeList, that is being flipped.
        pinSet: The set of disks to pin. (default = [0, 1, 2])
    
    Returns:
        The compleated rigidity matrix as a numpy array.
    """
    edgeRows = np.array([
        edgeRow(eIdx, disks, edgeList) 
        for eIdx in range(len(edgeList)) if eIdx != flipEdgeIdx
    ])
    if pinSet is None:
        pinSet = [0, 1, 2]
    pinRows0    = vertexPin(pinSet[0], disks)
    pinRows1    = vertexPin(pinSet[1], disks)
    pinRows2    = vertexPin(pinSet[2], disks)
    pinRowsOrig = vertexPin(len(disks) - 1, disks)
    return np.concatenate((edgeRows, pinRows0, pinRows1, pinRows2, pinRowsOrig))


def newtonStepOneDisk(disk, ns, deltaT):
    """Compleates one iteration of gradient decent on a single disk.
    
    Args:
        disk: the disk that is being moved.
        ns: The basis for the null space of the rigidity matrix.
        deltaT: The factor that determines the step size during gradient decent.
    
    Returns:
        The updated disk.
    """
    a = disk.a + deltaT * ns[0]
    b = disk.b + deltaT * ns[1]
    c = disk.c + deltaT * ns[2]
    d = disk.d + deltaT * ns[3]
    inv31 = 1.0# / inner_product31(a, b, c, d, a, b, c, d)
    return DiskS2(a * inv31, b * inv31, c * inv31, d * inv31)

def newtonStep(disks, edgeList, deltaT, ns, flipEdgeIdx, pinSet = None, direction = 1):
    """Compleates one iteration of gradient decent on the entire packing.
    
    Args:
        disks: The list of all disks in the packing.
        edgeList: The list of all edges in the packing.
        deltaT: The factor that determines the step size during gradient decent.
        ns: The null space to use for the gradient.
        flipEdgeIdx: The index of the edge, in the edgeList, that is being flipped.
        pinSet: The set of edges to pin in the packing.
        direction: The direction to move in.

    
    Returns:
        The array of updated disks.
    """
    R = rigidityMatrix(disks, edgeList, flipEdgeIdx, pinSet)
    ns = null_space(R).reshape(len(disks)-1, 4)
    # if prevNs is not None:
    #     posDot = np.dot(np.transpose(ns.reshape(64, 1)), prevNs.reshape(64, 1))[0][0]
    #     negDot = np.dot(np.transpose((-ns).reshape(64, 1)), prevNs.reshape(64, 1))[0][0]
    #     if negDot > posDot:
    #         ns = -ns
    # else:
    #     ns = ns * direction
    ns = ns * direction
    return [newtonStepOneDisk(disks[vIdx], ns[vIdx], deltaT) 
            for vIdx in range(len(disks) - 1)] + [disks[-1]]

def newtonAnimation(initialDisks, edgeList, deltaT, flipEdgeIdx, pinSet = None, direction = 1):
    """Runs gradient decent on a packing.
    
    Args:
        initialDisks: The list of all the disks in the packing before any gradient decent.
        edgeList: The list of all edges in the packing. 
        deltaT: The factor that determines the step size during gradient decent.
        flipEdgeIdx: The index of the edge, in the edgeList, that is being flipped.
        pinSet: The set of edges to pin in the packing.
        direction: The direction to move in.
    
    Returns:
        A list of lists of disks as gradient decent takes place.
    """
    animation = [initialDisks]
    prevNs = None
    # Instead of using an iteration count calculate the inversive distance along the flip edge
    # while it is less than a given threshold continue gradient decent.
    # With this method only one null space with the correct direction should be necessary.
    x, y = edgeList[flipEdgeIdx]
    px = tuple(initialDisks[x])
    py = tuple(initialDisks[y])
    invDist = px.inversiveDistTo(py)
    R = rigidityMatrix(initialDisks, edgeList, flipEdgeIdx, pinSet)
    ns = null_space(R).reshape(len(initialDisks)-1, 4)
    # Here I need to calculate the direction but im not sure how to do that.
    while invDist > 1.1 or invDist < 0.9:
        nextFrame = newtonStep(animation[-1], edgeList, deltaT, ns, flipEdgeIdx, pinSet, direction)
        px = tuple(nextFrame[x])
        py = tuple(nextFrame[y])
        invDist = px.inversiveDistTo(py)
        animation.append(nextFrame)
    return animation