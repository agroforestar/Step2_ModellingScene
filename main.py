### Librairies in the projects
from Parseur import *
from Crop import *
from Model import *
from Line import *

## Constante
# Hypothèse : 1 pixel = 1m
SCENE_SIZE = [20, 31]


## Methods
###Methods for the lines creation
def searchTree(origin: Tree, terrain: np.array) -> list:
    """
    Find the neighbors of a tree
    :param origin: tree of interest
    :param terrain: scene with other trees
    :return: a list of trees in the neighborhood of origin
    """
    buffer = 4
    listTree = []
    for i in range(max(0, origin.X - buffer), min(origin.X + buffer + 1, terrain.size[0])):
        for j in range(max(0, origin.Y - buffer), min(origin.Y + buffer + 1, terrain.size[1])):
            if type(terrain.raster[i, j]) == Tree and (i != origin.X or j != origin.Y):
                listTree.append(terrain.raster[i, j])
    return listTree


def isInLine(line: list, newTree: Tree) -> bool:
    """
    Test si l'arbre qu'on veut ajouté peut appartenir à la ligne (condition de distance et d'angle respectées)
    :param line: la ligne concernée
    :param newTree: l'arbre potentiel
    :return: Vrai si l'arbre appartient à la ligne, Faux sinon
    """
    temp_line = line.copy()
    temp_line.append(newTree)
    temp_line = sorted(temp_line, key=lambda element: element.Y)
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


def findLines(listTree: list, terrain: np.array) -> list[list]:
    """
    Retourne toutes les lignes formées par la arbres présents dans la scène
    :param listTree: arbres de la scène
    :param terrain: modèle contenant la scène
    :return: liste des lignes trouvées
    """
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
    print(lines)
    return lines


### Methods for graphe

####TODO : transfert in model class
def Affichage(graph: Graph):
    layout = graph.layout("kk")
    graph.vs["label"] = graph.vs["name"]
    color_dict = {"Tree": "blue", "IUGRE": "Forestgreen", "Crop": "yellow", "Line": "darkgreen", "Banc": "brown",
                  "Plant": "darkgreen", None: "grey"}
    graph.vs["color"] = [color_dict[name] for name in graph.vs["name"]]
    plot(graph, layout=layout)


###Methods for the crops creation
def expandCrop(crops: list, image: Model):
    """
    Pour chaque marqueurs culture, la méthodes cherches les pixels adjacants et ajoutent leur appartenance à la culture
    Recommence pour chaque pixel appartenant à la culture
    :param crops: marqueurs de culture
    :param image: modele contenant la scène (cf class Model)
    """
    for c in crops:
        voisin = [[c.X - 1, c.Y - 1], [c.X, c.Y - 1], [c.X + 1, c.Y - 1],
                  [c.X - 1, c.Y], [c.X, c.Y], [c.X + 1, c.Y],
                  [c.X - 1, c.Y + 1], [c.X, c.Y + 1], [c.X + 1, c.Y + 1]]
        while len(voisin) > 0:
            v = voisin.pop()
            if image.raster[v[0], v[1]] == 0:
                image.raster[v[0], v[1]] = c
                new = getVoisins(v)
                for n in new:
                    voisin.append(n)


def getVoisins(xy) -> list:
    """
    Retourne les voisins d'un pixel donné
    :param xy: coordonnées x et y
    :return: liste des voisins
    """
    startPosX = max(xy[0] - 1, 0)

    startPosY = max(xy[1] - 1, 0)

    endPosX = min(xy[0] + 1, SCENE_SIZE[0])

    endPosY = min(xy[1] + 1, SCENE_SIZE[1])

    voisin = []
    for rowNum in range(startPosX, endPosX):
        for colNum in range(startPosY, endPosY):
            voisin.append([rowNum, colNum])
    return voisin

## Main
# command : python3 main.py InputFile.txt
if __name__ == '__main__':
    elementInScene = readInputFile(sys.argv[1])
    image = Model(SCENE_SIZE)

    nbElement = len(elementInScene)
    # Import elements in model (raster)
    for i in range(nbElement):
        image.addPointInRaster(elementInScene[i])
    ####Traitement des lignes
    lines = findLines([element for element in elementInScene if type(element) == Tree], image)
    for line in lines:
        line = Line(line)
        image.addLineInRaster(line)
    ###Traitement des culture
    expandCrop([element for element in elementInScene if type(element) == Crop], image)
    image.visual.colorRepresentation(image.raster)
    print(image)

    ###### Création graphe
    image.createGraph()
    Affichage(image.g)
