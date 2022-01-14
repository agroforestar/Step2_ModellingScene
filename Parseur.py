from Plant import Plant
from Tree import Tree
from Crop import Crop
from webcolors import rgb_to_name, CSS3_HEX_TO_NAMES, hex_to_rgb  # python3 -m pip install webcolors
from scipy.spatial import KDTree
from collections import defaultdict


dictionnaryForm = {
    "circle": "Tree",
    "rectangle": "Crop"
}
dictionnaryForm = defaultdict(lambda: "Plant", dictionnaryForm)
dictionnaryColor = {
    "seagreen": "IUGRE", # code EPPO pour le noyer
    "yellow": "TRZAX" #code EPPO pour le blé tendre
}
dictionnaryColor= defaultdict(lambda: "Unknow", dictionnaryColor)


def closest_colour(requested_colour):
        min_colours = {}
        for key, name in CSS3_HEX_TO_NAMES.items():
            r_c, g_c, b_c = hex_to_rgb(key)
            rd = (r_c - requested_colour[0]) ** 2
            gd = (g_c - requested_colour[1]) ** 2
            bd = (b_c - requested_colour[2]) ** 2
            min_colours[(rd + gd + bd)] = name
        return min_colours[min(min_colours.keys())]


def convert_rgb_to_names(rgb_tuple):
        try:
            name = rgb_to_name((int(rgb_tuple[2]),int(rgb_tuple[1]),int(rgb_tuple[0])))
        except ValueError:
            name = closest_colour((int(rgb_tuple[2]),int(rgb_tuple[1]),int(rgb_tuple[0])))
        return name

def readInputFile(name):
    fichier = open(name, "r")
    plants = list()
    for line in fichier:
        element = line.strip("\n").split(";")
        form = element[0]# .split(" ")[0]
        color = eval(element[1])#element[0].split(" ")[1]
        color = convert_rgb_to_names(color[:3])
        if(dictionnaryForm[form] == "Crop"):
                plants.append(Crop(dictionnaryColor[color], element[2], element[3]))
        else:
                plants.append(Tree(dictionnaryColor[color], element[2], element[3]))
    return plants