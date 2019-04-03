import sys
from util import read_state_from_json

# get filename
filename = sys.argv[1]

# read state
state = read_state_from_json(filename)