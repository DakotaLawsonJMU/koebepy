from koebe.algorithms.tiling import *
from koebe.geometries.euclidean2 import PointE2
from koebe.algorithms.tutteEmbeddings import tutteEmbeddingE2
from koebe.graphics.svgMaker import SvgMaker
 
########################################
# Set up the finite subdivision rules
########################################

# The chair tiling only has one prototile
rules = TilingRules()
chair = rules.createPrototile("chair", [("A", PointE2(0,0)),
                                        ("B", PointE2(1,0)),
                                        ("C", PointE2(2,0)),
                                        ("D", PointE2(2,1)),
                                        ("E", PointE2(1,1)),
                                        ("F", PointE2(1,2)),
                                        ("G", PointE2(0,2)),
                                        ("H", PointE2(0,1))])

def chair_newverts(vDict):
    a = vDict["a"].point
    h = vDict["h"].point
    A = vDict["A"].point
    
    e0 = a - A
    e1 = h - A
    
    vDict["i"].point = A + 3 * e0 + e1
    vDict["j"].point = A + 2 * e0 + e1
    vDict["k"].point = A + e0 + e1
    vDict["l"].point = A + e0 + 2 * e1
    vDict["m"].point = A + e0 + 3 * e1

# Edges that need to be split
chair.addSplitEdgeRules(((("A","B"), ("a"), midp), 
                         (("B","C"), ("b"), midp), 
                         (("C","D"), ("c"), midp),
                         (("D","E"), ("d"), midp), 
                         (("E","F"), ("e"), midp), 
                         (("F","G"), ("f"), midp),
                         (("G","H"), ("g"), midp), 
                         (("H","A"), ("h"), midp)))

# New vertices to create
chair.addNewVertexRules(("i","j","k","l","m"))
chair.setNewVertexHandlerFn(chair_newverts)

# The subdivision subtiles: 
chair.addSubtile("chair", ("A", "a", "B", "j", "k", "l", "H", "h"))
chair.addSubtile("chair", ("G", "g", "H", "l", "m", "e", "F", "f"))
chair.addSubtile("chair", ("k", "j", "i", "d", "E", "e", "m", "l"))
chair.addSubtile("chair", ("C", "c", "D", "d", "i", "j", "B", "b"))

########################################
# Apply the rules
########################################

tiling = rules.generateTiling("chair", depth = 2)

# print("The level 4 chair tiling has")
# print(f"\t{len(tiling.verts)} vertices,")
# print(f"\t{len(tiling.edges)} edges, and")
# print(f"\t{len(tiling.faces)-1} tiles.")

# GeometricTilingViewer(tiling, 
#                       size=(800, 800), 
#                       shadedLevel=3, #colors in super tiles at a particular level
#                       style_fn=tileIdx_fill_fromList(["red", "green", "blue", "orange", "violet", "#30a"])
#                      ).show()

packing, _ = generateCirclePackingLayout(tiling)

svg = SvgMaker(packing)
svg.generateSVG("../ChairTiling.svg")

########################################
# Set up the finite subdivision rules
########################################

# The chair tiling only has one prototile
pent_rules = TilingRules()

pent = pent_rules.createPrototile("pent", tuple("ABCDE"))

# Edges that need to be split
pent.addSplitEdgeRules(((("A","B"), ("a", "b")), 
                        (("B","C"), ("c", "d")), 
                        (("C","D"), ("e", "f")),
                        (("D","E"), ("g", "h")), 
                        (("E","A"), ("i", "j"))))

# New vertices to create
pent.addNewVertexRules(("k"))

# The subdivision subtiles: 
pent.addSubtile("pent", tuple("Aabkj"))
pent.addSubtile("pent", tuple("Bcdkb"))
pent.addSubtile("pent", tuple("Cefkd"))
pent.addSubtile("pent", tuple("Dghkf"))
pent.addSubtile("pent", tuple("Eijkh"))

########################################
# Apply the rules
########################################

pent_tiling = pent_rules.generateTiling("pent", depth = 2)

pent_packing, _ = generateCirclePackingLayout(pent_tiling)

svg = SvgMaker(pent_packing)
svg.generateSVG("../ChairTilingPent.svg")