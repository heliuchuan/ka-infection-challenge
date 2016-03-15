import CoachingGraph
import argparse

def process_input(file):
	G = CoachingGraph.CoachingGraph()
	with open(file) as f:
		for ln in f:
			ln = ln.strip().split()
			if ln[0] == 'user':
				G.add_user(ln[1],ln[2])
			elif ln[0] == 'edge':
				G.add_coaching_relation(ln[1],ln[2])
			elif ln[0] == 'total':
				G.total_infection(ln[1])
			elif ln[0] == 'limited':
				G.limited_infection(int(ln[1]))	
	

if __name__ == '__main__':

	parser = argparse.ArgumentParser()
	parser.add_argument('input', help='input file containing test case')
	args = parser.parse_args()

	process_input(args.input)