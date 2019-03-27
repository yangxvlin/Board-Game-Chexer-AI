"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-18 22:33:55
Description: 
"""


def test1(state):
    print(state)
    print(state.cost_to_finish())
    for next_state in state.all_next_state():
        print(next_state.action, next_state, next_state.cost_to_finish())


def test2():
    pass
    # from util import vector_add, vector_dot_product
    # print(vector_add((0, 0), (1, -1)))
    # print(vector_dot_product(2, (1, -1)))
