"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-14 14:18:34
Description: 
"""


class Hexe:
    def __init__(self, q, r, owner=None):
        self.q = q
        self.r = r
        # an additional note
        self.owner = owner  # NOTE: needed for identify kill information

    def __repr__(self):
        return "".join(["(", str(self.q), ", ", str(self.r), ")"])

    def __eq__(self, other):
        return isinstance(other, self.__class__) & (self.q == other.q) & (self.r == other.r)

    def __hash__(self):
        return hash((self.q, self.r))

    def __add__(self, other):
        return Hexe(self.q + other.q, self.r + other.r, self.owner)

    @staticmethod
    def read_coordinates(pieces_coordinates, owner):
        """return list of hexe after read list of coordinates"""
        hexes = []

        for q, r in pieces_coordinates:
            hexes.append(Hexe(q, r, owner))

        return hexes

    def get_all_possible_actions(self, other_pieces=()):
        possible_actions = []  # TODO update: player player ordering

        move = 0
        jump = 1
        exit_action_id = 2

        from Action import Action
        jump_delta = Action.DELTAS[Action.ACTIONS[jump]]

        for i, delta in enumerate(Action.DELTAS[Action.ACTIONS[move]]):
            move_to_hexe = self + delta

            # move or jump path must in board
            if move_to_hexe._is_in_board():
                # move: destination in board and not onto other piece
                if move_to_hexe not in other_pieces:
                    possible_actions.append(Action(move, self, move_to_hexe))

                    jump_to_hexe = self + jump_delta[i]
                    # jump: destination in board and not onto other piece and
                    # path must on other piece
                    if (jump_to_hexe._is_in_board()) & \
                            (jump_to_hexe not in other_pieces):
                        possible_actions.append(Action(jump, self,
                                                       jump_to_hexe))

            # exi: one move step not in board and self in player's goal hexe
            elif self._is_in_goal_hexe():
                possible_actions.append(Action(exit_action_id, self))

        return possible_actions

    def _is_in_board(self):
        from Board import Board
        return (abs(self.q) <= Board.BOARD_BOUND) & (abs(self.r) <= Board.BOARD_BOUND)

    def _is_in_goal_hexe(self):
        from Player import Player
        if self.owner in Player.PLAYER_ORDER.keys():
            return self in Player.PLAYER_GOAL[Player.PLAYER_ORDER[self.owner]]
        return False
