"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-5-13 13:35:21
Description: MoZi comes from an ancient Chinese philosopher
             Our best agent, perform a human-like game playing strategy
"""

from deep_dark_fantastic_boys_next_door.Constants import (THE_ART_OF_WAR,
    THE_ART_OF_WAR_TURN_LIMIT, STRATEGIC_POINTS, MOVE, JUMP, EXIT, PASS,
    NEGATIVE_INFINITY, STRATEGIC_POINTS, ALL_STRATEGIC_POINTS,
    STRATEGY_JUMP_FROM_TO_POINTS, PLAYER_WIN_THRESHOLD,
    STRATEGY_POINTS_AND_WALL, STRATEGY_JUMP_FROM_TO_OUTSIDE_POINTS,
    STRATEGY_SAFE_MOVE_TO_OUTSIDE_POINTS, BLUE_PLAYER_INDEX, DEATH_POINT)
from deep_dark_fantastic_boys_next_door.agent.MaxnAgent import MaxnAgent
from numpy.random import choice


class MoZiAgent:

    def __init__(self, upstream, downstream, depth):
        """
        initialize a MoZi
        :param upstream: our first target player who is played before us
        :param downstream: our second target player who is played behind us
        :param depth: search depth
        """
        self.upstream = upstream
        self.downstream = downstream
        # indicate whether we have accomplished first phase strategy
        self.arrived_strategy_points = False
        # maxn agent search depth
        self.depth = depth
        # maxn agent to search MoZi agent
        self.search_agent = MaxnAgent(self.depth)
        # MoZi dynamic strategy points
        self.strategy_points = None

    def get_next_action(self, state, player):
        """"
        an interface provide for outside object to perform MoZi agent choice
        :param state: input state
        :param player: player object contains information parameter
        :return: MoZi searched result
        """
        # initialize MoZi's dynamic strategy points
        if self.strategy_points is None:
            self.strategy_points = player.strategy_points
        self.update_strategy_points(state)

        # human learned good start strategy
        if state.turns < THE_ART_OF_WAR_TURN_LIMIT:
            # can't choose predefined strategy, then directly jump to first
            # phase maxn search
            if (state.playing_player == BLUE_PLAYER_INDEX) and \
                    self.strategy_point_occupied(state, DEATH_POINT):
                # 0, 3 are chosen evaluation function in this phase
                return self.search_agent.get_next_action(state, player, 0, 3)
            else:
                return THE_ART_OF_WAR[state.playing_player][state.turns]
        elif state.turns == 1:
            return self.start_game_agent_action_search(state, player)

        else:
            strategy_points_arrived = self.player_pieces_in_strategy_points(
                state.playing_player, state)

            # second phase
            if (not self.arrived_strategy_points) and strategy_points_arrived:
                self.arrived_strategy_points = True
                return self.get_second_phase_action(state,
                                                    player,
                                                    strategy_points_arrived)
            elif self.arrived_strategy_points:
                return self.get_second_phase_action(state,
                                                    player,
                                                    strategy_points_arrived)

            # agent try to go to strategy points in first phase
            else:
                self.update_walls(state, player)
                # 0, 3 are chosen evaluation function in this phase
                return self.search_agent.get_next_action(state, player, 0, 3)

    def get_second_phase_action(self, state, player, strategy_points_arrived):
        """
        MoZi Agent has occupied all enemy's strategy points and start capturing
        enemy gift piece in the trap; moving extra pieces to self strategy
        points; set pieces in strategy points free when the hunted player in
        knocked out; exit pieces when have enough pieces to win
        :param state: current state
        :param player: player object
        :param strategy_points_arrived: strategy points player has occupied
        :return: action MoZi agent chosen in second phase
        """
        self.update_walls(state, player)
        player_arrived_pieces, player_outside_pieces = self.divide_pieces(state)

        num_player_outside_pieces = len(player_outside_pieces)

        # enemy gift piece check
        move = self.check_gift_jump(state, player_arrived_pieces)
        if move is not None:
            return move

        # remove to enemy strategy points
        if not strategy_points_arrived:
            # 0, 4 are chosen evaluation function in this phase
            return self.search_agent.get_next_action(state, player, 0, 4)

        # has extra pieces, thus wander pieces to strategy points; or exit
        # pieces when have enough pieces to win
        if num_player_outside_pieces > 0:
            copied_state = state.copy()
            copied_state.player_pieces_list[copied_state.playing_player] = \
                player_outside_pieces
            # enough to exit, exit as quick as possible
            if copied_state.player_has_win_chance(copied_state.playing_player):
                # 2, 4 are chosen evaluation function in this phase
                return self.search_agent.get_next_action(copied_state, player, 2, 4)
            # not enough to exit, go to goals and wait to exit
            # 1, 3 are chosen evaluation function in this phase
            return self.search_agent.get_next_action(copied_state, player, 1, 3)

        # has no extra pieces, thus choose an safe move
        else:
            enemy_gift = self.choose_safe_jump(state, player_arrived_pieces)
            if len(enemy_gift) > 0:
                return enemy_gift[choice(len(enemy_gift))]

            safe_move = self.choose_safe_move(state, player_arrived_pieces)
            if len(safe_move) > 0:
                return safe_move[choice(len(safe_move))]

            # otherwise do whatever
            # 0, 4 are chosen evaluation function in this phase
            return self.search_agent.get_next_action(state, player, 0, 4)

    def strategy_point_occupied(self, state, point):
        """
        :param state: current state
        :param point: coordinate of pieces
        :return: True if strategy is occupied by a pieces, False otherwise
        """
        return point in state.pieces_player_dict

    def update_strategy_points(self, state):
        """
        delete unnecessary strategy points when the player is knock out
        :param state: current state
        """
        # 2 here is number of two strategy point for each player
        if state.is_player_knock_out(self.upstream):
            for point in STRATEGIC_POINTS[state.playing_player][:2]:
                if point in self.strategy_points:
                    self.strategy_points.remove(point)
        if state.is_player_knock_out(self.downstream):
            for point in STRATEGIC_POINTS[state.playing_player][2:]:
                if point in self.strategy_points:
                    self.strategy_points.remove(point)

    def update_walls(self, state, player):
        """
        delete unnecessary walls when the strategy points are no longer needed
        :param state: current state
        :param player: player object
        """
        upstream_points, downstream_points = \
            self.divide_pieces_to_strategies_points(state.playing_player, state)
        # 2 here is number of two strategy point for each player
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

    def choose_safe_move(self, state, pieces_in_strategy_points):
        """
        :param state: current state
        :param pieces_in_strategy_points: pieces occupies strategy points
        :return: safe move to outside points
        """
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
        return safe_move

    def choose_safe_jump(self, state, pieces_in_strategy_points):
        """
        :param state: current state
        :param pieces_in_strategy_points: pieces occupies strategy points
        :return: safe jump to outside points
        """
        enemy_gift = []

        for piece in pieces_in_strategy_points:
            jump_choice = STRATEGY_JUMP_FROM_TO_OUTSIDE_POINTS[piece]
            if self.check_gift_enemy_piece(state,
                                           jump_choice[0],
                                           jump_choice[1]) and \
                    (jump_choice[2] not in state.pieces_player_dict):
                enemy_gift.append((JUMP, (piece, jump_choice[1])))
        return enemy_gift

    def check_gift_jump(self, state, pieces_in_strategy_points):
        """
        :param state: current state
        :param pieces_in_strategy_points: pieces occupies strategy points
        :return: opponent has piece in our trap and we can perform an action to
                 capture extra pieces, None if no such action
        """
        for piece in pieces_in_strategy_points:
            for jump_choice in STRATEGY_JUMP_FROM_TO_POINTS:
                if (piece == jump_choice[0]) and \
                        self.check_gift_enemy_piece(state,
                                                    jump_choice[1],
                                                    jump_choice[2]):
                    return JUMP, (jump_choice[0], jump_choice[2])
        return None

    def check_gift_enemy_piece(self, state, jumped, jumped_to):
        """
        :param state: current state
        :param jumped: the piece jumped over
        :param jumped_to: the hexe jumped to
        :return: True if here is a gift piece from the opponent, False otherwise
        """
        return (jumped in state.pieces_player_dict) and \
               (jumped_to not in state.pieces_player_dict) and \
               (state.pieces_player_dict[jumped] != state.playing_player)

    def divide_pieces(self, state):
        """
        divide player's currently owning pieces into pieces arrived in strategy
        points and pieces not in.
        :param state: current state
        :return: two list of pieces
        """
        player_arrived_pieces = []
        player_outside_pieces = []

        for piece in state.player_pieces_list[state.playing_player]:
            if piece in self.strategy_points:
                player_arrived_pieces.append(piece)
            else:
                player_outside_pieces.append(piece)
        return player_arrived_pieces, player_outside_pieces

    def player_pieces_in_strategy_points(self, player_id, state):
        """
        :param player_id: player checked for
        :param state: current state
        :return: True if player has occupied all dynamically allocated strategy
        points, False otherwise
        """
        arrived = 0

        for piece in state.player_pieces_list[player_id]:
            if piece in self.strategy_points:
                arrived += 1

        return arrived == len(self.strategy_points)

    def divide_pieces_to_strategies_points(self, player, state):
        """
        divide pieces on board into two piles: pieces in upstream player
        strategy points and pieces in downstream player strategy points
        :param player: player object
        :param state: current state
        :return: two tuples of pieces
        """
        upstream_points = []
        downstream_points = []

        # for all strategy points
        for i, piece in enumerate(STRATEGIC_POINTS[player]):
            # for strategy points occupied by player
            if piece in state.player_pieces_list[player]:
                # divide
                if i <= 1:
                    upstream_points.append(piece)
                else:
                    downstream_points.append(piece)

        return tuple(upstream_points), tuple(downstream_points)

    def start_game_agent_action_search(self, state, player):
        """
        :param state: input state
        :param player: player object contains information parameter
        :return: start game action
        """
        actions = set(state.all_next_action())

        for action in THE_ART_OF_WAR[state.playing_player][state.turns]:
            if action in actions:
                return action
        # otherwise directly step to first phase
        # 0, 3 are chosen evaluation function in this phase
        return self.search_agent.get_next_action(state, player, 0, 3)
