class Plant:
    """!
    @class Object represents a plant
    """
    def __init__(self, specie, Xcoord, Ycoord, eppo):
        self.specie = specie
        self.X = int(Xcoord)
        self.Y = int(Ycoord)
        self.color = (0,0,0)
        self.EPPO = eppo

    def getColor(self):
        return self.color

    def __repr__(self):
        return repr((self.specie,self.X, self.Y))