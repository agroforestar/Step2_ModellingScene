from igraph import *

from Representation import *
from Line import *


class Model:
    def __init__(self,size):
        self.size = size
        self.raster = np.zeros(self.size, dtype=object)
        self.visual = Representation(self.size)
        self.g = Graph()


    def bresenhamAlgorithm(self, x1, x2, y1, y2, newObject):
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
        self.raster[newObject.X, newObject.Y] = newObject

    def createGraph(self):
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.raster[i, j] != 0:
                    if type(self.raster[i, j]) != list:
                        self.addVertice({"name": repr(self.raster[i, j]), "x": self.raster[i, j].X, "y": self.raster[i, j].Y})
                    else:
                        for element in self.raster[i, j]:
                            self.addVertice({"name":repr(element), "x":element.X, "y": element.Y})
        print(self.g.vs.get_attribute_values("name"))

    def addVertice(self, attributes : dict):
        if not self.has_node(attributes):
            name = attributes.pop('name')
            self.g.add_vertices(name, attributes)

    def has_node(self, attributes):
        try:
            self.g.vs.find(name=attributes["name"], x= attributes['x'], y= attributes['y'])
        except:
            return False
        return True

    def __repr__(self):
        self.visual.printRepresentation()
        return ""