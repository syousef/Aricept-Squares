import sys

if __name__=="__main__":
	try:
		fname = sys.argv[1]
	except IndexError:
		fname = 'data/AL/day3/encoding.txt'


	from aricept_squares_util import *
	all_trials = parse_file(fname)
    
    #for first day capacity use -2, else put in the capacity from maxK.txt here
    maxK= -2

	plot_em_up(all_trials,fname,maxK)
