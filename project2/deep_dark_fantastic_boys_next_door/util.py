"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-18 19:20:58
Description: Some helper function used in program
"""


from .Constants import (PLAYER_GOAL, BOARD_BOUND, MOVE_DELTA, INITIAL_SCORE)

""" enable pause in state replay """
PAUSE = False


def initial_state():
    from .State import State

    return State(0, [[(-3, i) for i in range(0, 4)], 
                     [(i, -3) for i in range(0, 4)], 
                     [(3-i, i) for i in range(0, 4)]], INITIAL_SCORE)


def vector_add(a, b):
    """ perform vector addition assume input vectors have same dimension
    :param a: vector a
    :param b: vector b
    :returns:  a + b
    """
    assert(len(a) == len(b))

    from operator import add
    return tuple(map(add, a, b))


def axial_to_cube(axial):
    """ convert an cube coordinate from axial coordinate
    modified from https://www.redblobgames.com/grids/hexagons/#conversions
    :param axial: an axial coordinate in hexagonal system
    :return: cube coordinate in hexagonal system
    """
    x = axial[0]  # q
    z = axial[1]  # r
    y = -x-z
    return tuple([x, y, z])


def on_board(hexe):
    """ check if an hexe piece is on the chexer board by turning an axial
    coordinate hexe to a cube coordinate hexe
    :param hexe: axial coordinate in hexagonal system
    :returns: True if on bard, otherwise False
    """

    cube = axial_to_cube(hexe)

    # check each bound
    for axis in cube:
        if abs(axis) > BOARD_BOUND:
            return False
    return True


def action_to_string(action, from_hexe, to_hexe=None):
    """ return an action in chexer in string
    :param action: action name in String
    :param from_hexe: an axial coordinate hexe on board
    :param to_hexe: an axial coordinate hexe on board
    :return: action.toString()
    """
    res = " ".join([action, "from", str(from_hexe)])

    if to_hexe is not None:
            res = " ".join([res, "to", str(to_hexe)])

    return "".join([res, "."])


def is_in_goal_hexe(hexe, player):
    """ check whether a hexe has moved in player's goal hexes
    :param hexe: an axial coordinate hexe on board
    :param player: the player is playing
    :return: True if hexe is in player's goal hexes, otherwise False
    """
    assert(player in PLAYER_GOAL)

    return hexe in PLAYER_GOAL[player]


def element_to_tuple(list_of_elements):
    """ return list of tuple element
    :param list_of_elements: list of iterable elements
    :return: list of tuple elements
    """
    return list(map(lambda x: tuple(x), list_of_elements))


def calculate_jumped_hexe(from_hexe, to_hexe):
    for delta in MOVE_DELTA:
        jumped_hexe = vector_add(from_hexe, delta)
        # from_hexe perform a jump
        tmp_to_hexe = vector_add(jumped_hexe, delta)

        # from_hexe jumped over correct piece to to_hexe
        if tmp_to_hexe == to_hexe:
            return jumped_hexe
