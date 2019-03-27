"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-19 00:10:39
Description: Customized class for PriorityQueue<priority, item>
"""


class PriorityItem:
    """ class used to customized object in builtin python PriorityQueue
    """

    def __init__(self, priority, item):
        """ initialize a PriorityItem
        :param priority: float for item's priority
        :param item:
        """
        self._priority = priority
        self._item = item

    def __lt__(self, other):
        """ compare two PriorityItem
        :param other: the other PriorityItem
        :return: True if self.priority < other.priority
        """
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
