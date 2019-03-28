"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 21:33:12
Description: Player class
"""

# from Board import Board
from MaxnAgent import get_next_move


class Player:

    def __init__(self, colour):
        """ Initialize a player
        :param colour: representing the player that control this game
        """
        from util import initial_state

        self.colour = colour
        self.states_history = [initial_state()]


    def action(self, turn):
        """ Perform the agent's action
        :param 
        """
        next_move = get_next_move(self.states_history[-1])

        return next_move

    def update(self, action):
        """ Update opponent's action
        :param action
        """
        # action from String

        # generate state | action
        next_state = self.states_history[-1].copy()
        next_state.update_action()

        self.states_history.append(next_state)
