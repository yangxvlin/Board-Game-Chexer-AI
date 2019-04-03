
import json
from copy import deepcopy
from random import sample
from random import shuffle

SAMPLE_SIZE = 30
MAX_NP = 4

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

    player_used = []
    block_used = []

    count = 0
    while True:
        if count == SAMPLE_SIZE:
            break

        while True:
            player = sorted(sample(pieces, np))
            temp = deepcopy(pieces)
            for i in player:
                temp.remove(i)
            block = sorted(sample(temp, nb))

            if player not in player_used and block not in block_used:
                player_used.append(player)
                block_used.append(block_used)
                break

        out = {}
        out["colour"] = "red"
        shuffle(player)
        out["pieces"] = player
        shuffle(block)
        out["blocks"] = block
        with open("fullTestCase/" + str(np) + "p/" + str(nb) + "b" + str(count) + ".json", "w") as output:
            json.dump(out, output)
        count += 1


def main():

    for num_p in range(1, MAX_NP + 1):
        for num_b in range(37 - num_p + 1):
            generate_json_file(num_p, num_b)


if __name__ == '__main__':
    main()