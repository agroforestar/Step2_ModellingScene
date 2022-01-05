from Plant import Plant
from Tree import Tree

dictionnaryForm = {
    "circle": "Tree",
    "rectangle": "Crop"
}
dictionnaryColor = {
    "seagreen": "IUGRE", # code EPPO pour le noyer
    "yellow": "TRZAX" #code EPPO pour le blé tendre
}

def read(name):
    fichier = open(name, "r")
    plants = list()
    for line in fichier:
        element = line.strip("\n").split(";")
        form = element[0]# .split(" ")[0]
        color = "seagreen"#element[0].split(" ")[1]
        if(element[-1] != str(0)):
            if(dictionnaryForm[form] == "Crop"):
                plants.append(Plant(dictionnaryColor[color], element[1], element[2]))
            else:
                plants.append(Tree(dictionnaryColor[color], element[1], element[2]))
    print(type(plants[0]))
    return plants