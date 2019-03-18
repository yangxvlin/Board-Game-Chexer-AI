"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-18 19:20:58
Description: 
"""


def vector_add(a, b):
    """ vector addition"""
    assert(len(a) == len(b))

    from operator import add
    return tuple(map(add, a, b))


def vector_dot_product(c, v):
    """ c .* v"""
    return tuple(map(lambda x: x*c, v))


# from https://www.redblobgames.com/grids/hexagons/#conversions
def axial_to_cube(axial):
    x = axial[0]  # q
    z = axial[1]  # r
    y = -x-z
    return tuple([x, y, z])


def on_board(hexe):
    """ 
    :param hexe axial coordinate
    """
    from Constants import BOARD_BOUND

    cube = axial_to_cube(hexe)

    for axis in cube:
        if abs(axis) > BOARD_BOUND:
            return False
    return True


def hexe_to_string(hexe):
    return "".join(["(", str(hexe[0]), ", ", str(hexe[1]), ")"])


def action_to_string(action, from_hexe, to_hexe=None):
    res = " ".join([action, "from", hexe_to_string(from_hexe)])

    if to_hexe is not None:
            res = " ".join([res, "to", hexe_to_string(to_hexe)])

    return "".join([res, "."])


def is_in_goal_hexe(hexe, player):
    """ """
    from Constants import PLAYER_GOAL
    
    assert(player in PLAYER_GOAL.keys())
    return hexe in PLAYER_GOAL[player]


def element_to_tuple(list_of_elements):
    return list(map(lambda x: tuple(x), list_of_elements))
