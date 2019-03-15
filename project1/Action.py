"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-15 16:01:43
Description: 
"""

from Hexe import Hexe


class Action:
    ACTIONS = ["MOVE", "JUMP", "EXIT"]

    # [left,  top left,   top right, right, down wight, down left]
    DELTAS = {ACTIONS[0]: [Hexe(-1, 0, ACTIONS[0]), Hexe(0, -1, ACTIONS[0]), Hexe(1, -1, ACTIONS[0]),
                           Hexe(1, 0, ACTIONS[0]),  Hexe(0, 1, ACTIONS[0]),  Hexe(-1, 1, ACTIONS[0])],
              ACTIONS[1]: [Hexe(-2, 0, ACTIONS[0]), Hexe(0, -2, ACTIONS[0]), Hexe(2, -2, ACTIONS[0]),
                           Hexe(2, 0, ACTIONS[0]),  Hexe(0, 2, ACTIONS[0]),  Hexe(-2, 2, ACTIONS[0])]}

    # TODO update to maintain kill information
    def __init__(self, action_id, from_hexe, to_hexe=None): #, has_killed=False):
        self.action_id = action_id  # TODO use index or String
        self.from_hexe = from_hexe
        self.to_hexe = to_hexe
        # self.has_killed = has_killed

    def __repr__(self):
        res = " ".join([Action.ACTIONS[self.action_id], "from", str(self.from_hexe)])

        if self.to_hexe is not None:
            res = " ".join([res, "to", str(self.to_hexe)])

        return res + "."
