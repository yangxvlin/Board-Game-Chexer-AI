"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-14 14:32:08
Description: 
"""

import json
from collections import Counter
import numpy as np
import Board


class State:
    INITIAL_TURN = 0
    JSON_FILE_KEYS = ["colour", "pieces", "blocks"]

    def __init__(self, playing_player, player_pieces=None, player_finished_piece=None, turns=INITIAL_TURN):
        """ """
        # playing_player
        self.playing_player = playing_player
        # {player#: [Hexa(), ...], ...}
        self.player_pieces = player_pieces
        # {player#: finished(default=0)}
        self.player_finished_piece = player_finished_piece
        # turn# [1, ..., 256] inclusive
        self.turns = turns

    # for state in states
    def __eq__(self, other):
        # TODO test
        # TODO efficiency
        assert self.turns != other.turns

        if not isinstance(other, self.__class__):
            print("state compared with shit now")
            return False

        # same number pieces finished
        for player in np.arange(0, Board.Board.N_PLAYER):
            if self.player_finished_piece[player] != other.player_finished_piece[player]:
                return False

        # same piece for each player on board
        for player in np.arange(0, Board.Board.N_PLAYER):
            if Counter(self.player_pieces[player]) != Counter(other.player_pieces[player]):
                return False
        return True

    def __hash__(self):
        # TODO no idea
        #  class School:有一个attribute people(一个tuple of Person)
        #  我不知道该怎么implement __hash__()
        #  因为 hash((1, 2)) != hash(2, 1), 所以两个相同的学校（不同的person order）会hash出两个结果
        #  那只能反复in list check 而不能用collections.counter

        # note: hash((0, 1, 2, 3)) != hash((3, 2, 0, 1))
        # Counter(a) == Counter(b) in above example
        # a = (Person("a", (1, 2)), Person("b", 2), Person("c", 3))
        # b = (Person("a", (2, 1)), Person("c", 3), Person("b", 2))
        # hash(a) != hash (b)

        # p = Person("a", 1)
        # a = (Person("a", 1), Person("b", 2), Person("c", 3))
        # p in a == True if __eq__ defined in Person
        return 0

    @staticmethod
    def get_initial_state(playing_player):
        new_state = State(playing_player,
                          player_pieces=dict.fromkeys([i for i in np.arange(0, Board.Board.N_PLAYER)], Board.Board.INITIAL_PIECE_POSITION),
                          player_finished_piece=dict.fromkeys([i for i in np.arange(0, Board.Board.N_PLAYER)], Board.Board.PLAYER_INITIAL_SCORE))

        new_state._update_turns()

        return new_state

    def get_next_state(self, action):
        # update next player to play
        next_state = State(Board.Board.next_player(self.playing_player))

        # update player_piece position
        # TODO

        # update player finished pieces#
        # TODO

        # update turns if player 0 is now playing
        next_state.turns = self.turns
        next_state._update_turns()

        return next_state

    # TODO include this operation in previous method to reduce function call overhead
    def _update_turns(self):
        if self.playing_player == Board.Board.N_PLAYER[0]:
            self.turns += 1

    def winner(self):
        """ return true and player id if player won"""
        for player in np.arange(0, Board.Board.N_PLAYER):
            if self.player_finished_piece[player] >= Board.Board.PLAYER_WIN_THRESHOLD:
                return True, player
        return False, None

    @staticmethod
    def read_state(filename):
        with open(filename) as json_file:
            data = json.load(json_file)


