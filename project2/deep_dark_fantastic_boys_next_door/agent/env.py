"""
Author:      XuLin Yang
Student id:  904904
Date:        
Description: 
"""

from deep_dark_fantastic_boys_next_door.Constants import (MAX_TURN,
    PLAYER_WIN_THRESHOLD, MOVE, PASS, EXIT, JUMP)
from deep_dark_fantastic_boys_next_door.util import (initial_state, calculate_jumped_hexe)

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

    def update(self, state, action):
        # generate state | action
        next_state = state.copy()

        if action[0] == PASS:
            assert action[1] is None
            next_state.update_action(action[0], state.playing_player)
        elif action[0] == MOVE:
            next_state.update_action(action[0], state.playing_player,
                                     action[1][0], action[1][1])
        elif action[0] == EXIT:
            next_state.update_action(action[0], state.playing_player,
                                     action[1])
        else:
            jumped_hexe = calculate_jumped_hexe(action[1][0], action[1][1])
            next_state.update_action(action[0], state.playing_player,
                                     action[1][0], action[1][1], jumped_hexe)

        return next_state

    def step(self, players_next_states):

        is_done = False
        player_reward = [0, 0, 0]

        for player, player_next_state in enumerate(players_next_states):
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
        if players_next_states[0].turns == MAX_TURN:
            is_done = True
            return [0, 0, 0], is_done
        # print(player_reward)
        return player_reward, is_done
