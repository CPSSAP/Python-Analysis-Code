from __future__ import division
import math

def dotProduct(q1, q2):
	dot = (q1[0] * q2[0]) + (q1[1] * q2[1]) + (q1[2] * q2[2]) + (q1[3] * q2[3])
	return dot

def dotProductMean(set1, set2):
	total = 0
	for q1, q2 in zip(set1, set2):
		total = total + dotProduct(q1, q2)
	return total / len(set1)

def angleFromOneToTwo(q1, q2):
	comp1 = dotProduct(q1, q2) ** 2
	comp2 = (2 * comp1) - 1
	rnd = round(comp2, 5)
	the = math.acos(rnd)
	return the

def angleDiffMean(set1, set2):
	total = 0
	for q1, q2 in zip(set1, set2):
		total = total + angleFromOneToTwo(q1, q2)
	return total / len(set1)

def quaternionToEuler(q1):
	x = q1[0]
	y = q1[1]
	z = q1[2]
	w = q1[3]
	test = (x * y) + (z * w)
	heading = 0
	attitude = 0
	bank = 0
	if (test > 0.499):
		heading = 2 * math.atan2(x, w)
		attitude = math.pi/2
		bank = 0
		return
	if (test < -0.499):
		heading = -2 * math.atan2(x, w)
		attitude = math.pi/2
		bank = 0
		return

	sqx = x * x
	sqy = y * y
	sqz = z * z

	heading = math.atan2((2 * y * w) - (2 * x * z), 1 - (2 * sqy) - (2 * sqz)) #result in radians
	a = heading * (180/math.pi) #degrees
	attitude = math.asin(2 * test)
	b = attitude * (180/math.pi)
	bank = math.atan2(2 * x * w - 2 * y * z, 1 - 2 * sqx - 2 * sqz)
	c = bank * (180/math.pi)

	return (a, b, c)





