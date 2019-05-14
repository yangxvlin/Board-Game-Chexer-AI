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
                                                          NEGATIVE_INFINITY,
                                                          STRATEGIC_POINTS)
from deep_dark_fantastic_boys_next_door.agent.ParanoidAgent import ParanoidAgent
from deep_dark_fantastic_boys_next_door.agent.MaxnAgent import MaxnAgent

class MoZiAgent:

    def __init__(self, upstream, downstream, depth):
        self.upstream = upstream
        self.downstream = downstream
        self.arrived_strategy_points = False
        self.depth = depth
        self.search_agent = MaxnAgent(self.depth)

    def strategy_point_occupied(self, state, point):
        return point in state.pieces_player_dict

    def get_next_action(self, state, player):
        # return self.search_agent.get_next_action(state, player)
        if state.turns < THE_ART_OF_WAR_TURN_LIMIT:
            return THE_ART_OF_WAR[state.playing_player][state.turns]
        elif state.turns == 1:
            if self.strategy_point_occupied(state, STRATEGIC_POINTS[state.playing_player][0]):
                return (MOVE, ((-3, 1), (-3, 0)))
            elif self.strategy_point_occupied(state, (-1, -2)) and (not self.strategy_point_occupied(state, (0, -3))):
                return (JUMP, ((-2, -1), (0, -3)))
            else:
                return (MOVE, ((-2, -1), (-1, -2)))
        elif (not self.arrived_strategy_points) and state.player_pieces_in_strategy_points(state.playing_player):
            self.arrived_strategy_points = True
            # TODO
        elif self.arrived_strategy_points:
            # TODO

        else:
            return self.search_agent.get_next_action(state, player)

    def get_second_phase_action(self, state, player):
        player_arrived_pieces = []
        player_outside_pieces = []

        for piece in state.player_pieces_list[state.playing_player]:
            if piece in STRATEGIC_POINTS[state.playing_player]:
                player_arrived_pieces.append(piece)
            else:
                player_outside_pieces.append(piece)

