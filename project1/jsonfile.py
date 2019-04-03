

# calculate n choose r
import operator as op
from functools import reduce
def ncr(n, r):
    r = min(r, n-r)
    numer = reduce(op.mul, range(n, n-r, -1), 1)
    denom = reduce(op.mul, range(1, r+1), 1)
    return numer / denom

from itertools import combinations
from itertools import product
from random import randint
from random import choices
import json

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

    player_pieces = [i for i in combinations(pieces, np)]
    block_pieces = [i for i in combinations(pieces, nb)]
    # possible_com = [i for i in product(player_pieces, block_pieces)]

    name = 0
    count = 0
    while True:
        if count == SAMPLE_SIZE:
            break

        player = list(choices(player_pieces, k=2))
        while True:
            block = list(choices(block_pieces, k=2))

            if no_duplicate(player, block):
                count += 1
                break

        out = {}
        out["colour"] = "red"
        out["pieces"] = player
        out["blocks"] = block
        with open("fullTestCase/" + str(np) + "p/" + str(nb) + "b" + str(name) + ".json", "w") as output:
            json.dump(out, output)
        name += 1


# check if ls2 contains elements that are in ls1
def no_duplicate(ls1, ls2):
    for i in ls2:
        if i in ls1:
            return False
    return True


def main():
    MAX_NP = 4

    # for num_p in range(MAX_NP):
    for num_b in range(37 - 2):
        generate_json_file(2, num_b)


if __name__ == '__main__':
    main()
