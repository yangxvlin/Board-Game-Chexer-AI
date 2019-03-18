"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-19 00:10:39
Description: 
"""


class PriorityItem:
    def __init__(self, priority, item):
        self._priority = priority
        self._item = item

    def __lt__(self, other):
        return self._priority < other.get_priority()

    def get_item(self):
        return self._item

    def get_priority(self):
        return self._priority
