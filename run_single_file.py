fname = 'data/allsubj/encoding_grp2.txt'
from aricept_squares_util import *
all_trials = parse_file(fname)
plot_em_up(all_trials,fname)
