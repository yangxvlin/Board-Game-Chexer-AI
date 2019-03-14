"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-14 14:18:34
Description: 
"""

# each hexa contains some coordinates
# x, y, z for cube coordinates
# two of x, y, z for axial coordinate

# using axial coordinate for storing


class Hexa:
    def __init__(self, q, r):
        self.q = q
        self.r = r

    # TODO .join() us faster
    def __repr__(self):
        return "(" + str(self.q) + ", " + str(self.r) + ")"

    def __eq__(self, other):
        return isinstance(other, self.__class__) & (self.q == other.q) & (self.r == other.r)

    def __hash__(self):
        return hash((self.q, self.r))

    def get_all_movable_hexa(self):
        movable_hexa = []
        # TODO implement this
        return movable_hexa
