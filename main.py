# This is a sample Python script.
import math
import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from igraph import *

from Parseur import *
from Line import *
from Crop import *
from PIL import Image, ImageShow, ImageDraw, ImageColor


##
SCENE_SIZE = [15, 15]
def searchTree(origin: Tree, terrain: np.ndarray) -> list:
    """
    Find the neighbors of a tree
    :param origin: tree of interest
    :param terrain: scene with other trees
    :return: a list of trees in the neighborhood of origin
    """
    buffer = 3
    listTree = []
    for i in range(max(0, origin.X - buffer), min(origin.X + buffer + 1, terrain.shape[1])):
        for j in range(max(0, origin.Y - buffer), min(origin.Y + buffer + 1, terrain.shape[1])):
            if type(terrain[i, j]) == Tree and (i != origin.X or j != origin.Y):
                listTree.append(terrain[i, j])
    return listTree


def createLine(origin: Tree, terrain: np.ndarray, traitedTree: list, voisins=None):
    if voisins == []:
        return origin
    else:
        traitedTree.append(origin)
        voisins = searchTree(origin, terrain)
        createLine(voisins)


def isInLine(line: list, newTree: Tree) -> bool:
    temp_line = line.copy()
    temp_line.append(newTree)
    temp_line = sorted(temp_line, key=lambda element: element.X)
    vector_1 = [temp_line[(len(line) / 2).__floor__()].X - temp_line[0].X,
                line[(len(line) / 2).__floor__()].Y - temp_line[0].Y]
    vector_2 = [temp_line[-1].X - temp_line[(len(line) / 2).__floor__()].X,
                temp_line[-1].Y - temp_line[(len(line) / 2).__floor__()].Y]
    unit_vector_1 = vector_1 / np.linalg.norm(vector_1)
    unit_vector_2 = vector_2 / np.linalg.norm(vector_2)

    dot_product = np.dot(unit_vector_1, unit_vector_2)

    angle = math.degrees(np.arccos(dot_product))
    if angle < 25:
        return True
    else:
        return False


def findLines(listTree: list, terrain: np.ndarray) -> list[list]:
    traitedTree = list()
    lines = list()
    for tree in listTree:
        traitedTree.append(tree)
        voisins = searchTree(tree, terrain)
        for voisin in voisins:
            added = False
            voisinTraited = list()
            if voisin not in voisinTraited:
                voisinTraited.append(voisin)
                for line in lines:
                    if (tree in line) and (voisin in line):
                        added = True
                    elif (len(line) > 1):
                        if tree in line:
                            if isInLine(line, voisin):
                                line.append(voisin)
                                added = True
                        elif voisin in line:
                            if isInLine(line, tree):
                                line.append(voisin)
                                added = True
                    elif (len(line) == 1) and (tree in line):
                        line.append(voisin)
                        added = True
                if (not added):
                    lines.append([tree, voisin])
    return lines


def Affichage(graph: Graph):
    graph.vs["label"] = graph.vs["name"]
    color_dict = {"Tree": "blue", "IUGRE": "Forestgreen", "Crop": "yellow", "Line": "darkgreen", "Banc": "brown",
                  "Plant": "darkgreen", None: "grey"}
    graph.vs["color"] = [color_dict[name] for name in graph.vs["name"]]
    plot(graph, bbox=(300, 300), margin=20)


def Createscene(scene: list):
    visu = Image.new("RGB", SCENE_SIZE)
    modify = ImageDraw.Draw(visu)
    for element in scene:
        if type(element) == Tree:
            modify.point([element.X, element.Y], (0, 128, 0))
        elif type(element) == Line:
            element.points = sorted(element.points, key=lambda k: [k.X, k.Y])
            modify.line([(element.points[0].X, element.points[0].Y), (element.points[-1].X, element.points[-1].Y)])
        else:
            modify.point([element.X, element.Y], (128, 0, 0))
    visu.resize((500, 500), Image.NEAREST).show()


def drawLine(line : Line, image: ImageDraw):
    points = sorted(tuple(line.points), key=lambda k: [k.X, k.Y])
    for i in range(0, len(points)-1):
        image.line([(points[i].X,points[i].Y ), (points[i+1].X,points[i+1].Y )], (125,125,125), 1)
        image.point((points[i].X,points[i].Y ),(0,125,125) )


def expandCrop(crops : list, image, imageW: ImageDraw):
    for c in crops:
        voisin = [[c.X-1, c.Y-1],[c.X, c.Y-1],[c.X+1, c.Y-1],
                  [c.X-1, c.Y],  [c.X, c.Y],  [c.X+1, c.Y],
                  [c.X-1, c.Y+1],[c.X, c.Y+1],[c.X+1, c.Y+1]]
        while len(voisin) >0:
            v = voisin.pop()
            if image.getpixel((v[0], v[1])) == (0,0,0):
                color(v, (125, 125, 0), imageW)
                new = getVoisins(v)
                for n in new:
                    voisin.append(n)


def getVoisins(xy):
    voisin = []
    if xy[0] >0:
        voisin.append([xy[0]-1, xy[1]])
        if xy[0]<SCENE_SIZE[0]-1:
            voisin.append([xy[0]+1, xy[1]])
        if xy[1]<SCENE_SIZE[1]-1:
            voisin.append([xy[0]-1, xy[1]+1])
    if xy[0] >0 and xy[1] >0:
        voisin.append([xy[0] - 1, xy[1]- 1])
        if xy[0] < SCENE_SIZE[0]-1:
           voisin.append([xy[0] + 1, xy[1] - 1])
        if xy[0] < SCENE_SIZE[0]-1 and xy[1]< SCENE_SIZE[1]-1:
            voisin.append( [xy[0]+1, xy[1]+1])
    if xy[1] >0:
        voisin.append([xy[0] , xy[1]-1])
        if xy[1]<SCENE_SIZE[1]-1:
            voisin.append([xy[0], xy[1]+1])

    return voisin



def color(xy : tuple, color, image : ImageDraw):
    image.point(xy, color)

if __name__ == '__main__':
    scene = read("data.txt") #D:/Mes_Documents/code/OpenCVc++/data.txt
    image = np.ndarray(SCENE_SIZE, dtype=Plant)
    model = Image.new("RGB", SCENE_SIZE)
    modelWrite = ImageDraw.Draw(model)
    colorDict = {"Tree": (0,255,0)}
    listTree = list()
    #
    for i in range(len(scene)):
        if type(scene[i]) == Tree:
            image[scene[i].X, scene[i].Y] = scene[i]
            modelWrite.point([scene[i].X, scene[i].Y],(0, 255, 0))
            listTree.append(scene[i])
        else:
            image[scene[i].X, scene[i].Y] = scene[i]
    lines = findLines(listTree, image)


    for line in lines:
        line = Line(line)
        scene.append(line)
        drawLine(line, modelWrite)
    model.resize((500, 500), Image.NEAREST).show()
    expandCrop([element for element in scene if type(element) == Crop], model, modelWrite)
    model.resize((500, 500), Image.NEAREST).show()
    print("end")
    # Createscene(scene)
    #
    # ###### Création graphe
    # g = Graph()
    # lines = [element for element in scene if type(element) == Line]
    # g.add_vertices(len(scene))
    # g.vs["name"] = "Line"
    # for l in range(len(lines)):
    #     index = [g.vcount(), g.vcount() + len(lines[l].points)]
    #     g.add_vertices(len(lines[l].points))
    #
    #     for i in range(index[0], index[1]):
    #         print(l, i)
    #         g.add_edge(l, i)
    # Affichage(g)
