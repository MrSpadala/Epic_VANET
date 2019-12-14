#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CscAlgo:
	def __init__(self, V, G):
		self.V	=	V
		self.G	=	G
		self.R	=	[]		#list of lists
		self.U	=	None	#list

	

	def get_neighbors(self, V):
		"""
		Returns (a deep copy of) the list of neighbors of vertex V in G
		"""
		#return list(self.G[V-1][1:])

		return list(self.G[V][1:])		#if you start from 0


	def find_shortest_path(self, R, T):
		"""
		Finds the shortest R->T path, from any node in R to T.
		Returns a list of nodes P, where:
			. P[0] is a node in R
			. P[-1] is T
			. Every other node in not in R
		"""
		# Convert input from list to int (identifiers)
		R = list(map(lambda x: x[0], R))
		T = T[0]

		# Take neighbors of T
		T_neighbors = self.get_neighbors(T)

		to_explore = list(T_neighbors)	#nodes to explore via the BFS
		explored = set([T])				#nodes already explored via the BFS
		next_nodes = dict({n: T for n in T_neighbors})	#maps a node to its successor in the R->T path
		starting_node = None 			#first node of the R->T path
		
		# Do the BFS on the graph in "reverse": starting from node T and breaking when arriving to the first node in R
		while len(to_explore) > 0:
			node, to_explore = to_explore[0], to_explore[1:]

			if node in R:
				# This is the nearest node in R. I set it as the first node of the path and exit the BFS
				starting_node = node
				break
			
			for neighbor in self.get_neighbors(node):
				# Append neighbors of `node` to the list of nodes to be explored
				if not neighbor in explored:
					next_nodes[neighbor] = node
					to_explore.append(neighbor)

			explored.add(node)

		else:
			raise Exception("starting_node not found")

		# Use next_nodes to contruct path P
		P = []	#path to be returned
		node = starting_node
		while node != T:
			P.append(node)
			node = next_nodes[node]
		P.append(T)  #append last node T to path

		tP = []

		for p in P:
			#tP.append(self.G[p-1])
			tP.append(self.G[p])	#if you start from 0

		# Convert path from identifier to list
		#tP = list(map(self.G[p] for p in P, P))
		
		return tP


#	shit function 

	def differenceTwoList(self, first, second):
		second = set(second)
		return [item for item in first if item not in second]

	def intersectionTwoList(self, lst1, lst2): 
		lst3 = [value for value in lst1 if value in lst2] 
		return lst3

	def getVertices(self, S1):
		tmp = set()
		for Sx in S1:
			setSx = set(Sx)
			tmp = tmp.union(setSx)

		return list(tmp)




#remodule coverAdjacent with S1 and S2  
	def coverAdjacent(self, S1, S2):
		for lS2	in	S2:
			if self.intersectionTwoList(S1,lS2)	!=	[]:
				return	True
		
		return	False

	def graphAdjacent(self, S1, S2, G):
		for elems1 in S1:

			for setsS2 in S2:
				for elsubsS2 in setsS2:

					if elems1 in G[elsubsS2-1]:
						return True

		return False


	def getMaxFromList(self,L):
		#1 Chose S_0 € S_corsivo s.t. |S_0| is the maximum, and let R={S_0} and U = S_0
		#return a list inside the first maximum |S_0|
		return max(L, key=len)

	def getElemS1notS2(self,S1,S2):
		#where is a list of lists MORE ATTENTION HERE!
		
		tempFound	=	[]

		for elS1 in S1:
			found = False

			for elS2 in S2:
				diff = self.differenceTwoList(elS1,elS2)
				
				if diff == []:
					found	=	True
					break
		
			if not found:				
				tempFound.append(elS1)

		return tempFound

	def doConnectedSetCover(self):
		#######################################################################
		## In this program there are only lists							  	  #
		## but in every fuction  we manipulate them through set and subset	  #
		##																	  #
		#######################################################################

		################	FIRST STEP	###################################
		#Choose S0 ∈ S such that |S0| is the maximum

		S_0		=	self.getMaxFromList(self.G)
		
		
		
		#let R = {S0} and U = S0
		self.R.append(S_0)
		self.U	=	S_0
		
		veryG	= self.G

		# While V \ U != ∅ DO
		while self.differenceTwoList(self.V,self.U) !=  []:

			minimum_EPs		=	10000000000
			minimum_Ps 		= 	[]
			minimum_CPs		=	[]
			
			#fino a qui va tutto bene con G oleeeee

			# For each S ∈ S \ R which is cover-adjacent or graph-adjacent 
			# with a set in R


			

			elemNotR	=	self.getElemS1notS2(veryG,self.R)
			
			
			
			
			for Sx	in	elemNotR:
				resultCovAdj	= self.coverAdjacent(Sx,self.R)
				resultGraphAdj	= self.graphAdjacent(Sx,self.R,self.G)
				
				
				if resultCovAdj or resultGraphAdj:
					#Try It
					

					shortest_Path		=	self.find_shortest_path(self.R,Sx)

					tmpSPS				=	shortest_Path

					C_PS				=	self.getElemS1notS2(tmpSPS, self.R)

					list_verticesPath	=	self.getVertices(shortest_Path)
					
					list_verticesR		=	self.getVertices(self.R)

					lengthPS	=	len(self.differenceTwoList(list_verticesPath, list_verticesR))

					lengthCPS	=	len(C_PS)
					
					if lengthCPS == 0 or lengthPS == 0:
						e_PS	=	0
					else:
						e_PS		=	float(lengthPS/lengthCPS)


					

					if e_PS < minimum_EPs and e_PS != 0:
						
						minimum_EPs	=	e_PS
						self.R		+=	C_PS
						tmpVCPS		=	set(self.getVertices(C_PS))
						self.U		=	list(set(self.U).union(tmpVCPS))
						
						



		return self.R










