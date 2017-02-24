from __future__ import division
import math

def rotMatToEuler(rm):
	R11 = rm[0]
	R12 = rm[1]
	R13 = rm[2]
	R21 = rm[3]
	R22 = rm[4]
	R23 = rm[5]
	R31 = rm[6]
	R32 = rm[7]
	R33 = rm[8]

	if ((R31 == -1) or (R31 == 1)):
		phi = 0
		if (R31 == -1):
			theta1 = math.pi/2
			psi = math.atan2(R12, R13)
		else:
			theta1 = (0 - math.pi)/2
			psi = math.atan2((0 - R12), (0 - R13))

	else:
		theta1 = 0 - math.asin(R31) #has to be a minus number

		temp1 = R32/math.cos(theta1)
		temp2 = R33/math.cos(theta1)

		psi = math.atan2(temp1, temp2)

		temp3 = R21/math.cos(theta1)
		temp4 = R22/math.cos(theta1)

		phi = math.atan2(temp1, temp2)

	#return (theta1, psi, phi)
	return (math.degrees(theta1), math.degrees(psi), math.degrees(phi))

'''
r11 = 0.5
r12 = -0.1464
r13 = -0.8536
r21 = 0.5
r22 = 0.8536
r23 = -0.1464
r31 = -0.7071
r32 = 0.5
r33 = 0.5

arg = (r11, r12, r13, r21, r22, r23, r31, r32, r33)
print rotMatToEuler(arg)
print math.degrees(math.pi/4)
'''

