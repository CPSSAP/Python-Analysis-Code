from __future__ import division

import numpy as np
import haversine as hs
from math import radians, sin, cos, sqrt, asin


def haversinea(lat1, lon1, lat2, lon2):
 
  R = 6372.8 # Earth radius in kilometers
  #R = 6371
 
  dLat = radians(lat2 - lat1)
  dLon = radians(lon2 - lon1)
  lat1 = radians(lat1)
  lat2 = radians(lat2)
 
  a = sin(dLat/2)**2 + cos(lat1)*cos(lat2)*sin(dLon/2)**2
  c = 2*asin(sqrt(a))

  print 'Haver ' + str(R * c)
  return (R * c)

def haversineAndroidPaper(lat1, lon1, lat2, lon2):
	R = 6371

	a = radians((lat2 - lat1)) / 2
	firstPart = sin(a)**2

	b = radians((lon2 - lon1)) / 2
	secondPart = sin(b)**2

	thirdPart = (cos(radians(lat1)) * cos(radians(lat2))) * secondPart

	c = firstPart + thirdPart

	fourthPart = sqrt(c)
	d = asin(fourthPart)
	e = 2 * R

	return (d * e)

def getMeanHaversine(setCoord1, setCoord2):
	size = len(setCoord1)
	print len(setCoord1)
	temp = 0
	for i in range(0, size):
		temp = temp + haversinea(setCoord1[i][0], setCoord1[i][1], setCoord2[i][0], setCoord2[i][1])
	return (temp / size)

def processLocationData(csa, csb):
	latlonsDevice = []
	latlonsTerminal = []

	csva = open(csa, 'r')
	for line in csva:
		tempa = line.split(',')
		a = float(tempa[1])
		b = float(tempa[2])
		c = (a, b)
		latlonsDevice.append(c)
	csva.close()

	csvb = open(csb, 'r')
	for line in csvb:
		tempb = line.split(',')
		a = float(tempb[1])
		b = float(tempb[2])
		c = (a, b)
		latlonsTerminal.append(c)
	csvb.close()

	return (latlonsDevice, latlonsTerminal)


'''
lat1 = 0
lon1 = 0

lat2 = 0
lon2 = 0

lyon = (45.7597, 4.8422)
paris = (48.8567, 2.3508)

a = hs.haversine(lyon,paris,miles=False)
print a
b = haversinea(45.7597, 4.8422, 48.8567, 2.3508)
print b
c = haversineAndroidPaper(45.7597, 4.8422, 48.8567, 2.3508)
print c
'''
