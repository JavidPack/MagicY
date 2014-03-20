#!/usr/bin/python

import sys
import operator

print 'Argument List:', str(sys.argv)
raw_input("Press Enter to continue...")	
# script Selected file, scale, num, x, y, z
filename = sys.argv[1]
scale = float(sys.argv[2])
tempfile = sys.argv[3]
xm = float(sys.argv[5])/scale
zm = float(sys.argv[7])/scale
#print "file", filename
#print "tempfile", tempfile
#print "Scale", scale
#print "xm",xm
#print "zm",zm
def loadOBJ(filename):
	numVerts = 0
	verts = []
	norms = []
	vertsOut = []
	normsOut = []
	for line in open(filename, "r"):
		if len(line) < 2:
			continue
		vals = line.split()
		if vals[0] == "v":
			v = map(float, vals[1:4])
		#	print line
			verts.append(v)
		if vals[0] == "vn":
			n = map(float, vals[1:4])
			norms.append(n)
		if vals[0] == "f":
			for f in vals[1:]:
				w = f.split("/")
				# OBJ Files are 1-indexed so we must subtract 1 below
				vertsOut.append(list(verts[int(w[0])-1]))
				normsOut.append(list(norms[int(w[2])-1]))
				numVerts += 1
	return vertsOut, normsOut

def dot(v1, v2):
	return sum(p*q for p,q in zip(v1, v2))
	#sum(map(operator.mul, v1, v2))	

def calcY( p1,  p2,  p3,  x,  z):
	det = float((p2[2] - p3[2]) * (p1[0] - p3[0]) + (p3[0] - p2[0]) * (p1[2] - p3[2]))
	if(det==0):
		return 0
	l1 = float(((p2[2] - p3[2]) * (x - p3[0]) + (p3[0] - p2[0]) * (z - p3[2])) / det)
	l2 = float(((p3[2] - p1[2]) * (x - p3[0]) + (p1[0] - p3[0]) * (z - p3[2])) / det)
	l3 = float(1.0 - l1 - l2)

	return float(l1 * y1 + l2 * y2 + l3 * y3)

def trunc(f, n):
	#'''Truncates/pads a float f to n decimal places without rounding'''
	slen = len('%.*f' % (n, f))
	return str(f)[:slen]
	
def pointInTriangle(M, A, B, C):
	# Compute vectors        
	v0 = (C[0]-A[0] , C[1]-A[1])#C - A
	v1 = (B[0]-A[0] , B[1]-A[1])#B - A
	v2 = (M[0]-A[0] , M[1]-A[1])#P - A

# Compute dot products
	dot00 = dot(v0, v0)
	dot01 = dot(v0, v1)
	dot02 = dot(v0, v2)
	dot11 = dot(v1, v1)
	dot12 = dot(v1, v2)

# Compute barycentric coordinates
	invDenom = 1 / (dot00 * dot11 - dot01 * dot01)
	u = (dot11 * dot02 - dot01 * dot12) * invDenom
	v = (dot00 * dot12 - dot01 * dot02) * invDenom

# Check if point is in triangle
	return (u >= 0) and (v >= 0) and (u + v < 1)

def isClockwise(a, b, c):
	area = (b[0]-a[0])*(c[2]-a[2])-(c[0]-a[0])*(b[2]-a[2])
	return area>0

	
vertsO, normsO = loadOBJ(filename)

ypos = [0.0]

for a, b, c in zip(*[iter(vertsO)]*3):
	#print a
	#xmin = min(a[0],b[0],c[0])
	#zmin = min(a[2],b[2],c[2])

	x1 = a[0]
	x2 = b[0]
	x3 = c[0]
	y1 = a[1]
	y2 = b[1]
	y3 = c[1]
	z1 = a[2]
	z2 = b[2]
	z3 = c[2]

	AreaPAB = abs(x1*z2+x2*zm+xm*z1-x1*zm-xm*z2-x2*z1)/2 
	AreaPAC = abs(x1*zm+xm*z3+x3*z1-x1*z3-x3*zm-xm*z1)/2 
	AreaPBC = abs(xm*z2+x2*z3+x3*zm-xm*z3-x3*z2-x2*zm)/2 
	AreaABC = abs(x1*z2+x2*z3+x3*z1-x1*z3-x3*z2-x2*z1)/2 
	ThreeAreas = AreaPAB+AreaPAC+AreaPBC

	if(isClockwise(a,b,c)):
		continue
		
	if(abs(AreaABC - ThreeAreas) < .0001):
		ypos.append(calcY(a,b,c,xm,zm))
		#ypos.append(3344433.3)
		#ypos.append(max(y1, y2, y3))
		#print "In it!", a ,b,c
#raw_input("Press Enter to continue...")	
#for x in ypos:
#		print x
#raw_input("Premaxontinue...")
#print max(ypos)*scale		

file = open(tempfile, 'w')
value = str(max(ypos)*scale)
#file.write(value)
file.write(trunc(max(ypos)*scale, 2))
#file.write("jo")
file.close()
#raw_input("Press Enter to continue...")	
#try:
#    sys.stdout.close()
#except:
#    pass
#try:
#    sys.stderr.close()
#except:
 #   pass
	
print ypos    
print 'Number of arguments:', len(sys.argv), 'arguments.'
print 'Argument List:', str(sys.argv)
raw_input("Press Enter to continue...")

