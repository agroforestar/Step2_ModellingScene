from igraph import *

from Representation import *
from Line import *
from Tree import *


class Model:
    def __init__(self,size):
        self.size = size
        self.raster = np.zeros(self.size, dtype=object)
        self.visual = Representation(self.size)
        self.g = Graph()


    def bresenhamAlgorithm(self, x1, x2, y1, y2, newObject):
        """
        Coloris un pixel s'il est dans le tracé de la ligne entre deux points
        Pour plus de détail sur l'algorithme : https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm
        :param x1: coordonée x du premier point
        :param x2: coordonée x du deuxième point
        :param y1: coordonée y du premier point
        :param y2: coordonée y du deuxième point
        :param newObject: la ligne auxquelle appartiennent les points
        """
        m_new = 2 * (y2 - y1)
        slope_error_new = m_new - (x2 - x1)
        y = y1
        for x in range(x1, x2 + 1):
            self.raster[x, y] = newObject
            # Add slope to increment angle formed
            slope_error_new = slope_error_new + m_new
            # Slope error reached limit, time to
            # increment y and update slope error.
            if (slope_error_new >= 0):
                y = y + 1
                slope_error_new = slope_error_new - 2 * (x2 - x1)

    def addLineInRaster(self, newObject: Line):
        """
        Ajoute une ligne à la représentation raster de la scène
        :param newObject: la ligne à ajouter
        """
        points = sorted(newObject.points, key=lambda k: [k.X, k.Y])
        for i in range(len(points) - 1):
            x1 = points[i].X
            y1 = points[i].Y
            x2 = points[i + 1].X
            y2 = points[i + 1].Y
            if x1 == x2:  # cas ligne verticale
                for y in range(y1, y2 + 1):
                    if self.raster[x1, y] !=0:
                        if type(self.raster[x1, y]) != list:
                            self.raster[x1, y] = [self.raster[x1, y], newObject]
                        if type(newObject) not in [type(element) for element in set(self.raster[x1, y])]:
                            self.raster[x1, y].append(newObject)
                    else:
                        self.raster[x1, y] = newObject
            else:
                self.bresenhamAlgorithm(x1, x2, y1, y2, newObject)

    def addPointInRaster(self, newObject):
        """
        Ajoute un objet dont la taille correspond à un pixel à la représentation raster de la scène
        :param newObject: l'objet à ajouter
        """
        self.raster[newObject.X, newObject.Y] = newObject

    def getVoisins(self, xy, rayon :int) -> list:
        """
        Retourne les voisins d'un pixel donné
        :param xy: coordonnées x et y
        :return: liste des voisins
        """
        startPosX = max(xy[0] - 1, 0)
        startPosY = max(xy[1] - 1, 0)
        endPosX = min(xy[0] + rayon+1, self.size[0])
        endPosY = min(xy[1] +rayon +1, self.size[1])

        voisin = []
        for rowNum in range(startPosX,endPosX) :
            for colNum in range(startPosY,endPosY):
                if rowNum == xy[0] and colNum== xy[1]:
                    pass
                else:
                    if type(self.raster[rowNum, colNum]) != int:
                        if type(self.raster[rowNum, colNum]) !=list:
                            voisin.append(self.raster[rowNum, colNum])
                        else:
                            for element in self.raster[rowNum, colNum]:
                                voisin.append(element)
        return voisin

    def getAllelementsInScene(self):
        elements = list()
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.raster[i, j] != 0:
                    if type(self.raster[i, j]) != list :
                        if not elements.__contains__(self.raster[i, j]) :
                            elements.append(self.raster[i, j])
                    else:
                        for element in self.raster[i, j]:
                            if not elements.__contains__(element):
                                elements.append(element)
        return elements

## Graph methods
    def createGraph(self):
        self.createVertices()
        self.createEdges()

    def createVertices(self):
        inScene = self.getAllelementsInScene()
        for element in inScene:
            self.addVertice({"name": repr(element), "x": element.X, "y": element.Y})

    def addVertice(self, attributes : dict):
        if not self.has_node(attributes):
            name = attributes.pop('name')
            self.g.add_vertices(name, attributes)

    def createEdges(self):
        for vertice in self.g.vs:
            # relation adjacecence
            self.AdjancenceRelation(vertice)
            # relation inclusion
            self.InclusionRelation(vertice)

    def AdjancenceRelation(self, vertice):
        voisins = self.getVoisins(([vertice["x"], vertice["y"]]), 1)
        for v in voisins:
            if v != 0:
                if (vertice["name"] == "Tree" and type(v) == Line) or (vertice["name"] == "Line" and type(v) == Tree): # Tree in line ar not adjacent to their line
                    pass
                elif vertice["name"] == str(v) and vertice["x"] == v.X and vertice["y"] == v.Y: # identical node
                    pass
                else:
                    dest = self.g.vs.find(x=v.X, y=v.Y)
                    self.g.add_edges([(vertice, dest)], {"adjacene": True})

    def InclusionRelation(self,vertice):
        voisins = set(self.getVoisins(([vertice["x"], vertice["y"]]), 1))
        for v in voisins:
            if(vertice["name"] == "Tree" and type(v) == Line ):
                dest = self.g.vs.find(x=v.X, y=v.Y)
                self.g.add_edges([(vertice, dest)], {"inclusion": True})

    def has_node(self, attributes):
        if self.g.vcount() >0:
            rep = self.g.vs.select(name_eq=attributes["name"], x_eq= attributes["x"], y_eq= attributes["y"])
            if len(rep) >0 :
                return True
            else:
                return False

    def exportScene(self):
        f = open("output.txt", "w")
        inScene = self.getAllelementsInScene()
        for e in inScene:
            f.write(repr(e)+";"+str(e.X)+";"+str(e.Y)+"\n")
        f.close()

    def __repr__(self):
        self.visual.printRepresentation()
        return ""