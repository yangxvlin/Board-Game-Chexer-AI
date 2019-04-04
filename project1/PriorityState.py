"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-19 00:10:39
Description: Customized class for PriorityQueue<priority, item>
             But designed for compare State
"""


class PriorityState:
    """ class used to customized object in builtin python PriorityQueue
    """

    def __init__(self, priority, item, state_g_score):
        """ initialize a PriorityItem
        :param priority: float for item's priority
        :param item:
        """
        self._priority = priority
        self._item = item
        self._g = state_g_score

    def __lt__(self, other):
        """ compare two PriorityItem
        :param other: the other PriorityItem
        :return: True if self.priority < other.priority
                 compare state's remaining pieces if priority equals
        """
        from State import State

        if self._priority == other.get_priority():
            self_state = self._item
            # print(self_state)
            self_player_pieces = self_state.player_pieces_list[
                                    self_state.playing_player]
            other_state = other.get_item()
            other_player_pieces = other_state.player_pieces_list[
                                    other_state.playing_player]

            if len(self_player_pieces) == len(other_player_pieces):
                # return self._g < other.get_g()
                return self._g < other.get_g()
            else:
                return len(self_player_pieces) < len(other_player_pieces)
        else:
            return self._priority < other.get_priority()

    def get_item(self):
        """ return PriorityItem's item
        :return: return item
        """
        return self._item

    def get_priority(self):
        """ return PriorityItem's priority
        :return: return priority
        """
        return self._priority

    def get_g(self):
        return self._g
