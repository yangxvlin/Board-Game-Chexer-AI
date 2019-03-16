"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-14 14:32:08
Description: 
"""


class State:
    INITIAL_TURN = 0

    def __init__(self, playing_player, player_pieces=None, obstacles=None):
        """ """
        # playing_player
        self.playing_player = playing_player
        # {player#: [Hexe(), ...], ...}
        self.player_pieces = player_pieces
        # [Hexe(), ...]
        self.obstacles = obstacles

    def __repr__(self):
        # print(self.player_pieces)
        return "".join([str(self.playing_player), ": ",
                        str(self.player_pieces[self.playing_player])])

    def get_next_state(self, action):
        # update next player to play
        next_state = State(self.playing_player)

        # print("action: ", action)
        # print("previous: ", self)

        # update player_piece position|action
        import copy
        next_state.player_pieces = copy.deepcopy(self.player_pieces)
        # move or jump or exit
        # print("####", next_state.player_pieces[self.playing_player], action.from_hexe, action.from_hexe in next_state.player_pieces[self.playing_player])
        next_state.player_pieces[self.playing_player].remove(action.from_hexe)
        # move or jump
        if action.action_id != 2:
            next_state.player_pieces[self.playing_player].append(action.to_hexe)

        next_state.obstacles = copy.deepcopy(self.obstacles)

        # print("after: ", next_state)

        # print(" -> ".join([str(self), str(next_state)]))
        return next_state

    def has_remaining_pieces(self):
        return len(self.player_pieces[self.playing_player]) != 0

    def to_board_dict(self):
        board_dict = {}

        from Board import Board

        for player in range(0, Board.N_PLAYER):
            try:
                for hexe in self.player_pieces[player]:
                    board_dict[(hexe.q, hexe.r)] = hexe.owner
            except KeyError:
                continue

        for hexe in self.obstacles:
            board_dict[(hexe.q, hexe.r)] = hexe.owner
        return board_dict

    def all_pieces(self):
        all_pieces = []

        all_pieces.extend(self.obstacles)

        from Board import Board
        for player in range(0, Board.N_PLAYER):
            try:
                all_pieces.extend(self.player_pieces[player])
            except KeyError:
                continue

        return all_pieces

    def all_possible_playing_player_action(self):
        res = []

        for piece in self.player_pieces[self.playing_player]:
            res.extend(piece.get_all_possible_actions(self.all_pieces()))

        return res

    def cost_to_finish(self):
        
