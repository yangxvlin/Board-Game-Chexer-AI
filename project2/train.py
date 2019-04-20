"""
Author:      XuLin Yang
Student id:  904904
Date:        
Description: 
"""

from deep_dark_fantastic_boys_next_door.agent.env import GameEnv
from deep_dark_fantastic_boys_next_door.agent.QLearningAgent import QLearningAgent
import json


discount_factor=1.0
alpha=0.5
epsilon=0.1

# qlearning_<discount_factor>_<alpha>_<epsilon>_<cumulative_num_episode>
filename = "qlearning_" + str(discount_factor) + "_" + str(alpha) + "_" + str(epsilon) + ".json"

env = GameEnv()


q_learning = QLearningAgent()
q_learning.print_player_q_table()
q_learning.q_learning(env, 50000, discount_factor, alpha, epsilon)

# qlearning_<discount_factor>_<alpha>_<epsilon>_<cumulative_num_episode + num_episodes runned this time>
# with open(filename, "w") as output:
#     json.dump(q_learning.players_q_table, output)


q_learning.print_player_q_table()
