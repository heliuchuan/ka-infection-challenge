from matplotlib.pyplot import pause
from random import choice

import networkx as nx
import matplotlib.pyplot as plt
import itertools
import Queue


class UserInfo(object):
	
	def __init__(self, name, user_id):
		self.infected = False
		self.name = name
		self.user_id = user_id
		self.pos = None

class CoachingGraph(object):
	
	def __init__(self):
		self.user_network = nx.DiGraph()

	def add_user(self, user_id, name = '', coach = None, students = None):
		if user_id in self.user_network.nodes():
			print 'User already exists'
			return
		self.user_network.add_node(user_id, info = UserInfo(name,user_id))
		if students:
			for student in students:
				self.add_coaching_relation(user_id, student)
		if coach:
			self.add_coaching_relation(coach, user_id)
		
		#Update graph layout and fix it
		self.pos = nx.spring_layout(self.user_network)

	def add_coaching_relation(self, coach, student):
		if coach in self.user_network.nodes():
			if student in self.user_network.nodes():
				self.user_network.add_edge(coach, student)
			else:
				print 'Student ' + str(student) + ' does not exist in userbase'
		else:
			print 'Coach ' + str(coach) + ' does not exist in userbase'

	def get_name(self, node):
		return self.user_network.node[node]['info'].name

	def total_infection(self, node):
		undirected_copy = nx.Graph(self.user_network)
		
		bfs_path = [node] + map(lambda x: x[1], 
			nx.bfs_edges(undirected_copy, node))
		
		self.plot()
	
		for infectee in bfs_path:
			self.infect_user(infectee)
			self.plot()
	
	def limited_infection(self, target_num):
		original_target = target_num
		if target_num > len(self.user_network):
			self.infect_all()
			print 'All users infected'
			return

		for user in self.user_network.nodes_iter():
			if target_num == 0:
				break
			if self.user_network.in_degree(user) == 0:
				target_num -= self.limited_bfs_infection(user, target_num)
		num_infected = original_target - target_num
		
		print 'Infected ' + str(num_infected) + \
			' out of ' + str(original_target)

	def limited_bfs_infection(self, node, target_num):
		original_target = target_num
		if target_num == 0:
			return 0
		self.infect_user(node)
		target_num -= 1
		successors = nx.bfs_successors(self.user_network,node)
		fringe = Queue.Queue()
		fringe.put(node)
		while not fringe.empty():
			self.plot()
			coach = fringe.get()
			if coach in successors and len(successors[coach]) <= target_num:
				for student in successors[coach]:
					self.infect_user(student)
					fringe.put(student)
				target_num -= len(successors[coach])
		return original_target - target_num



	def infect_user(self, node):
		self.user_network.node[node]['info'].infected = True

	def infect_all(self):
		for infectee in self.user_network.nodes():
			self.infect_user(infectee)

	def plot(self):
		plt.clf()
		plt.ion()
		
		labels=dict((n,d['info'].name) 
			for n,d in self.user_network.nodes(data=True))
		
		nx.draw_networkx(self.user_network,
			pos = self.pos,
			node_color = ['r' if self.user_network.node[n]['info'].infected 
				else 'forestgreen' for n in self.user_network],
			node_size = [100 + 50 * self.user_network.degree(n) 
				for n in self.user_network],
			labels = labels,
			alpha = .7)

		plt.draw()
		pause(.5)
