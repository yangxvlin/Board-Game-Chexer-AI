"""
Author:      XuLin Yang
Student id:  904904
Date:        
Description: 
"""

from deep_dark_fantastic_boys_next_door.Constants import (MAX_TURN,
                                                          PLAYER_WIN_THRESHOLD)
from deep_dark_fantastic_boys_next_door.util import (initial_state)

WIN_REWARD = 12
LOSE_REWARD = -12
DRAW_REWARD = 0
CATCH_PIECE_REWARD = 1
LOSE_PIECE_REWARD = 1


class GameEnv:

    def __init__(self):
        self.states_history = [initial_state()]

    def reset(self):
        self.states_history = [initial_state()]
        return self.states_history[-1]

    def step(self, players_next_state):

        is_done = False
        player_reward = [0, 0, 0]

        for player, player_next_state in enumerate(players_next_state):
            # assert player == player_next_state.playing_player
            # add to history
            self.states_history.append(player_next_state)

            # one player win
            if player_next_state.is_player_finished():
                player_reward = [LOSE_REWARD, LOSE_REWARD, LOSE_REWARD]
                player_reward[player] = WIN_REWARD
                is_done = True
                return player_reward, is_done

            # calculate player gain/lose piece rewards
            player_reward[player] += \
                player_next_state.finished_pieces[player] + \
                len(player_next_state.player_pieces_list[player]) - PLAYER_WIN_THRESHOLD
            # no piece to keeps fighting == Lose
            if len(player_next_state.player_pieces_list[player]) == 0:
                player_reward[player] = LOSE_REWARD
            # print(player,  player_next_state.finished_pieces[player],
            #     len(player_next_state.player_pieces_list[player]))

        # turn ends
        if players_next_state[0].turns == MAX_TURN:
            is_done = True
        # print(player_reward)
        return player_reward, is_done