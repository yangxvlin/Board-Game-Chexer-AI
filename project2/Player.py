"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-2-24 20:44:11
Description: Player class (planned)
"""

import sys
sys.path.insert(0, './aima-python')

try:
    from games import alphabeta_cutoff_search
except:
    raise

# TODO Make Player an abstract class with WhitePlayer and BlackPlayer?
class Player:
    # White Player
    WHITE = "white"

    def __init__(self, colour, depth=4):
        """ Initialize a player
        :param str colour: representing the player that control this game 
        """
        self.isWhite = True if colour == Player.WHITE else False
        # 
        self.depth = depth

        # TODO finish the constructor

    def action(self, turns):
        """ Perform the agent's action
        :param 
        """
        # TODO try min-max

        alphabeta_cutoff_search()

        pass

    def update(self, action):
        """ Update opponent's action
        :param
        """
        # TODO finish this
        pass
