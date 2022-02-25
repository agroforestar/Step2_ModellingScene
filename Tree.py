from Plant import Plant

class Tree(Plant):
    """!
    @class Object represents a tree (or a ponctual object)
    """
    def __init__(self, specie, Xcoord, Ycoord, eppo):
        super().__init__(specie, Xcoord, Ycoord, eppo)
        self.color = (0, 255, 0)

    def __repr__(self):
        return self.specie