import math

def getEffectorPos(carriagePos, arms):

		l12, l12mag, l121, l121mag = getPerp(arms[0], arms[1], carriagePos[0][:], carriagePos[1][:])
		l23, l23mag, l232, l232mag = getPerp(arms[1], arms[2], carriagePos[1][:], carriagePos[2][:])

		p0 = carriagePos[0][:]
		p1 = carriagePos[1][:]
		p2 = carriagePos[2][:]

		p012 = getPlane(line(p0, p1)[0], line(p1, p2)[0], p2)

		#get the plane of each perpendicular plane	
		p12 = planeFromLinePoint(l12, l121)	#normal, calculate d ***need to make sure normal is correct***
		p23 = planeFromLinePoint(l23, l232)

		pCenter = intersection3Planes(p12,p23,p012)

		offset = distAlongLine(p012[0:3], 64.387)
		#intersection of 3 planes

		#need to go x distance along normal of p012 and through point just calc'd

		effectPos = [pCenter[0] - offset[0], pCenter[1] - offset[1],pCenter[2] - offset[2] ]

		return effectPos



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
