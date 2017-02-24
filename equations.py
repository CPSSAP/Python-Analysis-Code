from __future__ import division

import numpy as np
import math as math


def sumXSquared(X):
    tempX = 0
    for i in range(0, len(X)):
        tempX = tempX + (X[i] * X[i])
    return tempX

def sumX(X):
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
    tempXYSum = 0
    tempMeanX = mean(X)
    tempMeanY = mean(Y)
    for i in range(0, len(X)):
        tempX = (X[i] - tempMeanX)
        tempY = (Y[i] - tempMeanY)
        tempXY = tempX * tempY
        tempXYSum = tempXYSum + tempXY
    print "Hello"
    print tempXYSum
    result = tempXYSum / (len(X) - 1) #check this
    return result
    
def pearsonCorrelationCoefficient(X, Y):
    top = (n * varSumXY) - (varSumX * varSumY)
    print top
    bottom1 = (n * varSumXSquared) - (varSumX ** 2)
    #print bottom1
    bottom2 = (n * varSumYSquared) - (varSumY ** 2)
    #print bottom2
    bottom3 = bottom1 * bottom2
    bottom4 = math.sqrt(bottom3)
    result = top/bottom4
    #print result
    return result
    
def correlationCoefficientAlt1(X, Y):
    Zxi = []
    Zyi = []
    tempMeanX = mean(X)
    tempMeanY = mean(Y)
    stdX = standardDeviation(X)
    stdY = standardDeviation(Y)
    
    for i in range(0, len(X)):
        tempX = (X[i] - tempMeanX) / stdX
        tempY = (Y[i] - tempMeanY) / stdY
        Zxi.append(tempX)
        Zyi.append(tempY)
    
    tempZxiZyiSum = 0
    for j in range(0, len(X)):
        tempZxiZyi = Zxi[j] * Zyi[j]
        tempZxiZyiSum = tempZxiZyiSum + tempZxiZyi
        
    result = tempZxiZyiSum / (len(X) - 1)
    #print result
    return result
    
def sampleCorrelationCoefficient(X, Y):
    a = standardDeviation(X) * standardDeviation(Y)
    b = covariance1(X, Y)
    return b / a
    
def correlationCoefficientTapTapPayPaper(X, Y):
    a = covariance1(X, Y)
    b = standardDeviation(X) ** 2
    c = standardDeviation(Y) ** 2
    d = b * c
    e = math.sqrt(d)
    return a / e
    
    
  
X = [1,2,4,5]
Y = [1,3,5,7]

A = [2.1, 2.5, 3.6, 4.0]
B = [8, 10, 12, 14]

global varSumXY
varSumXY = sumXY(X,Y)
#print varSumXY

global varSumX
varSumX = sumX(X)
#print varSumX

global varSumY
varSumY = sumX(Y)
#print varSumY

global n
n = len(X)

global varSumXSquared
varSumXSquared = sumXSquared(X)
#print varSumXSquared

global varSumYSquared
varSumYSquared = sumXSquared(Y)
#print varSumYSquared



temp = mean(X)
#print temp

temp2 = mean(Y)
#print temp2

#standardDeviation(X)
#standardDeviation(Y)

print pearsonCorrelationCoefficient(X, Y)
print correlationCoefficientAlt1(X, Y)
print sampleCorrelationCoefficient(X, Y)
print correlationCoefficientTapTapPayPaper(X, Y)
#print covariance1(A, B)

a = covariance1(A, B)
b = mean(X) * mean(Y)
b = standardDeviation(X) * standardDeviation(Y)

print a / b