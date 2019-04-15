"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-11 22:33:05
Description: paranoid agent with alpha-beta pruning
             https://project.dke.maastrichtuniversity.nl/games/files/phd/Nijssen_thesis.pdf
"""
from Agent import Agent


class ParanoidAgent(Agent):
    SEARCH_DEPTH = 7

    def __init__(self, board, depth=SEARCH_DEPTH):
        self.board = board  # copy board for ai search
        self.depth = depth

    def get_next_move(self):
        next_move, _ = self.paranoid(self.board.get_current_state(), self.depth, self.board.get_playing_player(),
                                     Agent.NEGATIVE_INFINITY, Agent.POSITIVE_INFINITY)

        return next_move

    def paranoid(self, s, depth, cur_player, alpha, beta):
        # s:cur state

        next_move = None

        if self.board.is_terminate(s) or depth <= 0:
            # if currentPlayer == rootPlayer then
            if self.board.is_my_player_playing(cur_player):
                return next_move, self.board.evaluate_player_state(cur_player, s)
            else:
                return next_move, -self.board.evaluate_player_state(cur_player, s)

        possible_moves = self.board.get_all_moves(s)

        for possible_move in possible_moves:
            next_state = self.board.get_next_state(s, possible_move)
            next_player = self.board.get_cur_player(next_state)

            # TODO max & np.max
            # if currentPlayer == rootPlayer or nextPlayer == rootPlayer then
            #     α = max(α, –ALPHABETA(c, depth–1, nextPlayer, −β, −α));
            # else
            #     α = max(α, ALPHABETA(c, depth–1, nextPlayer, α, β));
            # end if
            if self.board.is_my_player_playing(cur_player):
                _, alpha_next = self.paranoid(next_state, next_player, depth - 1, -beta, -alpha)
            else:
                _, alpha_next = self.paranoid(next_state, next_player, depth - 1, alpha, beta)
            # TODO check my logic here
            if -alpha_next > alpha:
                alpha = -alpha_next
                next_move = possible_move
            # alpha = max(alpha, -alpha_next)

            if alpha >= beta:
                return next_move, beta

        return next_move, alpha



