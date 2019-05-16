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
                                                          STRATEGY_JUMP_FROM_TO_POINTS,
                                                          PLAYER_WIN_THRESHOLD,
                                                          STRATEGY_POINTS_AND_WALL,
                                                          STRATEGY_JUMP_FROM_TO_OUTSIDE_POINTS,
                                                          STRATEGY_SAFE_MOVE_TO_OUTSIDE_POINTS)
from deep_dark_fantastic_boys_next_door.agent.MaxnAgent import MaxnAgent
from copy import deepcopy
from numpy.random import choice

class MoZiAgent:

    def __init__(self, upstream, downstream, depth):
        self.upstream = upstream
        self.downstream = downstream
        self.arrived_strategy_points = False
        self.depth = depth
        self.search_agent = MaxnAgent(self.depth)
        self.strategy_points = None

    def strategy_point_occupied(self, state, point):
        return point in state.pieces_player_dict

    def update_strategy_points(self, state):
        if state.is_player_knock_out(self.upstream):
            for point in STRATEGIC_POINTS[state.playing_player][:2]:
                if point in self.strategy_points:
                    self.strategy_points.remove(point)
        if state.is_player_knock_out(self.downstream):
            for point in STRATEGIC_POINTS[state.playing_player][2:]:
                if point in self.strategy_points:
                    self.strategy_points.remove(point)

    def get_next_action(self, state, player):
        # print("><><", player is None)
        if self.strategy_points is None:
            self.strategy_points = player.strategy_points
        self.update_strategy_points(state)
        print(">>>>", player.strategy_points, self.strategy_points)
        # print(">>>>>", self.strategy_points, (not self.arrived_strategy_points) and state.player_pieces_in_strategy_points(state.playing_player), self.arrived_strategy_points)

        # return self.search_agent.get_next_action(state, player)
        if state.turns < THE_ART_OF_WAR_TURN_LIMIT:
            return THE_ART_OF_WAR[state.playing_player][state.turns]
        elif state.turns == 1:

            if state.playing_player == 0:
                if self.strategy_point_occupied(state, STRATEGIC_POINTS[state.playing_player][0]):
                    return MOVE, ((-3, 1), (-3, 0))
                elif self.strategy_point_occupied(state, (-1, -2)) and (not self.strategy_point_occupied(state, (0, -3))):
                    return JUMP, ((-2, -1), (0, -3))
                else:
                    return MOVE, ((-2, -1), (-1, -2))

            elif state.playing_player == 1:
                if self.strategy_point_occupied(state, STRATEGIC_POINTS[state.playing_player][0]):
                    return MOVE, ((2, -3), (3, -3))
                elif self.strategy_point_occupied(state, (3, -1)) and (not self.strategy_point_occupied(state, (3, 0))):
                    return JUMP, ((3, -2), (3, 0))
                else:
                    return MOVE, ((3, -2), (3, -1))

            else:
                assert state.playing_player == 2
                if self.strategy_point_occupied(state, STRATEGIC_POINTS[state.playing_player][0]):
                    return MOVE, ((1, 2), (0, 3))
                elif self.strategy_point_occupied(state, (-2, 3)) and (not self.strategy_point_occupied(state, (-3, 3))):
                    return JUMP, ((-1, 3), (-3, 3))
                else:
                    if (-2, 3) not in state.pieces_player_dict:
                        return MOVE, ((-1, 3), (-2, 3))
                    else:
                        return self.search_agent.get_next_action(state, player, 0, 3)
        else:
            strategy_points_arrived = self.player_pieces_in_strategy_points(state.playing_player, state)
            # if not strategy_points_arrived:
            #     self.arrived_strategy_points = False

            if (not self.arrived_strategy_points) and strategy_points_arrived:
                # print("now phase 2 !!!!")
                self.arrived_strategy_points = True
                return self.get_second_phase_action(state, player, strategy_points_arrived)
            elif self.arrived_strategy_points:
                return self.get_second_phase_action(state, player, strategy_points_arrived)
            # elif self.can_wandering(state, player):
            # agent try to go to strategy points 1st time
            else:
                self.update_walls(state, player)
                print(">>>>>>", player.strategy_points_walls, player.strategy_traps)
                return self.search_agent.get_next_action(state, player, 0, 3)

    def update_walls(self, state, player):
        upstream_points, downstream_points = self.divide_pieces_to_strategies_points(state.playing_player, state)

        if len(upstream_points) == 2:
            for wall in STRATEGY_POINTS_AND_WALL[upstream_points]:
                if wall in player.strategy_points_walls:
                    player.strategy_points_walls.remove(wall)
                    player.strategy_traps.append(wall)
        if len(downstream_points) == 2:
            for wall in STRATEGY_POINTS_AND_WALL[downstream_points]:
                if wall in player.strategy_points_walls:
                    player.strategy_points_walls.remove(wall)
                    player.strategy_traps.append(wall)
    # def can_wandering(self, state, player):

    def get_second_phase_action(self, state, player, strategy_points_arrived):
        self.update_walls(state, player)
        print(">>>>>>", player.strategy_points_walls, player.strategy_traps)
        player_arrived_pieces, player_outside_pieces = self.divide_pieces(state)

        num_player_outside_pieces = len(player_outside_pieces)
        # num_player_arrived_pieces = len(player_arrived_pieces)

        # enemy gift piece check
        move = self.check_gift_move(state, player_arrived_pieces)
        if move is not None:
            return move

        if not strategy_points_arrived:
            return self.search_agent.get_next_action(state, player, 0, 4)

        # has free pieces (#pieces > 4)
        # if (num_player_arrived_pieces == len(self.strategy_points)) and (num_player_outside_pieces > 0):
        if num_player_outside_pieces > 0:
            copied_state = state.copy()
            copied_state.player_pieces_list[copied_state.playing_player] = player_outside_pieces
            # enough to exit, exit as quick as possible
            if copied_state.player_has_win_chance(copied_state.playing_player):
                return self.search_agent.get_next_action(copied_state, player, 2, 4)
            # not enough to exit, go to goals and wait to exit
            return self.search_agent.get_next_action(copied_state, player, 1, 4)
        else:
            # choose an safe move
            enemy_gift = self.choose_safe_jump(state, player_arrived_pieces)
            if len(enemy_gift) > 0:
                return enemy_gift[choice(len(enemy_gift))]

            safe_move = self.choose_safe_move(state, player_arrived_pieces)
            if len(safe_move) > 0:
                return safe_move[choice(len(safe_move))]

            # otherwise do whatever
            return self.search_agent.get_next_action(state, player, 0, 4)

    # safe move to outside
    def choose_safe_move(self, state, pieces_in_strategy_points):
        safe_move = []

        for piece in pieces_in_strategy_points:
            move_choices = STRATEGY_SAFE_MOVE_TO_OUTSIDE_POINTS[piece]
            for move_choice in move_choices:
                if move_choice[0] not in state.pieces_player_dict:
                    has_move = True
                    for beside_point in move_choice[1:]:
                        if beside_point in state.pieces_player_dict:
                            has_move = False
                            break
                    if has_move:
                        safe_move.append((MOVE, (piece, move_choice[0])))
        print(">>>>>>>>>>>>", safe_move)
        return safe_move
    #

    # safe jump to outside
    def choose_safe_jump(self, state, pieces_in_strategy_points):
        enemy_gift = []

        for piece in pieces_in_strategy_points:
            jump_choice = STRATEGY_JUMP_FROM_TO_OUTSIDE_POINTS[piece]
            if self.check_gift_enemy_piece(state, jump_choice[0], jump_choice[1]) and (jump_choice[2] not in state.pieces_player_dict):
                enemy_gift.append((JUMP, (piece, jump_choice[1])))

        print("<<<<<<<<<<", enemy_gift)
        return enemy_gift

    # choose gift in trap by enemy
    def check_gift_move(self, state, pieces_in_strategy_points):
        for piece in pieces_in_strategy_points:
            for jump_choice in STRATEGY_JUMP_FROM_TO_POINTS:
                if (piece == jump_choice[0]) and self.check_gift_enemy_piece(state, jump_choice[1], jump_choice[2]):
                    return JUMP, (jump_choice[0], jump_choice[2])
        return None

    def check_gift_enemy_piece(self, state, jumped, jumped_to):
        return (jumped in state.pieces_player_dict) and (jumped_to not in state.pieces_player_dict) and (state.pieces_player_dict[jumped] != state.playing_player)

    def divide_pieces(self, state):
        player_arrived_pieces = []
        player_outside_pieces = []

        for piece in state.player_pieces_list[state.playing_player]:
            if piece in self.strategy_points:
                player_arrived_pieces.append(piece)
            else:
                player_outside_pieces.append(piece)
        return player_arrived_pieces, player_outside_pieces

    def player_pieces_in_strategy_points(self, player_id, state):
        arrived = 0

        for piece in state.player_pieces_list[player_id]:
            if piece in self.strategy_points:
                arrived += 1

        return arrived == len(self.strategy_points)

    def divide_pieces_to_strategies_points(self, player, state):
        upstream_points = []
        downstream_points = []

        for i, piece in enumerate(self.strategy_points):
            if piece in state.player_pieces_list[player]:
                if i <= 1:
                    upstream_points.append(piece)
                else:
                    downstream_points.append(piece)

        return tuple(upstream_points), tuple(downstream_points)
