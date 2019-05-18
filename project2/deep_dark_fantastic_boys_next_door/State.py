"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-14 14:32:08
Description: State to store information about the environment
"""
import random
import numpy as np
from .Constants import (MOVE_DELTA, PLAYER_PREFERRED_MOVE_DELTA, MOVE, JUMP,
                        EXIT, PASS, PLAYER_PLAYING_ORDER, EMPTY_BOARD,
                        PLAYER_WIN_THRESHOLD, MAX_TURN, N_PLAYER, PLAYER_GOAL,
                        PLAYER_GOAL_STRATEGY_POINTS, BLUE_PLAYER_INDEX)
from .util import (vector_add, on_board, is_in_goal_hexe, element_to_tuple,
                   normalize)


class State:
    """
    class used to store information of pieces on board and player is playing
    """

    def __init__(self, playing_player, player_pieces):
        """
        initialize a state
        :param playing_player: the  player is going to perform an action
        :param player_pieces: player's corresponding pieces
        """
        # playing_player
        self.playing_player = playing_player
        # mapping between player with their own pieces
        # [[(q, r), ...], ...]
        self.player_pieces_list = player_pieces
        # mapping between piece with its owner
        # {(q, r): player, ...}
        self.pieces_player_dict = {piece: player
                                   for player in PLAYER_PLAYING_ORDER.values()
                                   for piece in self.player_pieces_list[player]}
        # action from previous state to current state
        self.action = None
        # turns played by player up to the current state
        self.turns = 0
        # number of pieces finished by each player up to current state
        self.finished_pieces = [0, 0, 0]

    def __repr__(self):
        """
        str(State)
        :return: state.toString()
        """
        return str(self.player_pieces_list)

    def __hash__(self):
        """
        hash(State)
        :return: hash value the state
        """
        # return hash(str(self))
        return hash(tuple(element_to_tuple(self.player_pieces_list)))

    def __eq__(self, other):
        """
        check the equality of two states
        :param other: the other state
        :return: True if state has same board configuration. otherwise False
        """
        return set(self.pieces_player_dict.items()) == \
               set(other.pieces_player_dict.items())

    def copy(self):
        """
        copy(state)
        :return: shallow copy of state's attribute
        """
        copyed = State(self.playing_player, EMPTY_BOARD)
        copyed.player_pieces_list = [i.copy() for i in self.player_pieces_list]
        copyed.pieces_player_dict = self.pieces_player_dict.copy()
        copyed.turns = self.turns
        copyed.finished_pieces = self.finished_pieces.copy()

        return copyed

    def all_next_action(self):
        """
        :return: list of possible actions can be taken by the player
        """
        res = []

        all_piece = self.all_pieces()

        player_pieces = self.player_pieces_list[self.playing_player]

        # exit actions
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
                        if (jump_piece not in all_piece) & on_board(jump_piece):
                            res.append((JUMP, (piece, jump_piece)))

        if len(res) == 0:
            return [(PASS, None)]
        else:
            return res

    def all_next_state(self):
        """
        find all possible states
        :return: list of state after performed one action

        additional note: return the next state ordered by player's preferred
        move action order to ensure choices are sort by the distance to player
        finish goal order; shuffle the candidate player pieces to avoid agent
        always choose the same next state when choices are with same evaluation
        value.
        """
        res = []
        all_piece = self.all_pieces()
        # inplace shuffle requires a copy
        player_pieces = self.player_pieces_list[self.playing_player].copy()
        random.shuffle(player_pieces)

        # state with exit action
        for piece in player_pieces:
            if is_in_goal_hexe(piece, self.playing_player):
                # create next state
                next_state = self.copy()
                # update action
                next_state.update_action(EXIT, self.playing_player, piece)
                if next_state not in res:
                    res.append(next_state)

        # foreach movable piece
        # the order of for loop is discussed in the function comments
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
                        if (jump_piece not in all_piece) & on_board(jump_piece):
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
            return res

    def update_action(self, action, previous_player, from_hexe=None,
                      to_hexe=None, jumped_hexe=None):
        """
        update a state by action
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
                    if jumped_hexe not in self.player_pieces_list[
                            previous_player]:
                        # get jumped piece's player index
                        jumped_hexe_player = self.pieces_player_dict[
                            jumped_hexe]
                        # update player's new piece info over original piece
                        self.player_pieces_list[jumped_hexe_player].remove(
                            jumped_hexe)
                        self.player_pieces_list[previous_player].append(
                            jumped_hexe)

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
        """ 
        :return: next player's index in [0, 1, 2] for red, green, blue 
        respectively 
        """
        if self.playing_player != BLUE_PLAYER_INDEX:
            # +1 to get next player
            return self.playing_player + 1
        else:
            # blue player (index: 2) next player is red player (index: 0)
            return 0

    def has_remaining_pieces(self):
        """
        check whether a player has exited all player's pieces
        :return: True if player has no more pieces, otherwise False
        """
        return len(self.player_pieces_list[self.playing_player]) != 0

    def all_pieces(self):
        """
        find all pieces on board
        :return: list of all pieces
        """
        return self.pieces_player_dict.keys()

    def get_winner(self):
        """
        When a player has exited 4 pieces, then this player is the winner.
        :return: player if player is the winner, None otherwise
        """
        for player in range(0, N_PLAYER):
            if self.finished_pieces[player] == PLAYER_WIN_THRESHOLD:
                return player
        return None

    def is_playing_player_finished(self):
        """
        check if player has 4 exited pieces
        :return:
        """
        return self.finished_pieces[self.playing_player] == PLAYER_WIN_THRESHOLD

    def playing_player_has_pieces(self):
        """
        check if player has pieces left
        :return: true if player still has pieces
        """
        return len(self.player_pieces_list[self.playing_player]) != 0

    def _get_player_all_pieces_num(self, player_id):
        """
        :param player_id: player index to calculate distances for
        :return: exited pieces num + remaining pieces num
        """
        return len(self.player_pieces_list[player_id]) + \
               self.finished_pieces[player_id]

    def player_has_win_chance(self, player_id):
        """
        :param player_id: player index to calculate distances for
        :return: player has no winning chance when less than 4 pieces
        """
        return self._get_player_all_pieces_num(player_id) >= \
               PLAYER_WIN_THRESHOLD

    def is_player_knock_out(self, player):
        """
        check if the given player has no pieces left
        :param player: the player to be checked
        :return: true if the player has no pieces left
        """
        return len(self.player_pieces_list[player]) == 0

    def snap(self):
        """
        adapt from provided game.py and modified by ourselves
        """
        return frozenset(self.pieces_player_dict), self.playing_player

    def is_terminate(self, player):
        """
        a game is terminated when have reached 256 turns or has one winner in
        the game or board configure occurred 4 times
        :param player: Player object holds board configure counter
        :return: True if a game is terminated, False otherwise
        """
        return (self.turns == MAX_TURN) or \
               (self.get_winner() is not None) or \
               (player.states_counter[self.snap()] >= PLAYER_WIN_THRESHOLD)

    def _pieces_cost_to_points(self, pieces, points, to_array=False):
        """
        calculate the minimum summed distance for all pieces to reach in one of
        the points
        :param pieces: list of hexes to move
        :param points: list of hexes to arrive
        :param to_array: return distance for each piece in numpy.array or
                         summed value
        :return: hexe distance(s)
        """
        # hex distance right now
        total_dist = np.array([])
        for i in pieces:
            min_dist = float("inf")
            for j in points:
                # /2 +1 to let dist() be admissible
                curr_dist = self._hex_dist(i, j) / 2 + 1
                if curr_dist < min_dist:
                    min_dist = curr_dist

            total_dist = np.append(total_dist, min_dist)
        if to_array:
            return total_dist
        else:
            return np.sum(total_dist)

    def _cost_to_finish(self, player_id):
        """
        :param player_id: player index to calculate distances for
        :return: distance from current state to goal state
        """
        return self._pieces_cost_to_points(self.player_pieces_list[player_id],
                                           PLAYER_GOAL[player_id])

    def _necessary_cost_to_finish(self, player_id):
        """
        minimum distance to finish
        :param player_id: player index to calculate distances for
        :return: minimum cost for player
        """
        return np.sum(np.sort(
            self._pieces_cost_to_points(self.player_pieces_list[player_id],
                                        PLAYER_GOAL[player_id], True))
                      [:PLAYER_WIN_THRESHOLD - self.finished_pieces[player_id]]
                      )

    def _pieces_cost_to_goal(self, pieces, goals):
        """
        used when we want to move one piece to one goal
        :param pieces: pieces to be moved
        :param goals: goal hexe to have pieces moved in
        :return: distance for each pieces to reach a goal respectively
        """
        # when pieces are more than goals, associate a goal with pieces
        if len(pieces) >= len(goals):
            froms = goals
            tos = pieces
        # when pieces are less than goals, associate a piece with a closest goal
        else:
            froms = pieces
            tos = goals

        return self._pieces_cost_to_points(froms, tos)

    def _piece_should_not_be_in(self, player_id, points):
        """
        used when we don't want pieces in certain points
        :param player_id: player index to calculate distances for
        :param points: points we don't want pieces to be in
        :return: number of pieces in unwanted points
        """
        res = 0
        for piece in self.player_pieces_list[player_id]:
            if piece in points:
                res += 1
        return res

    def _piece_wander_cost(self, player_id):
        """
        used when only want to move less than 4 pieces to goal strategy points
        instead of 4 goal points
        :param player_id: player index to calculate distances for
        :return: distance to player's two exit strategy points
        """
        return self._pieces_cost_to_points(self.player_pieces_list[player_id],
                                       PLAYER_GOAL_STRATEGY_POINTS[player_id])

    @staticmethod
    def _hex_dist(hex1, hex2):
        """
        modified from red blob game
        :param hex1: first hexe piece
        :param hex2: second hexe piece
        :return: hexe distance between two pieces
        """
        return max(abs(hex1[0] - hex2[0]),
                   abs((-hex1[0] - hex1[1]) - (-hex2[0] - hex2[1])),
                   abs(hex1[1] - hex2[1])
                   )

    def evaluate(self, player_id, eval_function, player=None):
        """
        an interface provided to outside object
        :param player_id: player index to evaluate for
        :param eval_function: evaluation function identifier
        :param player: some player object attribute required for certain
                       evaluate function
        :return: evaluate value for certain player, larger means better
        """
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
            return self._evaluate13(Player.PLAYER_INDEX)
        # for completeness
        else:
            print("unsupported eval!!")
            return None

    def _evaluate1(self, player_id):
        """
        :param player_id: player index to evaluate for
        :return: evaluate value considering distance to exit and owning pieces
                 num
        """
        return - 0.1 * self._cost_to_finish(player_id) + \
               self._get_player_all_pieces_num(player_id)

    def _evaluate9(self, player_id, player):
        """
        :param player_id: player index to evaluate for
        :param player: some player object attribute required for certain
                       evaluate function
        :return: evaluate value considering distance to exit and owning pieces
                 num and points should not occupied
        """
        # win immediately
        if self.finished_pieces[player_id] >= PLAYER_WIN_THRESHOLD:
            return 100

        return - 0.1 * self._necessary_cost_to_finish(player_id) + \
               self._get_player_all_pieces_num(player_id) + \
               self.finished_pieces[player_id] - \
               self._piece_should_not_be_in(self.playing_player,
                                            player.strategy_points_walls)

    def _evaluate11(self, player_id, player):
        """
        :param player_id: player index to evaluate for
        :param player: some player object attribute required for certain
                       evaluate function
        :return: evaluate value for root player considering move pieces to
                 strategy points; otherwise follow normal game strategy
        """
        # win immediately
        if self.finished_pieces[player_id] >= PLAYER_WIN_THRESHOLD:
            return 100

        if player_id == self.playing_player:
            pieces_not_in_strategies_points = []
            occupied_strategy_points = []

            # filter pieces
            for piece in self.player_pieces_list[self.playing_player]:
                if piece not in player.strategy_points:
                    pieces_not_in_strategies_points.append(piece)
                else:
                    occupied_strategy_points.append(piece)

            unoccupied_strategy_points = list(
                set(player.strategy_points) - set(occupied_strategy_points))

            return - 0.1 * self._pieces_cost_to_goal(
                    pieces_not_in_strategies_points,
                    player.strategy_points_walls) + \
                   - 0.2 * self._pieces_cost_to_goal(
                    pieces_not_in_strategies_points,
                    unoccupied_strategy_points) + \
                   2 * self._get_player_all_pieces_num(player_id)
        else:
            return self._evaluate1(player_id)

    def _evaluate12(self, player_id, player):
        """
        :param player_id: player index to evaluate for
        :param player: some player object attribute required for certain
                       evaluate function
        :return: evaluate value for player to move several pieces to goal and
                 not exit and let pieces in the unwanted points to leave
        """
        if player_id == self.playing_player:
            return - 0.1 * self._piece_wander_cost(player_id) + \
                   len(self.player_pieces_list[player_id]) - \
                   self._piece_should_not_be_in(self.playing_player,
                                                player.strategy_points_walls)
        else:
            return self._evaluate1(player_id)

    def _evaluate13(self, player_id):
        """
        :param player_id: player index to evaluate for
        :return: evaluate value for player to minimize given player's pieces num
        """
        return - self._get_player_all_pieces_num(player_id)

# ************************* unused function but worth a look ******************

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
        """
        :return: the key representation of the state
        """
        return tuple(element_to_tuple(self.player_pieces_list)) + \
               tuple(self.finished_pieces)

    def is_binary(self):
        """
        :return: True if there are only 2 players
        """
        return [len(self.player_pieces_list[player]) != 0 for player in range(0, N_PLAYER)].count(True) == 2

    def is_single(self):
        """
        :return: True if there are only 1 player
        """
        return [len(self.player_pieces_list[player]) != 0 for player in range(0, N_PLAYER)].count(True) == 1
