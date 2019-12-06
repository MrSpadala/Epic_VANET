#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CscAlgo:
	def __init__(self, V,S,G):
		self.V	=	V
		self.S	=	S
		self.G	=	G
		self.R	=	[]		#list of lists
		self.U	=	None	#list

		self.doAlgorithm()


	def graphAdjacent(self, Sx, R):
		pass

#remodule coverAdjacent with S1 and S2  
	def coverAdjacent(self, Sx,R):
		setSx	=	set(Sx)
		for lsR	in	R:
			setR	=	set(lsR)

			if setSx.intersection(setR)	==	set():
				return	False
		
		return	True


	def choseMaxS(self):
		#1 Chose S_0 € S_corsivo s.t. |S_0| is the maximum, and let R={S_0} and U = S_0
		#return a list inside the first maximum |S_0|
		return max(self.S, key=len)

	def getElemSnotR(self):
		#where is a list of lists MORE ATTENTION HERE!
		tempS	=	[]

		for lsS in self.S:
			setS	=	set(lsS)
			for lsR in self.R:
				setR	=	set(lsR)

				# Sx \ R
				if setS.difference(setR) != set():
					tempS.append(list(setS))
					continue
		return tempS

	def doAlgorithm(self):
		#######################################################################
		## In this program there are only lists							  	  #
		## but in every fuction  we manipulate them through set and subset	  #
		##																	  #
		#######################################################################

		################	FIRST STEP	###################################
		S_0		=	self.choseMaxS()
		
		self.R.append(S_0)
		self.U	=	S_0
		################	END FIRST STEP	###############

		#################	SECOND STEP	################
		#2 WHILE ELEMENTS OF V \ U NOT BELONG Ø DO...

		setV	=	set(self.V)
		setU	=	set(self.U)


		while setV.difference(setU) != set():

			#start point 2.1
			elemNotR	=	self.getElemSnotR()

			for Sx	in	elemNotR:
				print(Sx)
				print(self.R)
				print(self.coverAdjacent(Sx,self.R))

			break









