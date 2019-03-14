"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 21:30:38
Description: Class used to represent the board and available information for agent
"""

import copy
from State import State
import numpy as np


class Board(object):
    N_PLAYER = 3
    PLAYERS = [0, 1, 2]
    INITIAL_PIECE_POSITION = [] # initial piece when game start

    # player has no pieces exit initially
    PLAYER_INITIAL_SCORE = 0

    # play win when 4 pieces exit
    PLAYER_WIN_THRESHOLD = 4

    # if cur turn > MAX_TURN, game draw
    MAX_TURN = 256

    # if 4 duplicate state, game draw
    DUPLICATE_STATE_THRESHOLD = 4

    def __init__(self, my_player):
        # history of states
        self.states = []

        # player play next move
        # TODO do we need this attribute?
        self.playing_player = Board.PLAYERS[0]

        # my player index
        self.my_player = my_player

        # load initial state
        # TODO store initial state based on forum reply
        self.states.append(State.get_initial_state(self.playing_player))

    def update_action(self, action):
        next_state = self.states[-1].get_next_state(action)
        self.states.append(next_state)

        # TODO delete based on attribute
        self.playing_player = next_state.playing_player

    def is_terminate(self, state):
        # return true or false if the game is ended
        # based on self.states[-1]

        has_winner, _ = state.winner()

        return has_winner | self.is_state_duplicated(state)

    def is_state_duplicated(self, state):
        # TODO O(n): can it be faster or better efficiency
        states_copy = copy.deepcopy(self.states)

        for _ in np.arange(0, Board.N_PLAYER):
            if state in states_copy:
                states_copy.remove(state)
            else:
                return False
        return True

    @staticmethod
    def next_player(cur_player):
        """ """
        return cur_player-Board.PLAYERS[-1] if (cur_player == Board.PLAYERS[-1]) else cur_player+1

    @staticmethod
    def get_all_possible_moves(state):
        """ Takes a sequence of game states representing the full game history, and returns the full list of moves that
        are legal plays for the current player.

        """
        all_player_pieces = state.player_pieces[state.playing_player]

        possible_moves = []

        for piece in all_player_pieces:
            possible_moves.extend(piece.get_all_movable_hexa())

        return possible_moves

# ************************************************** evaluation ******************************************************

    def evaluate_state(self, state):
        """ return a list of evaluate score for all player in one state"""
        # need be non-static cause need player's score
        res = []

        for player in np.arange(0, Board.N_PLAYER):
            res.append(self.evaluate_player_state(player, state))
        return res

    def evaluate_player_state(self, player, state):
        # TODO when just start no state for player not yet played
        # need be non-static cause need player's score
        return 0

    def evaluate_action(self, action):
        return self.evaluate_action_on_state(self.states[-1], action)

    def evaluate_action_on_state(self, state, action):
        return self.evaluate_state(state.get_next_state(action))
