from __future__ import division

import numpy as np
import math as math

def sumSetSquared(X):
    tempX = 0
    for i in range(0, len(X)):
        tempX = tempX + (X[i] * X[i])
    return tempX

def sumSet(X):
    tempX = 0
    for i in range(0, len(X)):
        tempX = tempX + X[i]
    return tempX

def sumXY(X, Y):
    #Sum XY for each pair values
    tempSumXY = 0
    for i in range(0, len(X)):
        tempSumXY = tempSumXY + (X[i] * Y[i])
    return tempSumXY

def mean(dataSet):
    temp = 0
    for i in range(0, len(dataSet)):
        temp = temp + dataSet[i]
    return temp / len(dataSet)

def standardDeviation(dataSet):
    tempMean = mean(dataSet)
    temp = 0
    for i in range(0, len(dataSet)):
        temp = temp + ((dataSet[i] - tempMean) ** 2)
    top = temp
    bottom = len(dataSet) - 1
    temp = top/bottom
    result = math.sqrt(temp)
    #print result
    return result

def covariance1(X, Y):
	n = len(X)
	tempXYSum = 0
	tempMeanX = mean(X)
	tempMeanY = mean(Y)
	for i in range(0, len(X)):
		tempX = (X[i] - tempMeanX)
		tempY = (Y[i] - tempMeanY)
		tempXY = tempX * tempY
		tempXYSum = tempXYSum + tempXY
	result = (1 / (n - 1)) * tempXYSum
	#result = tempXYSum / (len(X) - 1)
	return result

def correlationCoefficient(X, Y):
    a = covariance1(X, Y)
    b = standardDeviation(X)
    c = standardDeviation(Y)
    d = b * c
    return a / d

def pearsonCorrelationCoefficient(X, Y):
	n = len(X)
	varSumXY = sumXY(X, Y)
	varSumX = sumSet(X)
	varSumY = sumSet(Y)
	varSumXSquared = sumSetSquared(X)
	varSumYSquared = sumSetSquared(Y)

	top = (n * varSumXY) - (varSumX * varSumY)
	bottom1 = (n * varSumXSquared) - (varSumX ** 2)
	bottom2 = (n * varSumYSquared) - (varSumY ** 2)
	bottom3 = bottom1 * bottom2
	bottom4 = math.sqrt(bottom3)
	result = top/bottom4
	return result

def meanAbsoluteError(X, Y):
	n = len(X)
	sum = 0
	for i in range(0, len(X)): 
		tempXYsub = abs(X[i] - Y[i])
		sum = sum + tempXYsub
	result = (1 / n) * sum
	return result

def vectorMagnitude(x, y, z):
	temp = (x ** 2) + (y ** 2) + (z ** 2)
	result = math.sqrt(temp)
	return result

	

