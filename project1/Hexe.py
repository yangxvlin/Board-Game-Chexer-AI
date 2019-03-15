"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-14 14:18:34
Description: 
"""
from Board import Board


class Hexe:
    def __init__(self, q, r, owner=None):
        self.q = q  # TODO is this really column?
        self.r = r  # TODO is this really row?  I am not sure. You check.
        # an additional note
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
        """return list of hexe after read list of coordinates"""
        hexes = []

        for q, y in pieces_coordinates:
            hexes.append(Hexe(q, r, owner))

        return hexes

    def get_all_movable_hexe(self, other_pieces=()):
        movable_hexe = []
        # TODO implement this not return hexe out of board

        movable_hexe.extend(self._move(other_pieces))

        return movable_hexe

    def _is_in_board(self):
        return (abs(self.q) <= Board.BOARD_BOUND) & (self.r <= Board.BOARD_BOUND)

    def _move(self, other_pieces=()):
        moves = []

        return moves

    def _jump(self, other_pieces=()):
        jumps = []

        return jumps

    def _exit(self, other_pieces=()):
        exits = []

        return exits

    def _left(self):
        return Hexe(self.q, self.r, self.owner)
