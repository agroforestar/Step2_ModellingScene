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
        """!
        @brief Apply the Bresenham algorithm to draw the segment ([(x1, y1), (x2, y2)]) in the raster (see https://en.wikipedia.org/wiki/Bresenham%27s_line_algorithm )
        @param x1: X coord of the first point
        @param x2: X coord of the second point
        @param y1: Y coord of the first point
        @param y2: Y coord of the second point
        @param newObject: line where from the points
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
        """!
        @brief Add a line on the raster
        @param newObject: the new line
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
        """!
        @brief Add an object with a size of one pixel on the raster
        @param newObject: the new object
        """
        self.raster[newObject.X, newObject.Y] = newObject

    def getVoisins(self, xy, rayon :int) -> list:
        """!
        @brief Retour the neighbors of the point
        @param xy: X and Y coord
        @return: neighbors list
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
        """!
        Get all differents entities in the raster
        @return: a list of entities
        """
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
        """!
        @brief Create graph that match to raster
        """
        self.createVertices()
        self.createEdges()

    def createVertices(self):
        """!
        @brief Create the vertices of the graph
        """
        inScene = self.getAllelementsInScene()
        for element in inScene:
            self.addVertice({"name": repr(element), "x": element.X, "y": element.Y})

    def addVertice(self, attributes : dict):
        """!
        Add a vertice with its attribute to the graph
        @param attributes: dictionnary of attributes
        """
        if not self.has_node(attributes):
            name = attributes.pop('name')
            self.g.add_vertices(name, attributes)

    def createEdges(self):
        """!
        @brief Create the edges of the graphs
        @details A edge represents to a relation between two elements. Here, they are "adjacence" and "inclusion" relation
        """
        for vertice in self.g.vs:
            # relation adjacecence
            self.AdjancenceRelation(vertice)
            # relation inclusion
            self.InclusionRelation(vertice)

    def AdjancenceRelation(self, vertice):
        """!
        @brief Create edge when two elements are neigbors
        @param vertice: vertice tested
        """
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
        """!
        @brief Create edge when one element is include in onother
        @param vertice: vertice tested
        """
        voisins = set(self.getVoisins(([vertice["x"], vertice["y"]]), 1))
        for v in voisins:
            if(vertice["name"] == "Tree" and type(v) == Line ):
                dest = self.g.vs.find(x=v.X, y=v.Y)
                self.g.add_edges([(vertice, dest)], {"inclusion": True})

    def has_node(self, attributes):
        """!
        @brief Test if the graph has a node with specific attributes (only name, x, y)
        @param attributes: attributes tested (name, x, y)
        @return: Yes if a node exist, otherwise no
        """
        if self.g.vcount() >0:
            rep = self.g.vs.select(name_eq=attributes["name"], x_eq= attributes["x"], y_eq= attributes["y"])
            if len(rep) >0 :
                return True
            else:
                return False

    def exportScene(self):
        """!
        @brief Export the raster on a text file
        """
        f = open("output.txt", "w")
        inScene = self.getAllelementsInScene()
        for e in inScene:
            print(type(e))
            if issubclass(type(e), Plant):
                f.write(e.EPPO+";"+str(e.X)+";"+str(e.Y)+"\n")
            else:
                f.write(repr(e) + ";" + str(e.X) + ";" + str(e.Y) + "\n")
        f.close()

    def __repr__(self):
        self.visual.printRepresentation()
        return ""