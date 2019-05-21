"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-18 19:20:58
Description: Some helper function used in program
"""


from .Constants import (PLAYER_GOAL, BOARD_BOUND, PLAYER_WIN_THRESHOLD)

""" enable pause in state replay """
PAUSE = False


def initial_state():
    """
    return initial state
    :return: initial state
    """
    from .State import State

    return State(0, [[(-3, i) for i in range(0, PLAYER_WIN_THRESHOLD)],
                     [(i, -3) for i in range(0, PLAYER_WIN_THRESHOLD)],
                     [(3-i, i) for i in range(0, PLAYER_WIN_THRESHOLD)]])


def vector_add(a, b):
    """
    perform vector addition assume input vectors have same dimension
    :param a: vector a
    :param b: vector b
    :returns:  a + b
    """
    assert(len(a) == len(b))

    from operator import add
    return tuple(map(add, a, b))


def axial_to_cube(axial):
    """
    convert an cube coordinate from axial coordinate
    modified from https://www.redblobgames.com/grids/hexagons/#conversions
    :param axial: an axial coordinate in hexagonal system
    :return: cube coordinate in hexagonal system
    """
    x = axial[0]  # q
    z = axial[1]  # r
    y = -x-z
    return tuple([x, y, z])


def on_board(hexe):
    """
    check if an hexe piece is on the chexer board by turning an axial
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


def is_in_goal_hexe(hexe, player):
    """
    check whether a hexe has moved in player's goal hexes
    :param hexe: an axial coordinate hexe on board
    :param player: the player is playing
    :return: True if hexe is in player's goal hexes, otherwise False
    """
    assert(player in PLAYER_GOAL)

    return hexe in PLAYER_GOAL[player]


def element_to_tuple(list_of_elements):
    """
    return list of tuple element
    :param list_of_elements: list of iterable elements
    :return: list of tuple elements
    """
    return list(map(lambda x: tuple(x), list_of_elements))


def calculate_jumped_hexe(from_hexe, to_hexe):
    """
    return the coordinate of the hexagon being jumped over adapted from
    provided game.py in /referee
    :param from_hexe: the coordinate of the piece before it jumps
    :param to_hexe: the coordinate of the piece after it jumps
    :return: coordinate of the hexagon being jumped over
    """
    (q_a, r_a), (q_b, r_b) = from_hexe, to_hexe
    qr_c = (q_a + q_b) // 2, (r_a + r_b) // 2
    return qr_c


def normalize(x, x_max, x_min):
    """
    return the normalised value of the input value using given max and min
    values
    :param x: the value to be normalised
    :param x_max: the max value of x
    :param x_min: the min value of x
    :return: normalised value
    """
    return (x - x_min) / (x_max - x_min)
