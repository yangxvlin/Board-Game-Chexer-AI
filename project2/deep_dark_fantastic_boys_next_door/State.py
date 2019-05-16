"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-14 14:32:08
Description: State to store information about the environment
"""

from .Constants import (MOVE_DELTA, PLAYER_PREFERRED_MOVE_DELTA, MOVE, JUMP, EXIT, PASS,
                        PLAYER_PLAYING_ORDER, EMPTY_BOARD, PLAYER_WIN_THRESHOLD, MAX_TURN, N_PLAYER,
                        PLAYER_GOAL, PLAYER_GOAL_STRATEGY_POINTS)
from .util import (vector_add, on_board, is_in_goal_hexe, element_to_tuple, normalize)


class State:
    """ class used to store information of pieces on board and player is playing
    """

    def __init__(self, playing_player, player_pieces):
        """ initialize a state
        :param playing_player: the  player is going to perform an action
        :param player_pieces: player's corresponding pieces
        """
        # playing_player
        self.playing_player = playing_player
        # [[(q, r), ...], ...]  list planned for project 2
        self.player_pieces_list = player_pieces
        # {(q, r): player, ...}
        self.pieces_player_dict = {piece: player
                                   for player in PLAYER_PLAYING_ORDER.values()
                                   for piece in self.player_pieces_list[player]}

        # action from previous state to current state
        self.action = None
        self.turns = 0
        self.finished_pieces = [0, 0, 0]

    def __repr__(self):
        """ str(State)
        :return: state.toString()
        """
        return str(self.player_pieces_list)

    def __hash__(self):
        """ hash(State)
        :return: hash value the state
        """
        # return hash(str(self))
        return hash(tuple(element_to_tuple(self.player_pieces_list)))

    def __eq__(self, other):
        """ check the equality of two states
        :param other: the other state
        :return: True if state has same board configuration. otherwise False
        """
        return set(self.pieces_player_dict.items()) == \
               set(other.pieces_player_dict.items())

    def copy(self):
        """ copy(state)
        :return: deepcopy of current copy
        """
        copyed = State(self.playing_player, EMPTY_BOARD)
        # copyed.pieces_player_dict = deepcopy(self.pieces_player_dict)
        # copyed.player_pieces_list = deepcopy(self.player_pieces_list)
        # copyed.player_pieces_list = self.player_pieces_list.copy()
        copyed.player_pieces_list = [i.copy() for i in self.player_pieces_list]
        copyed.pieces_player_dict = self.pieces_player_dict.copy()
        copyed.turns = self.turns
        copyed.finished_pieces = self.finished_pieces.copy()

        return copyed

    def all_next_action(self):
        res = []

        all_piece = self.all_pieces()

        player_pieces = self.player_pieces_list[self.playing_player]

        # if there is an exit action, then current state has only this
        # next state
        for piece in player_pieces:
            if is_in_goal_hexe(piece, self.playing_player):
                res.append((EXIT, piece))

        # foreach movable piece
        for piece in player_pieces:
            for delta in MOVE_DELTA:
                adj_piece = vector_add(piece, delta)

                # move action: on board & not occupied
                if on_board(adj_piece):
                    # not occupied
                    if adj_piece not in all_piece:
                        res.append((MOVE, (piece, adj_piece)))

                    # jump action: occupied adj piece & not occupied & on board
                    else:
                        # jump is just move same direction again
                        jump_piece = vector_add(adj_piece, delta)

                        # not occupied & on board
                        if (jump_piece not in all_piece) & \
                                on_board(jump_piece):
                            res.append((JUMP, (piece, jump_piece)))

        if len(res) == 0:
            return [(PASS, None)]
        else:
            # sort the output to process exit action first then jump then move
            return res

    def all_next_state(self):
        """ find all possible states
        :return: list of state after performed one action

        additional note: state's copy should inside each if condition as copy
        is an expensive operation
        """
        res = []

        all_piece = self.all_pieces()

        player_pieces = self.player_pieces_list[self.playing_player]

        # if there is an exit action, then current state has only this
        # next state
        for piece in player_pieces:
            if is_in_goal_hexe(piece, self.playing_player):
                # create next state
                next_state = self.copy()
                # update action
                next_state.update_action(EXIT, self.playing_player, piece)

                if next_state not in res:
                    res.append(next_state)

        # foreach movable piece
        # TODO change the next state preference order
        for delta in PLAYER_PREFERRED_MOVE_DELTA[self.playing_player]:
            for piece in player_pieces:
                adj_piece = vector_add(piece, delta)

                # move action: on board & not occupied
                if on_board(adj_piece):
                    # not occupied
                    if adj_piece not in all_piece:
                        # create next state
                        next_state = self.copy()
                        # update action
                        next_state.update_action(MOVE, self.playing_player,
                                                 piece, adj_piece)

                        if next_state not in res:
                            res.append(next_state)

                    # jump action: occupied adj piece & not occupied & on board
                    else:
                        # jump is just move same direction again
                        jump_piece = vector_add(adj_piece, delta)

                        # not occupied & on board
                        if (jump_piece not in all_piece) & \
                                on_board(jump_piece):
                            # create next state
                            next_state = self.copy()
                            # update action
                            next_state.update_action(JUMP, self.playing_player,
                                                     piece, jump_piece,
                                                     adj_piece)

                            if next_state not in res:
                                res.append(next_state)

        if len(res) == 0:
            next_state = self.copy()
            next_state.update_action(PASS, self.playing_player)
            return [next_state]
        else:
            # sort the output to process exit action first then jump then move
            # return sorted(res, key=lambda x: x.action[0])
            return res

    def update_action(self, action, previous_player, from_hexe=None, to_hexe=None,
                      jumped_hexe=None):
        """ update a state by action
        :param previous_player: player playing in previous state
        :param action: MOVE or JUMP or EXIT
        :param from_hexe: original hexe piece coordinate
        :param to_hexe: new hexe piece coordinate
        :param jumped_hexe: piece was jumped over
        """
        # update next playing player info
        self.playing_player = self.get_next_player_index()
        # update turns
        if previous_player == 2:
            self.turns += 1

        if action != PASS:
            # mov and jump
            if to_hexe is not None:
                # get player's original piece index
                from_index = self.player_pieces_list[previous_player].index(
                    from_hexe)
                # update player's new piece info over original piece
                self.player_pieces_list[previous_player][from_index] = to_hexe
                # update location of piece
                self.pieces_player_dict.pop(from_hexe)
                self.pieces_player_dict.update({to_hexe: previous_player})
                # update action
                self.action = (action, (from_hexe, to_hexe))

                # jump need to update jumped piece info
                if action == JUMP:
                    # jumped other player's piece
                    if jumped_hexe not in self.player_pieces_list[previous_player]:
                        # get jumped piece's player index
                        jumped_hexe_player = self.pieces_player_dict[jumped_hexe]
                        # update player's new piece info over original piece
                        self.player_pieces_list[jumped_hexe_player].remove(
                            jumped_hexe)
                        self.player_pieces_list[previous_player].append(jumped_hexe)

                        # update location of piece
                        self.pieces_player_dict.pop(jumped_hexe)
                        self.pieces_player_dict.update(
                            {jumped_hexe: previous_player})

            # exit
            else:
                # delete player's original piece info
                self.player_pieces_list[previous_player].remove(from_hexe)
                # delete location of piece
                self.pieces_player_dict.pop(from_hexe)
                # update action
                self.action = (action, from_hexe)
                # update player's score
                self.finished_pieces[previous_player] += 1
        # pass
        else:
            # update action
            self.action = (action, None)

    def get_next_player_index(self):
        if self.playing_player != 2:
            return self.playing_player + 1
        else:
            return 0

    def has_remaining_pieces(self):
        """ check whether a player has exited all player's pieces
        :return: True if player has no more pieces, otherwise False
        """
        return len(self.player_pieces_list[self.playing_player]) != 0

    def all_pieces(self):
        """ find all pieces on board
        :return: list of all pieces
        """
        return self.pieces_player_dict.keys()

    def get_winner(self):
        for player in range(0, N_PLAYER):
            if self.finished_pieces[player] == PLAYER_WIN_THRESHOLD:
                return player
        return None

    def is_terminate(self):
        return (self.turns == MAX_TURN) or (self.get_winner() is not None)

    def _cost_to_finish(self, player):
        """ h(state)
        :return: distance from current state to goal state
        """
        # hex distance right now
        total_dist = 0
        for i in self.player_pieces_list[player]:
            min_dist = 10
            for j in PLAYER_GOAL[player]:
                curr_dist = self._hex_dist(i, j)/2 + 1
                if curr_dist < min_dist:
                    min_dist = curr_dist
            total_dist += min_dist
        return total_dist

    def _necessary_cost_to_finish(self, player):
        """ first four pieces' avg distance to finish """
        total_dist = []
        for i in self.player_pieces_list[player]:
            min_dist = 10
            for j in PLAYER_GOAL[player]:
                curr_dist = self._hex_dist(i, j)/2 + 1
                if curr_dist < min_dist:
                    min_dist = curr_dist
            total_dist.append(min_dist)
        return sum(sorted(total_dist)[:PLAYER_WIN_THRESHOLD - self.finished_pieces[player]])

    def _cost_to_goal(self, player, goals):
        total_dist = 0
        for i in self.player_pieces_list[player]:
            min_dist = 10
            for j in goals[player]:
                curr_dist = self._hex_dist(i, j) / 2 + 1
                if curr_dist < min_dist:
                    min_dist = curr_dist
            total_dist += min_dist
        return total_dist

    def _pieces_cost_to_goal(self, pieces, goals):
        total_dist = 0

        if len(pieces) >= len(goals):
            froms = goals
            tos = pieces
        else:
            froms = pieces
            tos = goals

        for i in froms:
            min_dist = 10
            for j in tos:
                curr_dist = self._hex_dist(i, j) / 2 + 1
                if curr_dist < min_dist:
                    min_dist = curr_dist
            total_dist += min_dist
        return total_dist

    def _piece_cost_away_points(self, player, points):
        total_dist = 0
        for i in self.player_pieces_list[player]:
            min_dist = 10
            for j in points:
                curr_dist = self._hex_dist(i, j) / 2 + 1
                if curr_dist < min_dist:
                    min_dist = curr_dist
            total_dist += min_dist
        return total_dist

    def _piece_should_not_be_in(self, player_id, points):
        res = 0
        for piece in self.player_pieces_list[player_id]:
            if piece in points:
                res += 1
        return res

    def _piece_wander_cost(self, player_id):
        total_dist = 0

        for i in self.player_pieces_list[player_id]:
            min_dist = 10
            for j in PLAYER_GOAL_STRATEGY_POINTS[player_id]:
                curr_dist = self._hex_dist(i, j) / 2 + 1
                if curr_dist < min_dist:
                    min_dist = curr_dist
            total_dist += min_dist
        return total_dist

    @staticmethod
    def _hex_dist(hex1, hex2):
        return max(abs(hex1[0] - hex2[0]), abs((-hex1[0] - hex1[1]) - (-hex2[0] - hex2[1])),
                   abs(hex1[1] - hex2[1]))

    # TODO
    #  how to distinguish state with same score?
    #  how to switch eval for different phase?
    #  do we need to move the most not yet moved pieces?
    #  how about prefer kill strategy(the move can gain pieces)?
    #  seems blue can always win when all are maxn
    def evaluate(self, player_id, eval_function, player=None):
        from .Player import Player

        if eval_function == 1:
            return self._evaluate1(player_id)
        elif eval_function == 2:
            return self._evaluate2(player_id)
        elif eval_function == 3:
            return self._evaluate3(player_id)
        elif eval_function == 4:
            return self._evaluate4(player_id)
        elif eval_function == 5:
            return self._evaluate5(player_id)
        elif eval_function == 6:
            return self._evaluate6(player_id)
        elif eval_function == 7:
            return self._evaluate7(player_id)
        elif eval_function == 8:
            return self._evaluate8(player_id)
        elif eval_function == 9:
            return self._evaluate9(player_id, player)
        elif eval_function == 10:
            return self._evaluate10(player_id)
        elif eval_function == 11:
            return self._evaluate11(player_id, player)
        elif eval_function == 12:
            return self._evaluate12(player_id, player)
        elif eval_function == 13:
            # print(Player.PLAYER_INDEX)
            return self._evaluate13(Player.PLAYER_INDEX)
        # for completeness
        else:
            print("unsupported eval!!")
            return None

    # eval for move to customized goals
    def _evaluate11(self, player_id, player):
        # print(">>>>> in 111111111111111111")
        # print(player_id, player is None)
        if player_id == self.playing_player:
            # print(self.player_pieces_list[self.playing_player])
            pieces_not_in_strategies_points = []
            occupied_strategy_points = []

            for piece in self.player_pieces_list[self.playing_player]:
                if piece not in player.strategy_points:
                    pieces_not_in_strategies_points.append(piece)
                else:
                    occupied_strategy_points.append(piece)

            unoccupied_strategy_points = list(set(player.strategy_points) - set(occupied_strategy_points))

            # print(pieces_not_in_strategies_points, unoccupied_strategy_points)
            return - 0.1 * self._pieces_cost_to_goal(pieces_not_in_strategies_points, player.strategy_points_walls) + \
                    - 0.2 * self._pieces_cost_to_goal(pieces_not_in_strategies_points, unoccupied_strategy_points) + \
                   self.finished_pieces[self.playing_player] + len(self.player_pieces_list[self.playing_player])
        else:
            return self._evaluate1(player_id)

    def _evaluate12(self, player_id, player):
        # print(">>>>>")
        if player_id == self.playing_player:
            return - 0.1 * self._piece_wander_cost(player_id) + \
                   len(self.player_pieces_list[player_id]) - \
                    self._piece_should_not_be_in(self.playing_player, player.strategy_points_walls)
                   # + 0.25 * self._piece_cost_away_points(self.playing_player, player.strategy_traps)
        else:
            return self._evaluate1(player_id)

    def _evaluate13(self, player):
        # print(player)
        # feature dist to destination, number of player's pieces(include player and finished)
        # eval func = 1 * distance +  1 * num_all_pieces
        return - (self.finished_pieces[player] + len(self.player_pieces_list[player]))

    # first attempt for eval f()
    def _evaluate1(self, player):
        # feature dist to destination, number of player's pieces(include player and finished)
        # eval func = 1 * distance +  1 * num_all_pieces
        return - 0.1 * self._cost_to_finish(player) + \
               self.finished_pieces[player] + \
               len(self.player_pieces_list[player])

    # consider for solitary pattern
    def _evaluate7(self, player):
        my_pieces_num = len(self.player_pieces_list[player])

        if my_pieces_num == 0 and self.finished_pieces[player] < PLAYER_WIN_THRESHOLD:
            return -100
        elif self.finished_pieces[player] >= PLAYER_WIN_THRESHOLD:
            return 100

        return - 0.1 * self._cost_to_finish(player) + \
               self.finished_pieces[player] + my_pieces_num + \
               self.finished_pieces[player]

    def _evaluate8(self, player):
        """ xulin modification """
        TOTAL_DIST_MIN = 0
        TOTAL_DIST_MAX = 12
        NUM_PIECES_MIN = 0
        NUM_PIECES_MAX = 12

        my_pieces_num = len(self.player_pieces_list[player])

        if self.finished_pieces[player] >= PLAYER_WIN_THRESHOLD:
            return 100

        return -1 * normalize(self._necessary_cost_to_finish(player), TOTAL_DIST_MAX, TOTAL_DIST_MIN) + \
               normalize(self.finished_pieces[player] + my_pieces_num, NUM_PIECES_MAX, NUM_PIECES_MIN) + \
               2 * normalize(self.finished_pieces[player], 4, 0)

    def _evaluate9(self, player_id, player):
        """ xulin modification """

        my_pieces_num = len(self.player_pieces_list[player_id])

        if self.finished_pieces[player_id] >= PLAYER_WIN_THRESHOLD:
            return 100

        return - 0.1 * self._necessary_cost_to_finish(player_id) + \
               self.finished_pieces[player_id] + my_pieces_num + \
               self.finished_pieces[player_id] - \
               self._piece_should_not_be_in(self.playing_player, player.strategy_points_walls)

    def _evaluate10(self, player):
        """ xulin modification """
        TOTAL_DIST_MIN = 0
        TOTAL_DIST_MAX = 12
        NUM_PIECES_MIN = 0
        NUM_PIECES_MAX = 12

        my_pieces_num = len(self.player_pieces_list[player])

        if self.finished_pieces[player] >= PLAYER_WIN_THRESHOLD:
            return 120

        return - 0.1 * self._cost_to_finish(player) + \
               self.finished_pieces[player] + my_pieces_num + \
               self.finished_pieces[player] + 20

    # normalize for easier weight discovery; consider solitary pattern
    def _evaluate2(self, player):
        TOTAL_DIST_MIN = 0
        TOTAL_DIST_MAX = 12
        NUM_PIECES_MIN = 0
        NUM_PIECES_MAX = 12
        TOTAL_NUM_PIECES_AROUND_MIN = 0
        # TODO solitary max score {1:..., 2:..., 3:..., }
        ONE_NUM_PIECES_AROUND_MAX = 6
        my_pieces_num = len(self.player_pieces_list[player])

        return -1 * normalize(self._cost_to_finish(player), TOTAL_DIST_MAX, TOTAL_DIST_MIN) + \
               normalize(self.finished_pieces[player] + my_pieces_num, NUM_PIECES_MAX, NUM_PIECES_MIN) + \
               normalize(self._solitary_score1(player), 10, TOTAL_NUM_PIECES_AROUND_MIN)

    # average dist to solve unwilling to attack to increase total dist
    def _evaluate3(self, player):
        TOTAL_DIST_MIN = 0
        TOTAL_DIST_MAX = 12
        NUM_PIECES_MIN = 0
        NUM_PIECES_MAX = 12
        TOTAL_NUM_PIECES_AROUND_MIN = 0
        # TODO solitary max score {1:..., 2:..., 3:..., }
        ONE_NUM_PIECES_AROUND_MAX = 6
        my_pieces_num = len(self.player_pieces_list[player])

        return -1 * normalize(self._cost_to_finish(player), TOTAL_DIST_MAX, TOTAL_DIST_MIN) / my_pieces_num + \
               normalize(self.finished_pieces[player] + my_pieces_num, NUM_PIECES_MAX, NUM_PIECES_MIN) + \
               normalize(self._solitary_score1(player), 10, TOTAL_NUM_PIECES_AROUND_MIN)

    # add finish score feature to solve unwilling to exit even though lot of
    # pieces can exit;
    # solve when evaluating self, has eaten one opponent's last remaining
    # pieces, cause divide by zero -> lose reward and winning reward +/- 12
    def _evaluate4(self, player):
        TOTAL_DIST_MIN = 0
        TOTAL_DIST_MAX = 12
        NUM_PIECES_MIN = 0
        NUM_PIECES_MAX = 12
        TOTAL_NUM_PIECES_AROUND_MIN = 0
        # TODO solitary max score {1:..., 2:..., 3:..., }
        ONE_NUM_PIECES_AROUND_MAX = 6
        MIN_SCORE = 0
        MAX_SCORE = 4

        my_pieces_num = len(self.player_pieces_list[player])

        if my_pieces_num == 0 and self.finished_pieces[player] < MAX_SCORE:
            return -12
        elif self.finished_pieces[player] >= MAX_SCORE:
            return 12
        else:
            return -1 * normalize(self._cost_to_finish(player), TOTAL_DIST_MAX, TOTAL_DIST_MIN) / my_pieces_num + \
                   normalize(self.finished_pieces[player] + my_pieces_num, NUM_PIECES_MAX, NUM_PIECES_MIN) + \
                   normalize(self._solitary_score1(player), 10, TOTAL_NUM_PIECES_AROUND_MIN) + \
                   normalize(self.finished_pieces[player], MAX_SCORE, MIN_SCORE)

    # solitary is not good for too many remaining pieces so we have a weight fo solitary
    def _evaluate5(self, player):
        TOTAL_DIST_MIN = 0
        TOTAL_DIST_MAX = 12
        NUM_PIECES_MIN = 0
        NUM_PIECES_MAX = 12
        TOTAL_NUM_PIECES_AROUND_MIN = 0
        # TODO solitary max score {1:..., 2:..., 3:..., }
        ONE_NUM_PIECES_AROUND_MAX = 6
        MIN_SCORE = 0
        MAX_SCORE = 4

        my_pieces_num = len(self.player_pieces_list[player])

        if my_pieces_num == 0 and self.finished_pieces[player] < MAX_SCORE:
            return -12
        elif self.finished_pieces[player] >= MAX_SCORE:
            return 12
        else:
            if my_pieces_num <= 5:
                w3 = 1
            else:
                w3 = 0.5

            return -1 * normalize(self._cost_to_finish(player), TOTAL_DIST_MAX, TOTAL_DIST_MIN) / my_pieces_num + \
                   normalize(self.finished_pieces[player] + my_pieces_num, NUM_PIECES_MAX, NUM_PIECES_MIN) + \
                   w3 * normalize(self._solitary_score1(player), 10, TOTAL_NUM_PIECES_AROUND_MIN) + \
                   normalize(self.finished_pieces[player], MAX_SCORE, MIN_SCORE)

    # as we arrive goals in solidarity, we can exit one pieces immediately
    def _evaluate6(self, player):
        TOTAL_DIST_MIN = 0
        TOTAL_DIST_MAX = 12
        NUM_PIECES_MIN = 0
        NUM_PIECES_MAX = 12
        TOTAL_NUM_PIECES_AROUND_MIN = 0
        # TODO solitary max score {1:..., 2:..., 3:..., }
        ONE_NUM_PIECES_AROUND_MAX = 6
        MIN_SCORE = 0
        MAX_SCORE = 4

        my_pieces_num = len(self.player_pieces_list[player])

        if my_pieces_num == 0 and self.finished_pieces[player] < MAX_SCORE:
            return -12
        elif self.finished_pieces[player] >= MAX_SCORE:
            return 12
        else:
            if my_pieces_num <= 4:
                w3 = 0.5
            else:
                w3 = 0

            return -1 * normalize(self._cost_to_finish(player), TOTAL_DIST_MAX, TOTAL_DIST_MIN) / my_pieces_num + \
                   normalize(self.finished_pieces[player] + my_pieces_num, NUM_PIECES_MAX, NUM_PIECES_MIN) + \
                   w3 * normalize(self._solitary_score1(player), 10, TOTAL_NUM_PIECES_AROUND_MIN) + \
                   2 * normalize(self.finished_pieces[player], MAX_SCORE, MIN_SCORE)

    # number of friends
    def _solitary_score1(self, player):
        num_friends = 0
        for my_hexe in self.player_pieces_list[player]:
            num_friends += self._get_hex_around_num(my_hexe, player)
        return num_friends

    def _get_hex_around(self, my_hexe, player):
        res = []
        for delta in MOVE_DELTA:
            move_to = vector_add(my_hexe, delta)

            if on_board(move_to) and self.pieces_player_dict[move_to] == player:
                res.append(move_to)
        return res

    def _get_hex_around_num(self, my_hexe, player):
        count = 0
        for delta in MOVE_DELTA:
            move_to = vector_add(my_hexe, delta)
            try:
                if on_board(move_to) and self.pieces_player_dict[move_to] == player:
                    count += 1
            except KeyError:
                pass
        return count

    # total dist between friends
    def _solidarity_score2(self, player):
        total_dist = 0
        for i in range(len(self.player_pieces_list[player])):
            for j in range(i + 1, len(self.player_pieces_list[player])):
                total_dist += self._hex_dist(self.player_pieces_list[player][i],
                                             self.player_pieces_list[player][j])
        return total_dist

    def get_key(self):
        """  """
        return tuple(element_to_tuple(self.player_pieces_list)) + tuple(self.finished_pieces)

    def is_playing_player_finished(self):
        """
        check if player
        :return:
        """
        return self.finished_pieces[self.playing_player] == PLAYER_WIN_THRESHOLD

    def playing_player_has_pieces(self):
        """
        check if player has pieces left
        :return: true if player still has pieces
        """
        return len(self.player_pieces_list[self.playing_player]) != 0

    def is_binary(self):
        """ check whether there are only 2 players """
        return [len(self.player_pieces_list[player]) != 0 for player in range(0, N_PLAYER)].count(True) == 2

    def is_single(self):
        """ check whether there is only 1 player left """
        return [len(self.player_pieces_list[player]) != 0 for player in range(0, N_PLAYER)].count(True) == 1

    def player_has_win_chance(self, player):
        return len(self.player_pieces_list[player]) + self.finished_pieces[player] >= PLAYER_WIN_THRESHOLD

    def is_player_knock_out(self, player):
        """
        check if the given player has no pieces left
        :param player: the player to be checked
        :return: true if the player has no pieces left
        """
        return len(self.player_pieces_list[player]) == 0

    # def is_other_player_finished(self):
