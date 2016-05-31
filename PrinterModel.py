import time
import datetime
import random
import math
#import kinematics_py as kinematics
import kinematics_c as kinematics

class PrinterModel:
	#for calculating the kinematics	
	#the tower orders are alpha, beta, gamma

	arms = [122,120,120]

	#locationsof the carriages, updated by method updateCarriagePosition
	'''
	carriagePos = [
	[0,1,0],		#x
	[0,0,1],		#y
	[0,0,0],		#z	
	]		
	'''	

	travelDist = [5,50,50]

	towerHeight = 120

	towerVertices = [
		[-86.66,86,0],	#lower x
		[-50,-50,100],		#lower y
		[0,0,0],			#lower z

		[-86.6,86,0],	#upper x
		[-50,-50,100],		#upper y
		[towerHeight,towerHeight,towerHeight]				#upper z
	]

	def setTravelDist(self, newTravelDist):
		self.travelDist = newTravelDist
		#print self.travelDist

	def setParameters(self, parameters):
		self.towerVertices[0][:] = parameters[0:3]
		self.towerVertices[1][:] = parameters[3:6]
		self.towerVertices[3][:] = parameters[6:9]
		self.towerVertices[4][:] = parameters[9:12]
		#print parameters

		
	def setRandDist(self, idx,val):
		self.travelDist[1] = 1
		return self.travelDist


	def getEffectorPosition(self):
		#see notebook for better explanation.
		#datastructures needed: arms, carriagePos

		#self.carriagePos = kinematics.updateCarriagePos(self.towerVertices, self.travelDist)

		effectPos = kinematics.getEffectorPos(self.towerVertices, self.travelDist, self.arms)
		return effectPos





	def exportVars(self):
		"""Write the printer parameters to a textfile for importing into solidworks"""

		lines = [
		"\"alpha_arm\"=",
		"\"beta_arm\"=",
		"\"gamma_arm\"=",

		"\"alpha_x_bot\"=",
		"\"beta_x_bot\"=",
		"\"gamma_x_bot\"=",
		"\"alpha_y_bot\"=",
		"\"beta_y_bot\"=",
		"\"gamma_y_bot\"=",

		"\"alpha_x_top\"=",
		"\"beta_x_top\"=",
		"\"gamma_x_top\"=",
		"\"alpha_y_top\"=",
		"\"beta_y_top\"=",
		"\"gamma_y_top\"=",

		"\"alpha_carriage_travel\"=",
		"\"beta_carriage_travel\"=",
		"\"gamma_carriage_travel\"=",

		"\"tower_height\"="
		]

		values = self.arms
		idx = [0,1,3,4]
		for i in range(len(idx)):
			for j in range(3):
				values.append(abs(self.towerVertices[ idx[i] ][j]))

		values = values + self.travelDist
		values.append(self.towerHeight)

		f = open("equations.txt", "w")
		for i in range(len(lines)):
			f.write(lines[i])
			f.write(str(values[i]))
			f.write("\n")
		f.close()

