"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-14 14:32:08
Description: 
"""


class State:
    INITIAL_TURN = 0

    def __init__(self, playing_player, player_pieces=None, obstacles=None, turns=INITIAL_TURN):
        """ """
        # playing_player
        self.playing_player = playing_player
        # {player#: [Hexa(), ...], ...}
        self.player_pieces = player_pieces
        # [Hexa(), ...]
        self.obstacles = obstacles
        # turn# [1, ..., 256] inclusive
        self.turns = turns

    def get_next_state(self, action):
        # update next player to play
        next_state = State(self.playing_player)

        # update player_piece position|action
        # TODO


        # update turns if player 0 is now playing
        next_state.turns = self.turns
        next_state._update_turns()

        return next_state

    # TODO include this operation in previous method to reduce function call overhead
    def _update_turns(self):
        if self.playing_player == Board.Board.N_PLAYER[0]:
            self.turns += 1
