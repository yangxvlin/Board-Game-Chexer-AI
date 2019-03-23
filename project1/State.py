"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-14 14:32:08
Description: 
"""


class State:
    INITIAL_TURN = 0

    def __init__(self, playing_player, obstacles, player_pieces={}):
        """ """
        # playing_player
        self.playing_player = playing_player
        # [(q, r), ...]
        self.obstacles = obstacles
        # {player: [(q, r), ...], ...}  dict planned for project 2
        self.player_pieces_dict = player_pieces
        # {(q, r): player, ...}
        self.pieces_player_dict = {}
        for player in player_pieces.keys():
            for piece in player_pieces[player]:
                self.pieces_player_dict[piece] = player

        self.action = None

    def __repr__(self):
        return "".join(["(", str(self.playing_player), ": ",
                        str(self.player_pieces_dict[self.playing_player]), ")"])
        # return "".join(["[", "{player: pieces}: ", "(", str(self.playing_player), ": ",
        #                 str(self.player_pieces_dict[self.playing_player]), ")",
        #                 ", ", "{piece: player} ",
        #                 "(", str(self.pieces_player_dict), ")", "]", "\n"])

    def __hash__(self):
        return hash(str(self))

    def __eq__(self, other):
        # state in states need this will there be a better way? 
        if self.playing_player != other.playing_player:
            return False
        self_player_piece = self.player_pieces_dict[self.playing_player]
        other_player_piece = other.player_pieces_dict[other.playing_player]

        if len(self_player_piece) != len(other_player_piece):
            return False

        for i in range(0, len(self_player_piece)):
            if self_player_piece[i] != other_player_piece[i]:
                return False
        return True

        # return set(self_player_piece) == set(other_player_piece)

        # return str(self) == str(other)

    def _copy(self):
        from copy import deepcopy
        copyed = State(self.playing_player, self.obstacles)
        copyed.player_pieces_dict = deepcopy(self.player_pieces_dict)
        copyed.pieces_player_dict = deepcopy(self.pieces_player_dict)

        return copyed

    def all_next_state(self):
        from Constants import MOVE_DELTA, MOVE, JUMP, EXIT
        from util import vector_add, on_board, action_to_string, is_in_goal_hexe

        res = []

        all_piece_on_board = self.all_pieces()

        # foreach movable piece
        for piece in self.pieces_player_dict.keys():
            for delta in MOVE_DELTA:
                adj_piece = vector_add(piece, delta)
                # print(is_in_goal_hexe(adj_piece, self.playing_player), adj_piece)
                # print(piece, delta, adj_piece)

                # move action: on board & not occupied
                if on_board(adj_piece):
                    if adj_piece not in all_piece_on_board:
                        # create next state
                        next_state = self._copy()
                        # update action
                        next_state.action = action_to_string(MOVE, piece, adj_piece)
                        # delete player's original piece info
                        mov_from_index = next_state.player_pieces_dict[self.playing_player].index(piece)
                        # update player's new piece info
                        next_state.player_pieces_dict[self.playing_player][mov_from_index] = adj_piece
                        # update location of piece
                        next_state.pieces_player_dict.pop(piece)
                        next_state.pieces_player_dict.update({adj_piece : self.playing_player})

                        if next_state not in res:
                            res.append(next_state)
                        # print(next_state.action)
                    # jump action: occupied adj piece & not occupied & on board
                    else:
                        jump_piece = vector_add(adj_piece, delta)  # jump is just move same direction again

                        if (jump_piece not in all_piece_on_board) & (on_board(jump_piece)):
                            # create next state
                            next_state = self._copy()
                            # update action
                            next_state.action = action_to_string(JUMP, piece, jump_piece)
                            # delete player's original piece info
                            jump_from_index = next_state.player_pieces_dict[self.playing_player].index(piece)
                            # update player's new piece info
                            next_state.player_pieces_dict[self.playing_player][jump_from_index] = jump_piece

                            # update location of piece
                            next_state.pieces_player_dict.pop(piece)
                            next_state.pieces_player_dict.update({jump_piece: self.playing_player})

                            # TODO for project 2 unchecked
                            # # kill other player's piece
                            # if next_state.pieces_player_dict[adj_piece] != self.playing_player:
                            #     # delete owner's piece information
                            #     next_state.player_pieces_dict[next_state.pieces_player_dict[adj_piece]].remove(adj_piece)
                            #
                            #     # update player gained piece
                            #     next_state.player_pieces_dict[self.playing_player].append(adj_piece)
                            #
                            #     # update killed piece owner
                            #     next_state.pieces_player_dict[adj_piece] = self.playing_player

                            if next_state not in res:
                                res.append(next_state)

                # exit action: move out board from goal hexe
                elif is_in_goal_hexe(piece, self.playing_player):
                    # create next state
                    next_state = self._copy()
                    # update action
                    next_state.action = action_to_string(EXIT, piece)
                    # delete player's original piece info
                    next_state.player_pieces_dict[self.playing_player].remove(piece)
                    # delete location of piece
                    next_state.pieces_player_dict.pop(piece)

                    if next_state not in res:
                        res.append(next_state)

        return res

    def has_remaining_pieces(self):
        return len(self.player_pieces_dict[self.playing_player]) != 0

    def to_board_dict(self):
        from copy import deepcopy
        board_dict = deepcopy(self.pieces_player_dict)

        for obstacle in self.obstacles:
            board_dict[obstacle] = "block"

        return board_dict

    def all_pieces(self):
        all_pieces = []

        all_pieces.extend(self.obstacles)
        all_pieces.extend(self.pieces_player_dict.keys())

        return all_pieces

    def cost_to_finish(self):
        
        def hex_distance(a, b):
            return (abs(a[0] - b[0]) +
                    abs(a[0] + a[1] - b[0] - b[1]) +
                    abs(a[1] - b[1])) / 2

        from Constants import PLAYER_GOAL
        # from math import floor

        total_dist = 0
        goal_hexes = PLAYER_GOAL[self.playing_player]

        # for each remaining pieces
        for piece in self.player_pieces_dict[self.playing_player]:
            final_dist = []

            # closest dist to exit
            for goal_hexe in goal_hexes:
                # /2 for always jumping; 1 for exit action
                final_dist.append(hex_distance(piece, goal_hexe) / 2 + 1)

            total_dist += min(final_dist)

        return total_dist

        # return 0
