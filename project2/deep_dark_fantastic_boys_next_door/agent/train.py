"""
Author:      XuLin Yang
Student id:  904904
Date:        
Description: 
"""

from deep_dark_fantastic_boys_next_door.agent.env import GameEnv
from deep_dark_fantastic_boys_next_door.agent.QLearningAgent import QLearningAgent

env = GameEnv()


q_learning = QLearningAgent()
q_learning.print_player_q_table()
print(q_learning.players_q_table)
q_learning.q_learning(env)

q_learning.print_player_q_table()
