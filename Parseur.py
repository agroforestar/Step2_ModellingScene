from Plant import Plant
from Tree import Tree
from Crop import Crop
from webcolors import rgb_to_name, CSS3_HEX_TO_NAMES, hex_to_rgb  # python3 -m pip install webcolors
from scipy.spatial import KDTree
from collections import defaultdict

import json

class Parseur:
    """!
    @class Class in charge to read/write data and to memorize config parameters
    """

    def __init__(self, data_path, config_path):
        self.config_Path = config_path
        self.data_Path = data_path

    def getColor(self, color_tested):
        """!
        @brief Get the color name from a list of color thanks to a minamal distance calculate with euclidian distance
        @aram color_tested: color tested (format BGR)
        @return: name of the color
        """
        min_colours = {}
        for color, name in self.color.items():
            color = color.strip("(").strip(")").split(',')
            b_c = int(color[0])
            g_c = int(color[1])
            r_c = int(color[2])
            rd = (r_c - color_tested[0]) ** 2
            gd = (g_c - color_tested[1]) ** 2
            bd = (b_c - color_tested[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]

    def readInputFile(self):
        """!
        @brief Read the data file with the elements of the scene
        @return: list of the elements
        """
        fichier = open(self.config_Path)
        config = json.load(fichier)

        fichier = open(self.data_Path, "r")

        plants = list()
        for line in fichier:
            element = line.strip("\n").split(";")
            form = element[0]
            color = eval(element[1])
            color = self.getColor(color[:3])
            element_name = form+" "+color
            if element_name in config["link"].keys():
                code_EPPO = config["link"][element_name]
                if code_EPPO in self.tree:
                    plants.append(Tree(self.tree[code_EPPO], element[2], element[3]))
                elif code_EPPO in self.crop:
                    plants.append(Crop(self.crop[code_EPPO], element[2], element[3]))
            else:
                    plants.append(Plant("Unknow", element[2], element[3]))
        fichier.close()
        return plants


    def initialisation(self):
        """!
        @brief Initialize the program with the config file
        @return: size of the scene
        """
        fichier = open(self.config_Path)
        data = json.load(fichier)
        size = data["Scene_size"]
        self.color = data["color"]
        self.tree = data["plants"]["tree"]
        self.crop = data["plants"]["crop"]
        fichier.close()
        return size
