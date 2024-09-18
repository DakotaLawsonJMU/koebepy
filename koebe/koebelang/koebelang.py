import sys
import re
from koebe.algorithms.tiling import *
from koebe.geometries.euclidean2 import PointE2
from koebe.algorithms.tutteEmbeddings import tutteEmbeddingE2
from koebe.graphics.svgMaker import SvgMaker

# Mainly for future use if we decide to add any command line arguments
def useage():
    print("koebelang.py <koebelang file>")

# I would like to at least print out which line the error is on but that is for later me Errors should prob also be a exception but im not sure how those work in python yet
def syntaxErr(line):
    print("There is a syntax error in the following line: <" + line + ">")

# This reads the data in from the given file and removes any comments and leading white space from the file
def readData(f):
    data = f.readlines()
    data = [re.sub(r'^\s+|#.*|\n', '', line, flags=re.MULTILINE) for line in data]
    data = [string for string in data if string.strip()]
    return data

def process(data):
    prototiles = {}
    outputData = []
    i = 0
    while i < len(data):
        line = data[i]
        if line.startswith("prototile "):
            prototile_name = re.sub(r'prototile\s*', '', line)
            prototiles[prototile_name] = []
            outputData.append(line)
        elif line.startswith("let "):
            workingPrototile = re.split(r'\s+', line)[1]
            if workingPrototile in prototiles:
                matches = re.findall(r'\((.*?)\)', line)
                verts = [item.strip() for match in matches for item in match.split(',')]
                prototiles[workingPrototile].append(verts)
                outputData.append((workingPrototile, verts))
            else:
                syntaxErr(line)
        elif line.startswith("create "):
            workingLine = re.sub(r'create\s*', '', line)
            if workingLine.startswith("verticies"):
                workingLine = re.sub(r'verticies\s*for\s*', '', workingLine)
                prototile = re.split(r'\s+', workingLine)[0]
                if prototile not in prototiles:
                    syntaxErr(line)
                    return
                subVerts = []
                for j in range(i + 1, len(data)):
                    if data[j] == '}':
                        i = j
                        break
                    if data[j].endswith('}'):
                        subVerts.append(re.sub('}', '', data[j]))
                        i = j
                        break
                    subVerts.append(data[j])
                prototiles[prototile].append(subVerts)
            elif workingLine.startswith("subtiles "):
                workingLine = re.sub(r'subtiles\s*for\s*', '', workingLine)
                prototile = re.split(r'\s+', workingLine)[0]
                if prototile not in prototiles:
                    syntaxErr(line)
                    return
                subtiles = []
                for j in range(i + 1, len(data)):
                    if data[j] == '}':
                        i = j
                        break
                    matches = re.findall(r'\((.*?)\)', data[j])
                    subtiles.append([item.strip() for match in matches for item in match.split(',')])
                    subtiles.append(re.sub('}', '', data[j].split()[-1]))
                    if data[j].endswith('}'):
                        i = j
                        break
                prototiles[prototile].append(subtiles)
            elif workingLine.startswith("circle"):
                matches = re.findall(r'\((.*?)\)', line)
                outputData = [item.strip() for match in matches for item in match.split(',')]
            else:
                syntaxErr(line)
        else:
            syntaxErr(line)
        i += 1
    return prototiles, outputData

# This uses the information stored in the data structure to run all of the code necessary to make it work
def run(data, outputData):
    rules = TilingRules()
    for prototile in data:
        currTile = rules.createPrototile(prototile, data[prototile][0])

        splitEdgeRules = []
        newVertex = []
        for item in data[prototile][1]:
            parts = item.split()
            if 'splits' in parts:
                verts = []
                for vertex in parts:
                    if vertex == 'splits': break
                    if vertex != 'and': verts.append(vertex)
                splitEdge = (parts[-1][0], parts[-1][1])
                splitEdgeRules.append((splitEdge, verts))
            elif 'vertex' in parts:
                newVertex.append(parts[2])
        currTile.addSplitEdgeRules(splitEdgeRules)
        currTile.addNewVertexRules(newVertex)
        
        i = 0
        while i < len(data[prototile][-1]):
            currTile.addSubtile(data[prototile][-1][i + 1], data[prototile][-1][i])
            i += 2

    tiling = rules.generateTiling(outputData[2], depth = int(outputData[1]))
    packing, _ = generateCirclePackingLayout(tiling)

    svg = SvgMaker(packing)
    svg.generateSVG(outputData[0])

def main():
    if (len(sys.argv) != 2):
        useage()
    else:
        f = open(sys.argv[1], 'r')
        if (not f.readable()): 
            useage()
        data = readData(f)
        processedData, outputData = process(data)
        run(processedData, outputData)

main()

# Keywords:
# prototile <some name>
# let <name of prototile> be (comma seperated list of strings)
# create verticies for <name of prototile> ( in here we have splits and new vertex )
# create subtiles for <name of prototile>  ( In here we define subtiles using new subtile(comma seperated list of verticies))
# create circle packing (<file save location>, depth, root prototile)
