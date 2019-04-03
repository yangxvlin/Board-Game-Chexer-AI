

# calculate n choose r
import operator as op
from functools import reduce
def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom

from itertools import combinations
import json
from random import randint

SAMPLE_SIZE = 30

# given number of player
def generate_json_file(np, nb):

    pieces = [
        [0, -3], [1, -3], [2, -3], [3, -3],
        [-1, -2], [0, -2], [1, -2], [2, -2], [3, -2],
        [-2, -1], [-1, -1], [0, -1], [1, -1], [2, -1], [3, -1],
        [-3, 0], [-2, 0], [-1, 0], [0, 0], [1, 0], [2, 0], [3, 0],
        [-3, 1], [-2, 1], [-1, 1], [0, 1], [1, 1], [2, 1],
        [-3, 2], [-2, 2], [-1, 2], [0, 2], [1, 2],
        [-3, 3], [-2, 3], [-1, 3], [0, 3]
    ]

    player_possible_com = ncr(37, np)
    block_possible_com = ncr(37 - np, nb)
    total_possible_com = player_possible_com * block_possible_com

    # if count in the list, generate the file
    to_choose = [randint(0, total_possible_com) for i in range(SAMPLE_SIZE)]

    count = 0
    if total_possible_com > SAMPLE_SIZE:
        for player_pieces in combinations(pieces, np):
            player_pieces = list(player_pieces)
            temp = pieces.copy()
            # remove hex occupied by player
            for i in player_pieces:
                temp.remove(i)
            # block can choose all the rest
            for block_pieces in combinations(temp, nb):
                block_pieces = list(block_pieces)
                if count in to_choose:
                    out = {}
                    out["colour"] = "red"
                    out["pieces"] = player_pieces
                    out["blocks"] = block_pieces
                    with open("fullTestCase/" + str(np) + "p/" + str(nb) + "b" + str(count) + ".json", "w") as output:
                        json.dump(out, output)
                count += 1
    # not enough position to choose, have all
    else:
        for player_pieces in combinations(pieces, np):
            player_pieces = list(player_pieces)
            temp = pieces.copy()
            for i in player_pieces:
                temp.remove(i)
            for block_pieces in combinations(temp, nb):
                block_pieces = list(block_pieces)
                out = {}
                out["colour"] = "red"
                out["pieces"] = player_pieces
                out["blocks"] = block_pieces
                with open("fullTestCase/" + str(np) + "p/" + str(nb) + "b" + str(count) + ".json", "w") as output:
                    json.dump(out, output)
                count += 1


def main():
    MAX_NP = 4

    # for num_p in range(MAX_NP):
    for num_b in range(37 - 1):
        generate_json_file(1, num_b)


if __name__ == '__main__':
    main()
