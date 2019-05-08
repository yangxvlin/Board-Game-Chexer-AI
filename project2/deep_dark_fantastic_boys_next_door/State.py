"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-14 14:32:08
Description: State to store information about the environment
"""

from copy import deepcopy
from .Constants import (MOVE_DELTA, MOVE, JUMP, EXIT, PASS,
                        PLAYER_PLAYING_ORDER, EMPTY_BOARD, PLAYER_WIN_THRESHOLD, MAX_TURN, N_PLAYER
                        )
from .util import (vector_add, on_board, is_in_goal_hexe, element_to_tuple)


class State:
    """ class used to store information of pieces on board and player is playing
    """

    # rea, green, blue
    DEST = [[(-3, 0), (-3, 1), (-3, 2), (-3, 3)],
            [(0, -3), (1, -3), (2, -3), (3, -3)],
            [(3, 0), (2, 1), (1, 2), (0, 3)]]

    def __init__(self, playing_player, player_pieces, scores):
        """ initialize a state
        :param playing_player: the  player is going to perform an action
        :param player_pieces: player's corresponding pieces
        """
        # playing_player
        self.playing_player = playing_player
        # [[(q, r), ...], ...]  list planned for project 2
        self.player_pieces_list = player_pieces
        # {(q, r): player, ...}
        self.pieces_player_dict = {piece: player
                                   for player in PLAYER_PLAYING_ORDER.values()
                                   for piece in self.player_pieces_list[player]}

        # action from previous state to current state
        self.action = None
        self.turns = 0
        self.finished_pieces = deepcopy(scores)

    def __repr__(self):
        """ str(State)
        :return: state.toString()
        """
        return str(self.player_pieces_list)

    def __hash__(self):
        """ hash(State)
        :return: hash value the state
        """
        # return hash(str(self))
        return hash(tuple(element_to_tuple(self.player_pieces_list)))

    def __eq__(self, other):
        """ check the equality of two states
        :param other: the other state
        :return: True if state has same board configuration. otherwise False
        """
        return set(self.pieces_player_dict.items()) == \
                set(other.pieces_player_dict.items())

    def copy(self):
        """ copy(state)
        :return: deepcopy of current copy
        """
        copyed = State(self.playing_player, EMPTY_BOARD, self.finished_pieces)
        copyed.player_pieces_list = deepcopy(self.player_pieces_list)
        copyed.pieces_player_dict = deepcopy(self.pieces_player_dict)
        copyed.turns = self.turns

        return copyed

    def all_next_action(self):
        res = []

        all_piece = self.all_pieces()

        player_pieces = self.player_pieces_list[self.playing_player]

        # if there is an exit action, then current state has only this
        # next state
        for piece in player_pieces:
            if is_in_goal_hexe(piece, self.playing_player):
                res.append((EXIT, piece))

        # foreach movable piece
        for piece in player_pieces:
            for delta in MOVE_DELTA:
                adj_piece = vector_add(piece, delta)

                # move action: on board & not occupied
                if on_board(adj_piece):
                    # not occupied
                    if adj_piece not in all_piece:
                        res.append((MOVE, (piece, adj_piece)))

                    # jump action: occupied adj piece & not occupied & on board
                    else:
                        # jump is just move same direction again
                        jump_piece = vector_add(adj_piece, delta)

                        # not occupied & on board
                        if (jump_piece not in all_piece) & \
                                on_board(jump_piece):
                            res.append((JUMP, (piece, jump_piece)))

        if len(res) == 0:
            return [(PASS, None)]
        else:
            # sort the output to process exit action first then jump then move
            return res

    def all_next_state(self):
        """ find all possible states
        :return: list of state after performed one action

        additional note: state's copy should inside each if condition as copy
        is an expensive operation
        """
        res = []

        all_piece = self.all_pieces()

        player_pieces = self.player_pieces_list[self.playing_player]

        # if there is an exit action, then current state has only this
        # next state
        for piece in player_pieces:
            if is_in_goal_hexe(piece, self.playing_player):
                # create next state
                next_state = self.copy()
                # update action
                next_state.update_action(EXIT, self.playing_player, piece)

                if next_state not in res:
                    res.append(next_state)

        # foreach movable piece
        for piece in player_pieces:
            for delta in MOVE_DELTA:
                adj_piece = vector_add(piece, delta)

                # move action: on board & not occupied
                if on_board(adj_piece):
                    # not occupied
                    if adj_piece not in all_piece:
                        # create next state
                        next_state = self.copy()
                        # update action
                        next_state.update_action(MOVE, self.playing_player,
                                                 piece, adj_piece)

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
                            next_state = self.copy()
                            # update action
                            next_state.update_action(JUMP, self.playing_player,
                                                     piece, jump_piece,
                                                     adj_piece)

                            if next_state not in res:
                                res.append(next_state)

        if len(res) == 0:
            next_state = self.copy()
            next_state.update_action(PASS, self.playing_player)
            return [next_state]
        else:
            # sort the output to process exit action first then jump then move
            return sorted(res, key=lambda x: x.action[0])
        # return res

    def update_action(self, action, previous_player, from_hexe=None, to_hexe=None,
                      jumped_hexe=None):
        """ update a state by action
        :param previous_player: player playing in previous state
        :param action: MOVE or JUMP or EXIT
        :param from_hexe: original hexe piece coordinate
        :param to_hexe: new hexe piece coordinate
        :param jumped_hexe: piece was jumped over
        """
        # update next playing player info
        self.playing_player = self.get_next_player_index()
        # update turns
        if previous_player == 2:
            self.turns += 1

        if action != PASS:
            # mov and jump
            if to_hexe is not None:
                # get player's original piece index
                from_index = self.player_pieces_list[previous_player].index(
                    from_hexe)
                # update player's new piece info over original piece
                self.player_pieces_list[previous_player][from_index] = to_hexe
                # update location of piece
                self.pieces_player_dict.pop(from_hexe)
                self.pieces_player_dict.update({to_hexe: previous_player})
                # update action
                self.action = (action, (from_hexe, to_hexe))

                # jump need to update jumped piece info
                if action == JUMP:
                    # jumped other player's piece
                    if jumped_hexe not in self.player_pieces_list[previous_player]:
                        # get jumped piece's player index
                        jumped_hexe_player = self.pieces_player_dict[jumped_hexe]
                        # update player's new piece info over original piece
                        self.player_pieces_list[jumped_hexe_player].remove(
                            jumped_hexe)
                        self.player_pieces_list[previous_player].append(jumped_hexe)

                        # update location of piece
                        self.pieces_player_dict.pop(jumped_hexe)
                        self.pieces_player_dict.update(
                            {jumped_hexe: previous_player})

            # exit
            else:
                # delete player's original piece info
                self.player_pieces_list[previous_player].remove(from_hexe)
                # delete location of piece
                self.pieces_player_dict.pop(from_hexe)
                # update action
                self.action = (action, from_hexe)
                # update player's score
                self.finished_pieces[previous_player] += 1
        # pass
        else:
            # update action
            self.action = (action, None)

    def get_next_player_index(self):
        if self.playing_player != 2:
            return self.playing_player + 1
        else:
            return 0

    def has_remaining_pieces(self):
        """ check whether a player has exited all player's pieces
        :return: True if player has no more pieces, otherwise False
        """
        return len(self.player_pieces_list[self.playing_player]) != 0

    def all_pieces(self):
        """ find all pieces on board
        :return: list of all pieces
        """
        return self.pieces_player_dict.keys()

    def get_winner(self):
        for player in range(0, N_PLAYER):
            if self.finished_pieces[player] == PLAYER_WIN_THRESHOLD:
                return player
        return None

    def is_terminate(self):
        return ((self.turns == MAX_TURN) and (self.playing_player == 2)) or \
               (self.get_winner is not None)

    def _cost_to_finish(self, player):
        """ h(state)
        :return: distance from current state to goal state
        """
        # TODO implement dijkstra to estimate the cost
        # hex distance right now
        total_dist = 0
        for i in self.player_pieces_list[player]:
            min_dist = 10
            for j in State.DEST[player]:
                curr_dist = self._hex_dist(i, j)
                if curr_dist < min_dist:
                    min_dist = curr_dist
            total_dist += min_dist
        return total_dist/2

    @staticmethod
    def _hex_dist(hex1, hex2):
        return max(abs(hex1[0] - hex2[0]), abs((-hex1[0] - hex1[1]) - (-hex2[0] - hex2[1])),
                   abs(hex1[1] - hex2[1]))

    def evaluate(self, player, eval_function_name):
        # return eval_function_name(player)
        return self._evaluate1(player)

    def _evaluate1(self, player):
        # feature dist to destination, number of player's pieces(include player and finished)
        # eval func = 1 * distance +  1 * num_all_pieces
        return -self._cost_to_finish(player) + self.finished_pieces[player] + len(self.player_pieces_list[player])

    def get_key(self):
        return tuple(element_to_tuple(self.player_pieces_list)) + tuple(self.finished_pieces)

    def is_player_finished(self):
        return self.finished_pieces[self.playing_player] == PLAYER_WIN_THRESHOLD

    # def is_other_player_finished(self):
