"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-5-18 20:19:42
Description: agent controlled by human (not adapted)
"""


class HumanAgent:
    def get_next_action(self, state, player):
        actions = state.all_next_action()

        for i, action in enumerate(actions):
            print(i, ":", action)

        choose = int(input("your choice: "))

        return actions[choose]
