"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-5-18 20:23:00
Description: agent used for reinforcement learning by policy learning
modify from https://github.com/dennybritz/reinforcement-learning/blob/master/TD/Q-Learning%20Solution.ipynb
if want to study https://www.cse.unsw.edu.au/~cs9417ml/RL1/algorithms.html
terminology: "round" == "turn"
"""

import numpy as np
import sys
import itertools
from deep_dark_fantastic_boys_next_door.Constants import (PLAYER_PLAYING_ORDER)


class QLearningAgent:

    def __init__(self):
        # {state: {action: v(s) "which is value"}}
        # TODO should we use Ordered Dict for action?
        self.players_q_table = {player: {}
                                for player in PLAYER_PLAYING_ORDER.values()}

    def make_epsilon_greedy_policy(self, Q, epsilon, nA):
        """
        Creates an epsilon-greedy policy based on a given Q-function and epsilon.

        Args:
            Q: A dictionary that maps from state -> action-values.
                Each value is a numpy array of length nA (see below)
            epsilon: The probability to select a random action. Float between 0 and 1.
            nA: Number of actions in the environment.

        Returns:
            A function that takes the observation as an argument and returns
            the probabilities for each action in the form of a numpy array of length nA.
        """

        def policy_fn(observation):
            A = np.ones(nA, dtype=float) * epsilon / nA
            assert len(Q[observation].values()) > 0
            best_action = np.argmax(Q[observation].values())
            A[best_action] += (1.0 - epsilon)
            return A

        return policy_fn

    def choose_action(self, player, player_round_i_state, player_round_i_state_key, epsilon):
        player_round_i_actions = player_round_i_state.all_next_action()
        # initialize Q(s, a) in q_table
        self.initialize_state_action_in_q_table(player, player_round_i_state_key, player_round_i_actions)
        assert len(self.players_q_table[player][player_round_i_state_key].keys()) > 0
        assert len(player_round_i_actions) == len(self.players_q_table[player][player_round_i_state_key].keys())

        # terminology: player's q_table = self.players_q_table[state.playing_player]
        # make an action based on policy
        player_policy = self.make_epsilon_greedy_policy(
            self.players_q_table[player], epsilon, len(player_round_i_actions))
        # Take a step for player
        player_round_i_action_probs = player_policy(player_round_i_state_key)
        player_round_i_action_index = np.random.choice(
            np.arange(len(player_round_i_action_probs)),
            p=player_round_i_action_probs)
        player_round_i_action = list(self.players_q_table[player][player_round_i_state_key].keys())[player_round_i_action_index]
        return player_round_i_action

    def generate_round(self, state, epsilon, env):
        # *********************** player0 *****************************
        player0_round_i_state = state
        player0_round_i_state_key = player0_round_i_state.get_key()
        player0_round_i_action = self.choose_action(0, player0_round_i_state, player0_round_i_state_key, epsilon)

        # *********************** player1 *****************************
        player1_round_i_state = env.update(player0_round_i_state, player0_round_i_action)
        player1_round_i_state_key = player1_round_i_state.get_key()
        player1_round_i_action = self.choose_action(1, player1_round_i_state, player1_round_i_state_key, epsilon)

        # *********************** player2 *****************************
        player2_round_i_state = env.update(player1_round_i_state, player1_round_i_action)
        player2_round_i_state_key = player2_round_i_state.get_key()
        player2_round_i_action = self.choose_action(2, player2_round_i_state, player2_round_i_state_key, epsilon)

        return player0_round_i_state, player0_round_i_state_key, player0_round_i_action, \
               player1_round_i_state, player1_round_i_state_key, player1_round_i_action, \
               player2_round_i_state, player2_round_i_state_key, player2_round_i_action

    def initialize_state_action_in_q_table(self, player, state_key, actions):
        if state_key not in self.players_q_table[player]:
            self.players_q_table[player][state_key] = {}
            # self.players_q_table[player][state_key] = OrderedDict()
        # Q(s, a) = 0
        for action in actions:
            if action not in self.players_q_table[player][state_key]:
                self.players_q_table[player][state_key][action] = 0

    def q_learning(self, env, cur_batch, num_batch, num_episodes=1, discount_factor=1.0, alpha=0.5, epsilon=0.1):
        """
            Q-Learning algorithm: Off-policy TD control. Finds the optimal greedy policy
            while following an epsilon-greedy policy

            Args:
                env: OpenAI environment.
                num_episodes: Number of episodes to run for.
                discount_factor: Gamma discount factor.
                alpha: TD learning rate.
                epsilon: Chance to sample a random action. Float between 0 and 1.

            Returns:
                A tuple (Q, episode_lengths).
                Q is the optimal action-value function, a dictionary mapping state -> action values.
                stats is an EpisodeStats object with two numpy arrays for episode_lengths and episode_rewards.
            """
        for i_episode in range(num_episodes):
            # Print out which episode we're on, useful for debugging.
            if (i_episode + 1) % 5 == 0:
                print("\rEpisode {}/{}#Batch {}/{}\n".format(i_episode + 1, num_episodes, cur_batch, num_batch),
                      end="")
                sys.stdout.flush()

            # Reset the environment and pick the first action
            state = env.reset()

            # One step in the environment
            for i in itertools.count():
                # first turn
                if i == 0:
                    player0_round_i_state, player0_round_i_state_key, player0_round_i_action, \
                    player1_round_i_state, player1_round_i_state_key, player1_round_i_action, \
                    player2_round_i_state, player2_round_i_state_key, player2_round_i_action = \
                    self.generate_round(state, epsilon, env)
                    assert player0_round_i_state.playing_player == 0
                    assert player1_round_i_state.playing_player == 1
                    assert player2_round_i_state.playing_player == 2

                # j = i+1
                player0_round_j_state = env.update(player2_round_i_state, player2_round_i_action)
                player0_round_j_state, player0_round_j_state_key, player0_round_j_action, \
                player1_round_j_state, player1_round_j_state_key, player1_round_j_action, \
                player2_round_j_state, player2_round_j_state_key, player2_round_j_action = \
                    self.generate_round(player0_round_j_state, epsilon, env)
                assert player0_round_j_state.playing_player == 0
                assert player1_round_j_state.playing_player == 1
                assert player2_round_j_state.playing_player == 2

                # ********************* get turn census ***********************
                [player0_reward, player1_reward, player2_reward], done = \
                    env.step([player0_round_i_state, player1_round_i_state, player2_round_i_state])

                # self.print_player_q_table()
                # ********************* update q table ************************
                self.update_player_q_table(0,
                                           player0_round_i_state_key,
                                           player0_round_j_state_key,
                                           player0_round_i_action,
                                           player0_reward,
                                           discount_factor, alpha)
                self.update_player_q_table(1,
                                           player1_round_i_state_key,
                                           player1_round_j_state_key,
                                           player1_round_i_action,
                                           player1_reward,
                                           discount_factor, alpha)
                self.update_player_q_table(2,
                                           player2_round_i_state_key,
                                           player2_round_j_state_key,
                                           player2_round_i_action,
                                           player2_reward,
                                           discount_factor, alpha)

                # ******************* next round in episodes ******************
                if done:
                    # rewards = [player0_reward, player1_reward, player2_reward]
                    # if 12 in rewards:
                    #     print("one winner", rewards)
                    # else:
                    #     print("draw", rewards)
                    break
                if i >= 256:
                    print("t >= 256")

                # swap i j; to process round j as next turn
                player0_round_i_state, player0_round_i_state_key, player0_round_i_action, \
                player1_round_i_state, player1_round_i_state_key, player1_round_i_action, \
                player2_round_i_state, player2_round_i_state_key, player2_round_i_action = \
                    player0_round_j_state, player0_round_j_state_key, player0_round_j_action, \
                    player1_round_j_state, player1_round_j_state_key, player1_round_j_action, \
                    player2_round_j_state, player2_round_j_state_key, player2_round_j_action

    def update_player_q_table(self, playing_player, state_key, next_state_key, action, reward, discount_factor, alpha):
        # TD Update
        # Q(s, a) <- Q(s, a) + alpha * [reward + gamma * max(Q(s', a' for all a')) - Q(s, a)]
        #                                                      ^ note for s' in this case, we need player#X's new round state to be next state for player#X in this case
        assert len(self.players_q_table[playing_player][next_state_key].values()) > 0
        assert len(self.players_q_table[playing_player][state_key].values()) > 0

        # max(Q(s', a' for all a'))
        best_next_action_index = np.argmax(self.players_q_table[playing_player][next_state_key].values())
        best_next_action = list(self.players_q_table[playing_player][next_state_key].keys())[best_next_action_index]

        # reward + gamma * max(Q(s', a' for all a'))
        td_target = reward + discount_factor * self.players_q_table[playing_player][next_state_key][best_next_action]
        # [reward + gamma * max(Q(s', a' for all a')) - Q(s, a)]
        td_delta = td_target - self.players_q_table[playing_player][state_key][action]
        # Q(s, a) <- Q(s, a) + alpha * [reward + gamma * max(Q(s', a' for all a')) - Q(s, a)]
        self.players_q_table[playing_player][state_key][action] += alpha * td_delta

    def print_player_q_table(self):
        print("[")
        for player in PLAYER_PLAYING_ORDER.values():
            print(" player#{0}: [".format(player))
            for state_key in self.players_q_table[player].keys():
                print("            {0}".format(state_key), ":[")
                for action in self.players_q_table[player][state_key].keys():
                    print("                |-{0}: {1}".format(action,
                            self.players_q_table[player][state_key][action]))
                print("                                                                                                                            ]")
            print("           ]")
        print("]")

