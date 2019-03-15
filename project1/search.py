"""
Author:      XuLin Yang
Student id:  904904
Date:        2019-3-15 14:56:03
Description: 
"""

import json
import sys

from Action import Action
from Hexe import Hexe
from Player import Player
from State import State

JSON_FILE_KEYS = ["colour", "pieces", "blocks"]


class Search:
    @staticmethod
    def search(state):
        # TODO finish this
        actions = []

        # NOTE: use s.get_next_state to further search

        return actions


def main(argv):
    filename = argv

    with open(filename) as json_file:
        data = json.load(json_file)

        player = data[JSON_FILE_KEYS[0]]
        player_pieces = {player: Hexe.read_coordinates(data[JSON_FILE_KEYS[1]],
                                                       Player.PLAYER_ORDER[data[JSON_FILE_KEYS[0]]])}
        obstacles = Hexe.read_coordinates(data[JSON_FILE_KEYS[2]], JSON_FILE_KEYS[2])

    state = State(player, player_pieces, obstacles)

    search_res = Search.search(state)
    Action.print_all_actions(search_res)


if __name__ == "__main__":
    main(sys.argv)
