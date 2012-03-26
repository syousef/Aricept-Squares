import sys

if __name__=="__main__":
	try:
		fname = sys.argv[1]
	except IndexError:
		fname = 'data/AL/day1/capacity.txt'


	from aricept_squares_util import *
	all_trials = parse_file(fname)
	plot_em_up(all_trials,fname,-2)
