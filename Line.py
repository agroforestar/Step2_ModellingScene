import numpy as np

class Line:
    """!
    @class Object reprensents a line of something (or linear object)
    """
    def __init__(self, listPoints):
        self.X = round(np.mean([c.X for c in listPoints]))
        self.Y = round(np.mean([c.Y for c in listPoints]))
        self.witdh = 2
        vector = [listPoints[-1].X - listPoints[0].X,
                listPoints[-1].Y - listPoints[0].Y]
        self.length = vector / np.linalg.norm(vector)
        self.points = listPoints
        self.color = (62,62,62)

    def __repr__(self):
        return "Line"