"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-14 14:32:08
Description: State to store information about the environment
"""

from copy import deepcopy
from math import ceil
from Constants import MOVE_DELTA, MOVE, JUMP, EXIT, PLAYER_GOAL, \
    PLAYER_PLAYING_ORDER, PLAYING_ORDER_PLAYER_MAP, EMPTY_BOARD
from util import vector_add, on_board, is_in_goal_hexe, action_to_string, \
    piece_min_action_to_finish


class State:
    """ class used to store information of pieces on board and player is playing
    """    

    def __init__(self, playing_player, obstacles, player_pieces=EMPTY_BOARD):
        """ initialize a state
        :param playing_player: the  player is going to perform an action
        :param obstacles: obstacles in part a
        :param player_pieces: player's corresponding pieces
        """
        # playing_player
        self.playing_player = playing_player
        # [(q, r), ...]
        self.obstacles = obstacles
        # [[(q, r), ...], ...]  list planned for project 2
        self.player_pieces_list = player_pieces
        # {(q, r): player, ...}
        self.pieces_player_dict = {}

        if player_pieces:
            for player in PLAYER_PLAYING_ORDER.values():
                for piece in player_pieces[player]:
                    self.pieces_player_dict[piece] = player

        # action from previous state to current state
        self.action = None

        # initialize static attribute for h()
        try:
            State.minimum_actions
        except AttributeError:
            State.minimum_actions = piece_min_action_to_finish(self.obstacles, 
                                        self.playing_player)


    def __repr__(self):
        """ str(State)
        :return: state.toString()
        """
        return "".join(["(", str(self.playing_player), ": ",
                        str(self.player_pieces_list[self.playing_player]), ")"])

    def __hash__(self):
        """ hash(State)
        :return: hash value the state
        """
        # return hash(str(self))
        return hash(tuple(self.player_pieces_list[self.playing_player]))

    def __eq__(self, other):
        """ check the equality of two states
        :param other: the other state
        :return: True if state has same board configuration. otherwise False
        """
        self_player_piece = self.player_pieces_list[self.playing_player]
        other_player_piece = other.player_pieces_list[other.playing_player]

        if len(self_player_piece) != len(other_player_piece):
            return False

        for i in range(0, len(self_player_piece)):
            if self_player_piece[i] != other_player_piece[i]:
                return False
        return True

    def _copy(self):
        """ copy(state)
        :return: deepcopy of current copy
        """
        copyed = State(self.playing_player, self.obstacles)
        copyed.player_pieces_list = deepcopy(self.player_pieces_list)
        copyed.pieces_player_dict = deepcopy(self.pieces_player_dict)

        return copyed

    def all_next_state(self):
        """ find all possible states
        :return: list of state after performed one action

        additional note: state's copy should inside each if condition as copy
        is an expensive operation
        """

        res = []

        all_piece = self.all_pieces()

        player_pieces = self.player_pieces_list[self.playing_player]

        # foreach movable piece
        for piece in player_pieces:
            for delta in MOVE_DELTA:
                adj_piece = vector_add(piece, delta)

                # move action: on board & not occupied
                if on_board(adj_piece):
                    # not occupied
                    if adj_piece not in all_piece:
                        # create next state
                        next_state = self._copy()

                        # update action
                        next_state.update_action(MOVE, piece, adj_piece)

                        if next_state not in res:
                            res.append(next_state)

                    # jump action: occupied adj piece & not occupied & on board
                    else:
                        # jump is just move same direction again
                        jump_piece = vector_add(adj_piece, delta)

                        # not occupied & on board
                        if (jump_piece not in all_piece) & \
                                on_board(jump_piece):
                            # create next state
                            next_state = self._copy()

                            # update action
                            next_state.update_action(JUMP, piece, jump_piece, 
                                                     adj_piece)

                            if next_state not in res:
                                res.append(next_state)

                # exit action: move out board from goal hexe
                elif is_in_goal_hexe(piece, self.playing_player):
                    # create next state
                    next_state = self._copy()
                    # update action
                    next_state.update_action(EXIT, piece)

                    if next_state not in res:
                        res.append(next_state)
        # sort the output to process exit action first then jump then move
        return sorted(res, key=lambda x: x.action)

    def update_action(self, action, from_hexe, to_hexe=None, jumped_hexe=None):
        """ update a state by action
        :param action: MOVE or JUMP or EXIT
        :param from_hexe: original hexe piece coordinate
        :param to_hexe: new hexe piece coordinate
        :param jumped_hexe: piece was jumped over
        """

        # mov and jump
        if to_hexe is not None:
            # get player's original piece index
            from_index = self.player_pieces_list[self.playing_player].index(
                from_hexe)
            # update player's new piece info over original piece
            self.player_pieces_list[self.playing_player][from_index] = to_hexe
            # update location of piece
            self.pieces_player_dict.pop(from_hexe)
            self.pieces_player_dict.update({to_hexe: self.playing_player})

        # exit
        else:
            # delete player's original piece info
            self.player_pieces_list[self.playing_player].remove(from_hexe)
            # delete location of piece
            self.pieces_player_dict.pop(from_hexe)

        # update action
        self.action = action_to_string(action, from_hexe, to_hexe)

    def has_remaining_pieces(self):
        """ check whether a player has exited all player's pieces
        :return: True if player has no more pieces, otherwise False
        """
        return len(self.player_pieces_list[self.playing_player]) != 0

    def to_board_dict(self):
        """ convert state to a printable board
        :return: {piece: piece's colour}
        """
        board_dict = {}

        for piece, player in self.pieces_player_dict.items():
            board_dict[piece] = PLAYING_ORDER_PLAYER_MAP[player]

        for obstacle in self.obstacles:
            board_dict[obstacle] = "block"

        return board_dict

    def all_pieces(self):
        """ find all pieces on board
        :return: list of all pieces
        """
        all_pieces = []

        all_pieces.extend(self.obstacles)
        all_pieces.extend(self.pieces_player_dict.keys())

        return all_pieces

    def cost_to_finish(self):
        """ h(state)
        :return: distance from current state to goal state
        """
        total_dist = 0

        # exit state has highest priority
        if (self.action is not None) and (self.action[0:4] == EXIT):
            return total_dist

        # for each remaining pieces
        for piece in self.player_pieces_list[self.playing_player]:
            total_dist += State.minimum_actions[piece]

        # used for testing to respond to case with no solution
        # try:
        #     # for each remaining pieces
        #     for piece in self.player_pieces_list[self.playing_player]:
        #         total_dist += State.minimum_actions[piece]
        # except KeyError:
        #     with open('output.txt', 'w') as the_file:
        #         the_file.write("None\n")
        #         the_file.write("None\n")
        #         the_file.write("None\n")
        #         the_file.write("None\n")
        #         the_file.write("None\n")
        #     exit(0)

        return total_dist
