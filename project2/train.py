"""
Author:      XuLin Yang
Student id:  904904
Date:        
Description: 
"""

from deep_dark_fantastic_boys_next_door.agent.env import GameEnv
from deep_dark_fantastic_boys_next_door.agent.QLearningAgent import QLearningAgent
import pickle

END = ".pickle"
# PATH = "./train_output/"

env = GameEnv()
q_learning = QLearningAgent()

discount_factor=1.0
alpha=0.5
epsilon=0.1
# test
# num_episodes = 10
# num_batch = 2
# run
num_episodes = 30000
num_batch = 2

for batch in range(0, num_batch):
    if batch == 0:
        # qlearning_<discount_factor>_<alpha>_<epsilon>_<cumulative_num_episode>
        old_file_name = "qlearning_1.0_0.5_0.1_0"
        old_file_name += END
        with open(old_file_name, 'wb') as pickle_file:
            pickle.dump(q_learning.players_q_table, pickle_file)
    [learning_algo, pre_discount_factor, pre_alpha, pre_epsilon, pre_num_episodes] = old_file_name[:-7].split("_")
    # print([learning_algo, pre_discount_factor, pre_alpha, pre_epsilon, pre_num_episodes])

    pre_discount_factor = float(pre_discount_factor)
    pre_epsilon = float(pre_epsilon)
    pre_alpha = float(pre_alpha)
    pre_num_episodes = int(pre_num_episodes)

    assert discount_factor == pre_discount_factor
    assert alpha == pre_alpha
    assert epsilon == pre_epsilon

    # qlearning_<discount_factor>_<alpha>_<epsilon>_<cumulative_num_episode + num_episodes runned this time>
    new_filename = "qlearning_" + str(discount_factor) + "_" + str(alpha) + "_" + str(epsilon) + "_" + str(pre_num_episodes + num_episodes) + END
    # read previous learning data from file seems can work
    with open(old_file_name, 'rb') as pickle_file:
        q_learning.players_q_table = pickle.load(pickle_file)

    # q_learning.print_player_q_table()
    q_learning.q_learning(env, batch, num_batch, num_episodes, discount_factor, alpha, epsilon)

    with open(new_filename, 'wb') as pickle_file:
        pickle.dump(q_learning.players_q_table, pickle_file)
    old_file_name = new_filename

# q_learning.print_player_q_table()
