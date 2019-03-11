"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 21:30:38
Description: Class used to represent the board and available information for agent
"""


class Board(object):
    N_PLAYER = 3
    PLAYERS = [0, 1, 2]

    def __init__(self):
        self.states = []
        self.playing_player = Board.PLAYERS[0]

    def get_states(self):
        return self.states

    def get_current_state(self):
        return self.states[-1]

    def update_state(self, state):
        self.states.append(state)

    def update_action(self, action):
        self.update_state(self.get_next_state(self.get_current_state(), action))

    def start(self):
        # Returns a representation of the starting state of the game.
        pass

    def get_current_player(self, state):
        # Takes the game state and returns the current player's int number.
        pass

    def get_next_state(self, state, action):
        # Takes the game state, and the move to be applied.
        # Returns the new game state.
        pass

    def get_all_moves(self, state):
        # Takes a sequence of game states representing the full
        # game history, and returns the full list of moves that
        # are legal plays for the current player.
        pass

    def get_winner(self):
        # use self.states[:] to fin winner
        # Takes a sequence of game states representing the full
        # game history.  If the game is now won, return the player
        # number.  If the game is still ongoing, return zero.  If
        # the game is tied, return a different distinct value, e.g. -1.
        pass

    def is_terminate(self):
        # return true or false if the game is ended
        # based on self.states[-1]
        pass

    def evaluate_state(self, state):
        # return a tuple of evaluation for each player
        pass

    def evaluate_player_state(self, player):
        # use self.states[-1]
        pass

    def evaluate_action(self, action):
        return self.evaluate_state(self.get_next_state(self.get_current_state(),action))

    def is_my_player_playing(self, my_player):
        # i.e. is our player playing now using state[-1]
        return my_player == self.playing_player

    def get_playing_player(self):
        return self.playing_player

    def get_next_player(self):
        return Board.PLAYERS[(self.playing_player - 2) if (self.playing_player > 2) else (self.playing_player + 1)]
