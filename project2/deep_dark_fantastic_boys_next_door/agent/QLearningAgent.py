"""
Author:      XuLin Yang
Student id:  904904
Date:        
Description: modify from https://github.com/dennybritz/reinforcement-learning/blob/master/TD/Q-Learning%20Solution.ipynb
"""

from collections import defaultdict
import numpy as np
import sys
import itertools
from deep_dark_fantastic_boys_next_door.Constants import (PLAYER_PLAYING_ORDER)
from deep_dark_fantastic_boys_next_door.util import (element_to_tuple)


class QLearningAgent:

    def __init__(self):
        # {state: {action: v(s) "which is value"}}
        # TODO should we use Ordered Dict for action?
        self.players_q_table = {player: defaultdict(lambda: defaultdict(int))
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
            # TODO is this correct? if not yet visited, do a random move
            if len(Q[observation].values()) == 0:
                best_action = np.random.choice(np.arange(nA))
            else:
                best_action = np.argmax(Q[observation].values())
            A[best_action] += (1.0 - epsilon)
            return A

        return policy_fn

    def q_learning(self, env, num_episodes=1, discount_factor=1.0, alpha=0.5,
                   epsilon=0.1):
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
            if (i_episode + 1) % 100 == 0:
                print("\rEpisode {}/{}.".format(i_episode + 1, num_episodes),
                      end="")
                sys.stdout.flush()

            # Reset the environment and pick the first action
            state = env.reset()  # TODO env

            # One step in the environment
            # total_reward = 0.0
            for t in itertools.count():
                # get states for a round
                # *********************** player0 *****************************
                player0_state = state
                assert player0_state.playing_player == 0
                player0_state_key = player0_state.get_key()
                player0_next_states = player0_state.all_next_state()
                player0_next_actions = [next_state.action
                                        for next_state in player0_next_states]

                # terminology:
                # player's q_table = self.players_q_table[state.playing_player]
                player0_policy = self.make_epsilon_greedy_policy(
                    self.players_q_table[player0_state.playing_player], epsilon,
                    len(player0_next_actions))
                # Take a step for player 0
                player0_action_probs = player0_policy(player0_state_key)
                player0_action_index = np.random.choice(
                    np.arange(len(player0_action_probs)),
                    p=player0_action_probs)
                player0_action = player0_next_actions[player0_action_index]
                # next_state, reward, done, _ = env.step(action)  # TODO env
                # player0_reward, done, _ = env.step(player0_next_state)
                player0_next_state = player0_next_states[player0_action_index]
                player0_next_state_key = player0_next_state.get_key()

                # *********************** player1 *****************************
                player1_state = player0_next_state
                assert player1_state.playing_player == 1
                player1_state_key = player1_state.get_key()
                player1_next_states = player1_state.all_next_state()
                player1_next_actions = [next_state.action
                                        for next_state in player1_next_states]

                player1_policy = self.make_epsilon_greedy_policy(
                    self.players_q_table[player1_state.playing_player], epsilon,
                    len(player1_next_actions))
                # Take a step for player 1
                player1_action_probs = player1_policy(player1_state_key)
                player1_action_index = np.random.choice(
                    np.arange(len(player1_action_probs)),
                    p=player1_action_probs)
                player1_action = player1_next_actions[player1_action_index]
                player1_next_state = player1_next_states[player1_action_index]
                player1_next_state_key = player1_next_state.get_key()

                # *********************** player2 *****************************
                player2_state = player1_next_state
                assert player2_state.playing_player == 2
                player2_state_key = player2_state.get_key()
                player2_next_states = player2_state.all_next_state()
                player2_next_actions = [next_state.action
                                        for next_state in player2_next_states]

                player2_policy = self.make_epsilon_greedy_policy(
                    self.players_q_table[player2_state.playing_player], epsilon,
                    len(player2_next_actions))
                # Take a step for player 1
                player2_action_probs = player2_policy(player2_state_key)
                player2_action_index = np.random.choice(
                    np.arange(len(player2_action_probs)),
                    p=player2_action_probs)
                player2_action = player2_next_actions[player2_action_index]
                player2_next_state = player2_next_states[player2_action_index]
                player2_next_state_key = player2_next_state.get_key()

                # ********************* get turn census ***********************
                [player0_reward, player1_reward, player2_reward], done = \
                    env.step([player0_next_state,
                             player1_next_state,
                             player2_next_state])

                # ********************* update q table ************************
                self.update_player_q_table(0, player0_state_key,
                                           player0_next_state_key,
                                           player0_next_actions,
                                           player0_action,
                                           player0_reward,
                                           discount_factor, alpha)
                self.update_player_q_table(1, player1_state_key,
                                           player1_next_state_key,
                                           player1_next_actions,
                                           player1_action,
                                           player1_reward,
                                           discount_factor, alpha)
                self.update_player_q_table(2, player2_state_key,
                                           player2_next_state_key,
                                           player2_next_actions,
                                           player2_action,
                                           player2_reward,
                                           discount_factor, alpha)

                print(self.players_q_table)
                return

                # ******************* next round in epsoides ******************
                if done:
                    break
                if t > 256:
                    print("t > 256")
                state = player2_next_state

    def update_player_q_table(self, playing_player, state_key, next_state_key,
                              next_actions, action, reward, discount_factor,
                              alpha):
        # TD Update
        print(next_state_key, self.players_q_table[playing_player])
        print(next_state_key in self.players_q_table[playing_player])
        if next_state_key in self.players_q_table[playing_player]:
            best_next_action_index = np.argmax(
                    self.players_q_table[playing_player][state_key].values())
            print(self.players_q_table[playing_player][
                    state_key].keys())
            print(best_next_action_index)
            best_next_action = list(self.players_q_table[playing_player][
                    state_key].keys())[best_next_action_index]
            # TODO should we have OrderedDict?
        else:
            # no visited
            best_next_action_index = np.random.choice(
                                        np.arange(len(next_actions)))
            best_next_action = next_actions[best_next_action_index]

        if next_state_key in self.players_q_table[playing_player]:
            td_target = reward + discount_factor * self.players_q_table[
                            playing_player][next_state_key][best_next_action]
        else:
            td_target = reward

        td_delta = td_target - self.players_q_table[playing_player][state_key][
                                                                    action]
        self.players_q_table[playing_player][state_key][action] \
            += alpha * td_delta

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

