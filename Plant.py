class Plant:

    def __init__(self, specie, Xcoord, Ycoord):
        self.specie = specie
        self.X = int(Xcoord)
        self.Y = int(Ycoord)

    def __repr__(self):
        return repr((self.specie,self.X, self.Y))