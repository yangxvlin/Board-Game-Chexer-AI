"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-14 14:32:08
Description: 
"""
from Board import Board


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

    def get_next_state(self, action):
        # update next player to play
        next_state = State(self.playing_player)

        # update player_piece position|action
        # move or jump
        self.player_pieces[self.playing_player].remove(action.from_hexe)
        # exit
        if action.action_id == 2:
            self.player_pieces[self.playing_player].remove(action.from_hexe)
        
        return next_state

    def has_remaining_pieces(self):
        return len(self.player_pieces[self.playing_player]) == 0

    def to_board_dict(self):
        board_dict = {}

        for player in range(0, Board.N_PLAYER):
            for hexe in self.player_pieces[player]:
                board_dict[(hexe.q, hexe.r)] = hexe.owner

        for hexe in self.obstacles:
            board_dict[(hexe.q, hexe.r)] = hexe.owner
        return board_dict
