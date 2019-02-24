"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-2-24 21:09:33
Description: Class for the game including gaming history, all possible moves, 
             gaming history after commit a move, a utility function, final state
             check.
"""

import sys
sys.path.insert(0, './aima-python')

try:
    from games import Game
except:
    raise


class BoardGame(Game):
    def __init__(self):
        # TODO constructor of an empty game
        self.initial = None # TODO start status needs implement

    def actions(self, state):
        """Return a list of the allowable moves at this point."""
        # TODO finish this
        pass

    def result(self, state, move):
        """Return the state that results from making a move from a state."""
        # TODO finish this
        pass

    def utility(self, state, player):
        """Return the value of this final state to player."""
        # TODO finish this
        pass

    def terminal_test(self, state):
        """Return True if this is a final state for the game."""
        return not self.actions(state)

