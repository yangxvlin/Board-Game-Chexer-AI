"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 21:33:12
Description: Player class
"""

# from MaxnAgent import get_next_move
from .agent.RandomAgent import RandomAgent
from .agent.MaxnAgent import MaxnAgent
from .agent.GreedyAgent import GreedyAgent

from .agent.AgentFactory import AgentFactory
from .Constants import (MOVE, JUMP, EXIT, PASS, PLAYER_PLAYING_ORDER,
                        OPEN_GAME_AGENT, OPEN_GAME_TURN_LIMIT, PASS_ACTION)
from .util import (calculate_jumped_hexe, initial_state)
from collections import defaultdict

import json

class Player:

    PLAYER_SETUP = "./deep_dark_fantastic_boys_next_door/setup.json"

    def __init__(self, colour):
        """
        This method is called once at the beginning of the game to initialise
        your player. You should use this opportunity to set up your own internal
        representation of the game state, and any other information about the
        game state you would like to maintain for the duration of the game.

        The parameter colour will be a string representing the player your
        program will play as (Red, Green or Blue). The value will be one of the
        strings "red", "green", or "blue" correspondingly.

        :param colour: representing the player that control this game
        """
        self.colour = PLAYER_PLAYING_ORDER[colour]

        # TODO check it can work on dimefox
        # json to identify out strategy
        with open(Player.PLAYER_SETUP, 'r') as f:
            player_setup = json.load(f)
            self.agent = AgentFactory.create_agent(player_setup[colour]["agent"], **player_setup[colour])

        self.states_history = [initial_state()]

    def action(self):
        """
        This method is called at the beginning of each of your turns to request
        a choice of action from your program.

        Based on the current state of the game, your player should select and
        return an allowed action to play on this turn. If there are no allowed
        actions, your player must return a pass instead. The action (or pass)
        must be represented based on the above instructions for representing
        actions.
        """

        # previous_state = self.states_history[-1]
        # print(previous_state.playing_player, "next player make an action")
        # print("all actions:", [s.action for s in previous_state
        # .all_next_state()])
        previous_state = self.states_history[-1]
        # print("#######", previous_state.turns)

        # player has no pieces, so no need to search
        # if len(previous_state.player_pieces_list[previous_state.playing_player])==0:
        #     return PASS_ACTION
        # else:
        #     if previous_state.turns < OPEN_GAME_TURN_LIMIT:
        #         return OPEN_GAME_AGENT[previous_state.playing_player][previous_state.turns]
        #     else:
        return self.agent.get_next_action(previous_state, self)

    def update(self, colour, action):
        """
        This method is called at the end of every turn (including your player's
        turns) to inform your player about the most recent action. You should
        use this opportunity to maintain your internal representation of the
        game state and any other information about the game you are storing.

        The parameter colour will be a string representing the player whose turn
        it is (Red, Green or Blue). The value will be one of the strings "red",
        "green", or "blue" correspondingly.

        The parameter action is a representation of the most recent action (or
        pass) conforming to the above instructions for representing actions.

        You may assume that action will always correspond to an allowed action
        (or pass) for the player colour (your method does not need to validate
        the action/pass against the game rules).

        :param colour
        :param action
        """
        # print(self.colour, "updated:", colour, action)

        previous_state = self.states_history[-1]
        assert previous_state.playing_player == PLAYER_PLAYING_ORDER[colour]
        # generate state | action
        next_state = previous_state.copy()

        if action[0] == PASS:
            assert action[1] is None
            next_state.update_action(action[0], previous_state.playing_player)
        elif action[0] == MOVE:
            next_state.update_action(action[0], previous_state.playing_player,
                                     action[1][0], action[1][1])
        elif action[0] == EXIT:
            next_state.update_action(action[0], previous_state.playing_player,
                                     action[1])
        else:
            jumped_hexe = calculate_jumped_hexe(action[1][0], action[1][1])
            next_state.update_action(action[0], previous_state.playing_player,
                                     action[1][0], action[1][1], jumped_hexe)

        self.states_history.append(next_state)
