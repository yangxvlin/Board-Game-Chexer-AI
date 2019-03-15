"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-15 16:01:43
Description: 
"""


class Action:
    ACTIONS = ["MOVE", "JUMP", "EXIT"]

    def __init__(self, action_id, from_hexe, to_hexe=None):
        self.action_id = action_id  # TODO use index or String
        self.from_hexe = from_hexe
        self.to_hexe = to_hexe

    def __repr__(self):
        res = " ".join([Action.ACTIONS[self.action_id], "from", str(self.from_hexe)])

        if self.to_hexe is not None:
            res = " ".join([res, "to", str(self.to_hexe)])

        return res + "."

    @staticmethod
    def print_all_actions(actions):
        for action in actions:
            print(str(action))
