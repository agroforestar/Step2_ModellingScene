from Plant import Plant

class Crop(Plant):
    def __init__(self, specie, Xcoord, Ycoord, eppo):
        super().__init__(specie, Xcoord, Ycoord, eppo)
        self.color = (125,125,0)

    def __repr__(self):
        return self.specie