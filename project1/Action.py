"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-15 16:01:43
Description: 
"""


class Action:
    ACTIONS = ["MOVE", "JUMP", "EXIT"]

    def __init__(self, action_id, from_hexa, to_hexa=None):
        self.action_id = action_id  # TODO use index or String
        self.from_hexa = from_hexa
        self.to_hexa = to_hexa

    def __repr__(self):
        res = " ".join([Action.ACTIONS[self.action_id], "from", str(self.from_hexa)])

        if self.to_hexa is not None:
            res = " ".join([res, "to", str(self.to_hexa)])

        return res + "."

    @staticmethod
    def print_all_actions(actions):
        for action in actions:
            print(str(action))
