import pandas as pd
import numpy as np
import glob
import os
import timeit
from subprocess import call
import subprocess
import json

df = pd.DataFrame(columns = ['number of pieces', 'number of blocks', 'average branching factor', 'depth of search tree', 
                             'relative error', 'runtime(in ms)', 'space used(in MB)', "preprocess time(in ms)"])

N_iter = 5
N_digit = 4
PYTHON = "python"
PYTHON_FILE = "test_a_star.py"

filename = "./input/sample14"
file = filename + ".json"

N_FILE = 30

def print_file(file):
    with open(file) as output:
        data = json.load(output)
        print()

index = 0
root_path = os.getcwd()

files = []

for np in range(1, 2):
    path = './fullTestCase/' + str(np) + 'p/'
#     print(os.getcwd())
    
#     os.chdir(root + path)
    
    for nb in range(37 - np + 1):
        
        for file_num in range(0, N_FILE):
            filename = str(nb) + 'b' + str(file_num) + '.json'
#             files = [i for i in glob.glob(filename)]
            filename = path + filename
            files.append(filename)
# print(files)

for i in range(len(files)):
    try:
        fn = files[i]
        print(fn)
        def total_test():
            call([PYTHON, PYTHON_FILE, fn])

        time = round(timeit.timeit(total_test, number=N_iter) / N_iter * 1000, N_digit)

        def test2():
            call([PYTHON, "preprocess.py", fn])
        preprocess_time = round(timeit.timeit(test2, number=N_iter) / N_iter * 1000, N_digit)
        # print(time, "(ms)")

        bad_file = False

#                 os.chdir(root)
        with open('./output.txt', 'r') as the_file:
            # d, avg b, delta, #piece, #block
            temp = []
            for line in the_file:
                if line == 'None\n':
                    bad_file = True
                    break
                else:
                    temp.append(float(line))

        if bad_file:
            continue
        else:
            temp.append(preprocess_time)
            temp.insert(5, time)
            df.loc[index] = temp
            index += 1
    except FileNotFoundError:
        pass
df.to_csv("out.csv", sep=',', encoding='utf-8')