"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-14 14:18:34
Description: 
"""


class Hexa:
    def __init__(self, q, r, owner=None):
        self.q = q  # TODO is this really column?
        self.r = r  # TODO is this really row?  I am not sure. You check.
        self.owner = owner  # TODO not yet fully decided to delete this

    # TODO .join() us faster
    def __repr__(self):
        return "(" + str(self.q) + ", " + str(self.r) + ")"

    def __eq__(self, other):
        return isinstance(other, self.__class__) & (self.q == other.q) & (self.r == other.r)

    def __hash__(self):
        return hash((self.q, self.r))

    @staticmethod
    def read_coordinates(pieces_coordinates, owner):
        """return list of hexa after read list of coordinates"""
        hexas = []

        for q, y in pieces_coordinates:
            hexas.append(Hexa(q, r, owner))

        return hexas

    def get_all_movable_hexa(self, other_pieces=[]):
        movable_hexa = []
        # TODO implement this not return hexa out of board
        return movable_hexa

    # TODO return hexa if not outside board use Board.BOUND else None
    def _left(self):
        return None
