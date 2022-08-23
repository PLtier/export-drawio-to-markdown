import zlib
import sys
import base64
import xml.etree.ElementTree as ET
from urllib.parse import unquote
from functools import reduce

if(len(sys.argv) != 3):
    print("Not sufficient amount of arguments. Minimaly provide input file")
else:
    inputPath = sys.argv[1]
    outputPath = sys.argv[2]


tree = ET.parse(inputPath)

data = base64.b64decode(tree.find('diagram').text)
xml = zlib.decompress(data, wbits=-15)

xml = xml.decode('utf-8')

xml = unquote(xml)
xml = ET.fromstring(xml)
root = xml[0]


edges = {}
entities = {}
valuesWithIdentation = []


def addEdge(source, target, where=edges):
    if source not in where:
        where[source] = []
    where[source].append(target)


def addEntity(_id, value, where):
    where[_id] = value


for child in root:
    value = child.attrib.get('value')
    ID = child.attrib.get('id')
    if value:
        addEntity(ID, value, entities)
    elif value == '':
        source = child.attrib.get('source')
        target = child.attrib.get('target')
        addEdge(source, target, edges)


def goDeepGraph(graph, values, man, parent=None, lvl=0):
    valuesWithIdentation.append((values[man], lvl))
    print(values[man], lvl)
    lvl += 1
    if (man in graph):
        targets = graph[man]
        for target in targets:
            goDeepGraph(graph, values, target, man, lvl)


def findMasterEntity(graph):
    masterDescendants = set(reduce(lambda a, b: a+b, list(graph.values())))
    for parent in graph.keys():
        if (parent not in masterDescendants):
            return parent


master = findMasterEntity(edges)
# print(master)
goDeepGraph(edges, entities, master)
# print(valuesWithIdentation)


def convertIdentationLevelToChars(data):
    return [(value, identationLevel*'\t') for value, identationLevel in data]


with open(outputPath, 'w', encoding="utf-8") as file:
    data = convertIdentationLevelToChars(valuesWithIdentation)
    # print(data)
    for value, identationChars in data:
        file.write(f"{identationChars}- {value}\n")
