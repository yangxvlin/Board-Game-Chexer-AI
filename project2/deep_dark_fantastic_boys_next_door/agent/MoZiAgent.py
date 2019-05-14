"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-5-13 13:35:21
Description: MoZi comes from an ancient Chinese philosopher
"""

from deep_dark_fantastic_boys_next_door.Constants import (THE_ART_OF_WAR,
                                                          THE_ART_OF_WAR_TURN_LIMIT,
                                                          STRATEGIC_POINTS,
                                                          MOVE, JUMP, EXIT, PASS,
                                                          NEGATIVE_INFINITY)
from deep_dark_fantastic_boys_next_door.agent.ParanoidAgent import ParanoidAgent


class MoZiAgent:

    def __init__(self, upstream, downstream, depth):
        self.upstream = upstream
        self.downstream = downstream
        self.first_phase_finished = False
        self.depth = depth
        self.search_agent = ParanoidAgent(self.depth)

    def strategy_point_occupied(self, state, point):
        return point in state.pieces_player_dict

    def get_next_action(self, state, player):
        if state.turns < THE_ART_OF_WAR_TURN_LIMIT:
            return THE_ART_OF_WAR[state.playing_player][state.turns]
        elif state.turns == 1:
            print(">>>>>>")

            if self.strategy_point_occupied(state, STRATEGIC_POINTS[state.playing_player][0]):
                return (MOVE, ((-3, 1), (-3, 0)))
            elif self.strategy_point_occupied(state, (-1, -2)) and (not self.strategy_point_occupied(state, (0, -3))):
                self.first_phase_finished = True
                return (JUMP, ((-2, -1), (0, -3)))
            else:
                return (MOVE, ((-2, -1), (-1, -2)))
        else:
            return self.search_agent.get_next_action(state, player)
