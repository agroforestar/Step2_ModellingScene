from PIL import Image, ImageDraw
import numpy as np


class Representation:

    def __init__(self, size):
        self.size = size
        self.image = Image.new("RGB", self.size)
        self.writeImage = ImageDraw.Draw(self.image)
        self.colorComposed = dict()

    def colorRepresentation(self, raster : np.array):
        """!
        @brief Compute a color for each pixel depending of the pixel content
        @param raster: source
        """
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if raster[i, j] == 0:
                    self.writeImage.point([i, j], (0,0,0))
                else:
                    if type(raster[i, j]) != list:
                        self.writeImage.point([i, j], raster[i, j].color)
                    else :
                        typeElement = list()
                        for element in raster[i,j]:
                            typeElement.append(type(element))
                        if str(set(typeElement)) in self.colorComposed.keys():
                            self.writeImage.point([i, j], self.colorComposed[str(set(typeElement))])
                        else:
                            self.colorComposed[str(set(typeElement))] = (62,62,255)
                            self.writeImage.point([i, j], self.colorComposed[str(set(typeElement))])

    def printRepresentation(self):
        """!
        @brief Display the raster with color in a image of 500*500
        """
        self.image.resize((500, 500), Image.NEAREST).show()

