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
                                                          STRATEGIC_POINTS,
                                                          ALL_STRATEGIC_POINTS,
                                                          STRATEGY_JUMP_FROM_TO_POINTS)
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
            # print("now phase 2 !!!!")
            self.arrived_strategy_points = True
            return self.get_second_phase_action(state, player)
        elif self.arrived_strategy_points:
            # print("continuous phase 2 !!!!")
            return self.get_second_phase_action(state, player)
        elif self.can_wandering(state, player):

        else:
            return self.search_agent.get_next_action(state, player)

    def can_wandering(self, state, player):


    def get_second_phase_action(self, state, player):
        player_arrived_pieces = []
        player_outside_pieces = []

        for piece in state.player_pieces_list[state.playing_player]:
            if piece in STRATEGIC_POINTS[state.playing_player]:
                player_arrived_pieces.append(piece)
            else:
                player_outside_pieces.append(piece)

        # enemy gift piece check
        move = self.check_gift_move(state, player_arrived_pieces)
        if move is not None:
            return move

        # has free pieces (#pieces > 4)
        if (len(player_arrived_pieces) == 4) and (len(player_outside_pieces) > 0):
            copied_state = state.copy()
            copied_state.player_pieces_list[copied_state.playing_player] = player_outside_pieces
            return self.search_agent.get_next_action(copied_state, player, 1)

        return self.search_agent.get_next_action(state, player)

    # ((-3, 0), (0, -3), (3, -3), (3, 0), (0, 3), (-3, 3))
    def check_gift_move(self, state, pieces_in_strategy_points):
        for piece in pieces_in_strategy_points:
            for jump_choice in STRATEGY_JUMP_FROM_TO_POINTS:
                if (piece == jump_choice[0]) and self.check_gift_enemy_piece(state, jump_choice[1], jump_choice[2]):
                    return JUMP, (jump_choice[0], jump_choice[2])
        return None

    def check_gift_enemy_piece(self, state, jumped, jumped_to):
        return (jumped in state.pieces_player_dict) and (jumped_to not in state.pieces_player_dict) and (state.pieces_player_dict[jumped] != state.playing_player)
