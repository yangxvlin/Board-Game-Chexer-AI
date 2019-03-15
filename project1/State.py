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

    def get_next_state(self, action):
        # update next player to play
        next_state = State(self.playing_player)

        # update player_piece position|action
        # TODO

        return next_state
