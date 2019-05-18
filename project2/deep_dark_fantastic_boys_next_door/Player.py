"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 21:33:12
Description: Player class
"""

from .agent.AgentFactory import AgentFactory
from .Constants import (MOVE, JUMP, EXIT, PASS, PLAYER_PLAYING_ORDER,
                        OPEN_GAME_AGENT, OPEN_GAME_TURN_LIMIT, PASS_ACTION,
                        PLAYER_WALLS, STRATEGIC_POINTS)
from .util import (calculate_jumped_hexe, initial_state)
from collections import defaultdict
import json


class Player:
    """ agent setup to be used """
    # PLAYER_SETUP = "./deep_dark_fantastic_boys_next_door/three.json"
    # PLAYER_SETUP = "./deep_dark_fantastic_boys_next_door/setup.json"
    # PLAYER_SETUP = "./deep_dark_fantastic_boys_next_door/haha.json"
    PLAYER_SETUP = "./deep_dark_fantastic_boys_next_door/mozi.json"
    # PLAYER_SETUP = "./deep_dark_fantastic_boys_next_door/human.json"

    """ static attribute for player """
    PLAYER_INDEX = -1

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
        # player's index
        self.colour = PLAYER_PLAYING_ORDER[colour]
        # root player
        Player.PLAYER_INDEX = PLAYER_PLAYING_ORDER[colour]

        # json to identify the agent strategy
        with open(Player.PLAYER_SETUP, 'r') as f:
            player_setup = json.load(f)
            self.agent = AgentFactory.create_agent(
                player_setup[colour]["agent"],
                **player_setup[colour])

        # read setup from json
        self.eval = player_setup[colour]["eval"]
        # choose human start strategy
        self.human_start = player_setup[colour]["human_start"]

        # all played state
        self.states_history = [initial_state()]
        # board configure counter
        self.states_counter = defaultdict(int)

        # walls pieces should close to
        self.strategy_points_walls = PLAYER_WALLS[self.colour].copy()
        # walls pieces should far from
        self.strategy_traps = []
        # self.strategy_points = []
        self.strategy_points = STRATEGIC_POINTS[self.colour].copy()

    def action(self):
        """
        :return: our agent's chosen action
        """

        previous_state = self.states_history[-1]

        # player has no pieces, so no need to search
        if not previous_state.playing_player_has_pieces():
            return PASS_ACTION

        # choose to enable and follow human learned start game strategy
        if self.human_start and previous_state.turns < OPEN_GAME_TURN_LIMIT:
            return OPEN_GAME_AGENT[previous_state.playing_player][previous_state.turns]

        return self.agent.get_next_action(previous_state, self)

    def update(self, colour, action):
        """
        update the action performed by players
        :param colour: representing the player make the action
        :param action: the action made by the player
        """
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
            assert action[0] == JUMP
            jumped_hexe = calculate_jumped_hexe(action[1][0], action[1][1])
            next_state.update_action(action[0], previous_state.playing_player,
                                     action[1][0], action[1][1], jumped_hexe)

        self.states_history.append(next_state)
        self.states_counter[next_state.snap()] += 1
        print("!!!!!!!!", self.states_counter[next_state.snap()], next_state.snap())

    def choose_eval(self, index=0):
        """
        return the evaluation function with specified index in player's
        evaluation function list
        :param index: the index of the evaluation function to be returned
        :return: evaluation function with specified index
        """
        return self.eval[index]
