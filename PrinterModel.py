import time
import datetime
import random
import math

class PrinterModel:
	#for calculating the kinematics	
	#the tower orders are alpha, beta, gamma

	arms = [122,120,120]

	#locationsof the carriages, updated by method updateCarriagePosition
	carriagePos = [
	[0,1,0],		#x
	[0,0,1],		#y
	[0,0,0],		#z	
	]		

	travelDist = [5,50,50]

	towerHeight = 120

	towerVertices = [
		[-86.66,86,0],	#lower x
		[-50,-50,100],		#lower y
		[0,0,0],			#lower z

		[-86.6,86,0],	#upper x
		[-50,-50,100],		#upper y
		#[120,121,122]
		[towerHeight,towerHeight,towerHeight]				#upper z
	]

	def getParameters(self):
		return self.travelDist

	def setParameters(self, parameters):
		if(len(parameters) == 3):	#only change the carriage travel distances
			self.travelDist = parameters

		elif(len(parameters) == 12):
			#print self.towerVertices
			self.towerVertices[0][:] = parameters[0:3]
			self.towerVertices[1][:] = parameters[3:6]
			self.towerVertices[3][:] = parameters[6:9]
			self.towerVertices[4][:] = parameters[9:12]
		return parameters

		
	def setRandDist(self, idx,val):
		self.travelDist[1] = 1
		return self.travelDist


	def getEffectorPosition(self):
		#see notebook for better explanation.
		#datastructures needed: arms, carriagePos

		for i in range (3):
			towerLength = math.sqrt( (self.towerVertices[0][i]-self.towerVertices[3][i])**2 + (self.towerVertices[1][i]-self.towerVertices[4][i])**2 + (self.towerVertices[2][i]-self.towerVertices[5][i])**2)

			for j in range (3):
				#do similar triangles for each of the three axies
				self.carriagePos[j][i] =  self.towerVertices[i][j] - ((self.towerVertices[i][j]-self.towerVertices[i+3][j]) * (towerLength-self.travelDist[j]) / towerLength)


		l12, l12mag, l121, l121mag = getPerp(self.arms[0], self.arms[1], self.carriagePos[0][:], self.carriagePos[1][:])
		l23, l23mag, l232, l232mag = getPerp(self.arms[1], self.arms[2], self.carriagePos[1][:], self.carriagePos[2][:])

		#print l12
		#print l12mag
		#print l121mag
		#print "l121: ", l121

		p0 = self.carriagePos[0][:]
		p1 = self.carriagePos[1][:]
		p2 = self.carriagePos[2][:]

		#get the plane of the 3carrige points.
		#print "line p0 p1:", line(p0, p1)[0]
		#print "line p1 p2:", line(p1, p2)[0]

		#print "p0:", p0
		#print "p1:", p1
		#print "p2:", p2
		p012 = getPlane(line(p0, p1)[0], line(p1, p2)[0], p2)

		#print "p012: ", p012

		#get the plane of each perpendicular plane
		
		p12 = planeFromLinePoint(l12, l121)	#normal, calculate d ***need to make sure normal is correct***
		p23 = planeFromLinePoint(l23, l232)

		pCenter = intersection3Planes(p12,p23,p012)
		#print "pCenter:", pCenter

		offset = distAlongLine(p012[0:3], 64.387)
		#intersection of 3 planes

		#need to go x distance along normal of p012 and through point just calc'd

		effectPos = [pCenter[0] - offset[0], pCenter[1] - offset[1],pCenter[2] - offset[2] ]
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



def cross(v0, v1):
	#scalefactor = v0[1]*v1[2] - v0[2]*v1[1] 
	#return [ 1, (v0[0]*v1[2] - v0[2]*v1[0])/scalefactor, (v0[0]*v1[1] - v0[1]*v1[0])/scalefactor ]
	return [ v0[1]*v1[2] - v0[2]*v1[1], -v0[0]*v1[2] + v0[2]*v1[0], v0[0]*v1[1] - v0[1]*v1[0] ]

def line(p0, p1):
	l = []
	lmag = 0
	for i in range(3):
		l.append(p1[i]-p0[i])
		lmag += l[i]**2
	lmag = math.sqrt(lmag)

	return l, lmag

def getPerp(r1, r2, carriagePos0, carriagePos1):

	l12, l12mag = line(carriagePos0, carriagePos1)
	l121mag = (r1**2 - r2**2 + l12mag**2)/(2*l12mag)
	l121 = []

	for i in range(3):
		l121.append( carriagePos0[i] + (carriagePos1[i]-carriagePos0[i]) * (l121mag) / l12mag )	#get the x, y, z coord

	return l12, l12mag, l121, l121mag

def getPlane(l1, l2, p0):
	#equation of a plane
	# a(x-x0) + b(y-y0) + c(z-z0)
	# ax + by + cz = d
	# normal = n = (a,b,c)
	# point on plane = p0 = (x0, y0, z0)

	#equation of a plane from 3 points
	#make 2 vectors that are on the plane, the cross product them.
	#now have normal and point on plane. 

	plane = cross (l1, l2)

	d = 0
	for i in range(3):
		d += plane[i]*p0[i]
	plane.append(d)
	return plane

def planeFromLinePoint(l12, l121):
	return [ l12[0], l12[1], l12[2], l12[0]*l121[0] + l12[1]*l121[1] + l12[2]*l121[2]  ]

def intersection3Planes( p1, p2, p3 ):	

	a1 = p1[0]
	b1 = p1[1]
	c1 = p1[2]
	d1 = p1[3]

	a2 = p2[0]
	b2 = p2[1]
	c2 = p2[2]
	d2 = p2[3]

	a3 = p3[0]
	b3 = p3[1]
	c3 = p3[2]
	d3 = p3[3]

	a = (-a1/a2)*b2 + b1
	b = (-a1/a3)*b3 + b1
	c = (-a1/a3)*d3 + d1
	d = (-a1/a3)*c3 + c1
	e = (-a1/a2)*c2 + c1
	f = (-a1/a2)*d2 + d1


	z = ( (a*c)/b-f ) / ( (a*d)/b-e )
	y = (c-d*z)/b
	x = (-b2*y-c2*z+d2)/a2
	return [x,y,z]


def distAlongLine(l, h):
	#normalize
	l[1] = l[1]/l[0]
	l[2] = l[2]/l[0]
	l[0] = 1

	t = math.sqrt( (h**2)/(l[1]**2 + l[2]**2 + 1) )

	return [t, l[1]*t, l[2]*t]