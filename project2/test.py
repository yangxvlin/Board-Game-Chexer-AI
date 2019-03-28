"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-18 22:33:55
Description: 
"""


def main():
    """ main function
    """
    from util import read_state_from_json, initial_state
    from search import a_star_search
    import sys
    from datetime import datetime

    state = [initial_state()][0]

    # filename = sys.argv[1]

    # state = read_state_from_json(filename)

    # test a* running time
    # print("#", datetime.now())
    # search_res = a_star_search(state)
    # print("#", datetime.now())

    # print("# solution path length =", len(search_res) - 1, "\n#")

    # submission output
    # print_result(search_res, True)
    # debug output: enable state pause, board printed
    # print_result(search_res, True, True, True)

    # testing
    # from test import test1
    # print("#", datetime.now())
    # test1(state)
    # print("#", datetime.now())
    test2(state)

def test2(state):
    # print(state)
    print()

    state = state1()
    print(state)

    print(state.all_next_state())

    # for next_state in state.all_next_state():
        # print(next_state.action, next_state)
        # print(next_state.pieces_player_dict)
        # print(next_state.playing_player)

    # print(next_state)
    # print(state == next_state)
    # print(next_state == next_state)
    
def state1():
    from State import State

    return State("red", {"red": [(0, 0)], "green": [], "blue": [(1, 0)]})

def test1(state):

    state = state.all_next_state()[0].all_next_state()[0]
    print(state)

    from datetime import datetime
    print("#", datetime.now())
    print(state.player_pieces_dict[state.playing_player])
    print("#", datetime.now())

    print("#", datetime.now())
    print(list(state.pieces_player_dict.keys()))
    print("#", datetime.now())
    

    # print(state.pieces_player_dict)
    # print(state.cost_to_finish())
    for next_state in state.all_next_state():
        print(next_state.action,
              next_state.player_pieces_dict,
              next_state.pieces_player_dict,
              next_state.playing_player)
        



if __name__ == '__main__':
    """ when this module is executed, run the `main` function:
    """
    main()
