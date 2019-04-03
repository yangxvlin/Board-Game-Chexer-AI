
import json
from copy import deepcopy
from random import sample

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

    count = 0
    while True:
        if count == SAMPLE_SIZE:
            break

        player = sample(pieces, np)
        temp = deepcopy(pieces)
        for i in player:
            try:
                temp.remove(i)
            except:
                print(i)
                print(temp)
                exit(0)
        block = sample(temp, nb)

        out = {}
        out["colour"] = "red"
        out["pieces"] = player
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
