import sys

if __name__=="__main__":
	try:
		fname = sys.argv[1]
	except IndexError:
		fname = 'data/allsubj/encoding_grp2.txt'

	from aricept_squares_util import *
	all_trials = parse_file(fname)
	plot_em_up(all_trials,fname)
