"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-14 14:32:08
Description: State to store information about the environment
"""

from copy import deepcopy
from math import ceil
from Constants import MOVE_DELTA, MOVE, JUMP, EXIT, PLAYER_GOAL, \
    PLAYER_PLAYING_ORDER, PLAYING_ORDER_PLAYER_MAP, N_PLAYER, PLAYER_ORDER, \
    PLAYER_WIN_THRESHOLD, MAX_TURN
from util import vector_add, on_board, is_in_goal_hexe, action_to_string

class State:
    """ class used to store information of pieces on board and player is playing
    """

    def __init__(self, playing_player, player_pieces=[], turns = 0):
        """ initialize a state
        :param playing_player: the  player is going to perform an action
        :param obstacles: obstacles in part a
        :param player_pieces: player's corresponding pieces
        :param turns: turns has played in game
        """
        # playing_player
        self.playing_player = playing_player
        # [[(q, r), ...], ...]  list planned for project 2
        self.player_pieces_list = player_pieces
        # {(q, r): player, ...}
        self.pieces_player_dict = {}

        if player_pieces:
            for player in PLAYER_PLAYING_ORDER.values():
                for piece in player_pieces[player]:
                    self.pieces_player_dict[piece] = player

        self.action = None
        self.turns = turns
        self.score = [0 for _ in range(0, N_PLAYER)]

    def __repr__(self):
        """ str(State)
        :return: state.toString()
        """

        res = str(self.turns) + ": " + \
            PLAYING_ORDER_PLAYER_MAP[self.playing_player]

        for player in PLAYER_ORDER:
            res = "".join([res, " (", PLAYING_ORDER_PLAYER_MAP[player], ": ",
                        str(self.player_pieces_list[player]), ")"])

        return res

    def __hash__(self):
        """ hash(State)
        :return: hash value the state
        """

        res = []

        for player in PLAYER_ORDER:
            res.append((player, tuple(self.player_pieces_list[player])))

        return hash(tuple(res))

    def __eq__(self, other):
        """ check the equality of two states
        :param other: the other state
        :return: True if state has same board configuration. otherwise False
        """

        for player in PLAYER_ORDER:

            self_player_piece = self.player_pieces_list[player]
            other_player_piece = other.player_pieces_list[player]

            if len(self_player_piece) != len(other_player_piece):
                return False

            for i in range(0, len(self_player_piece)):
                if self_player_piece[i] != other_player_piece[i]:
                    return False
        return True

    def copy(self):
        """ copy(state)
        :return: deepcopy of current copy
        """
        copyed = State(self.playing_player)
        copyed.player_pieces_list = deepcopy(self.player_pieces_list)
        copyed.pieces_player_dict = deepcopy(self.pieces_player_dict)

        return copyed

    def next_player(self):
        # blue go to red
        if self.playing_player == 2:
            self.playing_player = 0
            self.turns += 1
        else:
            self.playing_player += 1

    def all_next_state(self):
        """ find all possible states
        :return: list of state after performed one action

        additional note: state's copy should inside each if condition as copy
        is an expensive operation
        """

        res = []

        all_piece_on_board = self.all_pieces()

        # These two line of code give same output and nearly same run time, but
        # the second has a better practical performance.
        # Because the first one give in piece order (e.g. always [piece No.1, 
        # piece No.2, ...] no matter the change in axial coordinates due to my 
        # implementation). 
        # The second one give in last modified time order (e.g. [most hasn't 
        # moved piece, second most hasn't moved piece, ...])
        # As a result, the true solution tends to move piece respectively not
        # in a focusing on particular piece. Which means the second one is
        # closer to real world logic consider process. As a result, lead to 
        # a better practical performance.
        # player_pieces = self.player_pieces_list[self.playing_player]
        player_pieces = [k for k, v in self.pieces_player_dict.items()
                         if v == self.playing_player]

        # foreach movable piece
        for piece in player_pieces:
            for delta in MOVE_DELTA:
                adj_piece = vector_add(piece, delta)

                # move action: on board & not occupied
                if on_board(adj_piece):
                    # not occupied
                    if adj_piece not in all_piece_on_board:
                        # create next state
                        next_state = self.copy()

                        # update action
                        next_state.update_action(MOVE, piece, adj_piece)

                        if next_state not in res:
                            res.append(next_state)

                    # jump action: occupied adj piece & not occupied & on board
                    else:
                        # jump is just move same direction again
                        jump_piece = vector_add(adj_piece, delta)

                        # not occupied & on board
                        if (jump_piece not in all_piece_on_board) & \
                                (on_board(jump_piece)):
                            # create next state
                            next_state = self.copy()

                            # update action
                            next_state.update_action(JUMP, piece, jump_piece, 
                                                     adj_piece)

                            if next_state not in res:
                                res.append(next_state)

                # exit action: move out board from goal hexe
                elif is_in_goal_hexe(piece, self.playing_player):
                    # create next state
                    next_state = self.copy()
                    
                    # update action
                    next_state.update_action(EXIT, piece)

                    if next_state not in res:
                        res.append(next_state)

        if len(res) == 0:
            res = ["PASS"]

        return res

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

            # kill other player's piece
            if action == JUMP:
                # jumped other player's piece
                if self.pieces_player_dict[jumped_hexe] != \
                        self.playing_player:

                    # delete owner's piece information
                    self.player_pieces_list[
                        self.pieces_player_dict[
                            jumped_hexe]].remove(jumped_hexe)
            
                    # update player gained piece
                    self.player_pieces_list[
                        self.playing_player].append(jumped_hexe)
            
                    # update killed piece owner
                    self.pieces_player_dict[jumped_hexe] = \
                        self.playing_player
        # exit
        else:
            # delete player's original piece info
            self.player_pieces_list[self.playing_player].remove(from_hexe)
            # delete location of piece
            self.pieces_player_dict.pop(from_hexe)
            # update player's score
            self.score[self.playing_player] += 1

        # update action
        self.action = action_to_string(action, from_hexe, to_hexe)
        # update next player to play & turn number
        self.next_player()

    def has_remaining_pieces(self, player=None):
        """ check whether a player has exited all player's pieces
        :return: True if player has no more pieces, otherwise False
        """
        if player is None:
            player = self.playing_player
            
        return len(self.player_pieces_list[player]) != 0

    def to_board_dict(self):
        """ convert state to a printable board
        :return: {piece: piece's colour}
        """
        board_dict = deepcopy(self.pieces_player_dict)

        return board_dict

    def all_pieces(self):
        """ find all pieces on board
        :return: list of all pieces
        """
        return self.pieces_player_dict.keys()

    def cost_to_finish(self, player=None):
        """ h(state)
        :return: distance from current state to goal state
        """
        
        def hex_distance(a, b):
            """ calculate hexe distance
            modified from https://www.redblobgames.com/grids/hexagons/#distance
            :param a: piece 1
            :param b: piece 2
            :return: hexe distance between two hexe
            """
            return (abs(a[0] - b[0]) +
                    abs(a[0] + a[1] - b[0] - b[1]) +
                    abs(a[1] - b[1])) / 2

        if player is None:
            player = self.playing_player

        total_dist = 0
        goal_hexes = PLAYER_GOAL[player]

        # for each remaining pieces
        for piece in self.player_pieces_list[player]:
            final_dist = []

            # closest dist to exit
            for goal_hexe in goal_hexes:
                # /2 for always jumping; 1 for exit action
                final_dist.append(ceil(hex_distance(piece, goal_hexe) / 2) + 1)

            total_dist += min(final_dist)

        return total_dist

    def has_winner(self):
        for player in PLAYER_ORDER:
            if self.score[player] >= PLAYER_WIN_THRESHOLD:
                return True
        return False

    def has_turns_reamining(self):
        return self.turns <= MAX_TURN

    def is_terminate(self):
        return self.has_turns_reamining() and self.has_winner()

    def evaluate(self):
        # TODO a long road to go :(
        return 0