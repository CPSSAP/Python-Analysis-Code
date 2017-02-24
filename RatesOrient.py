from __future__ import division

absLimit = 0.000000000000000004

def calculateFPRandFNR(arrLeg, arrIll, outCsv):
	if (arrLeg[0] <= arrIll[0]):
		low = arrLeg[0]
	else:
		low = arrIll[0]

	#for x in arrLeg:
		#print x

	#print '\n'

	#for y in arrIll:
		#print y

	if (arrIll[-1] >= arrLeg[-1]):
		high = arrIll[-1]
	else:
		high = arrLeg[-1]

	#print "high = " + str(high)
	#print high
	#print low
	tranRange = (float(high) - float(low))
	noOfThresholds = 100.0
	thresholdInc = tranRange / noOfThresholds

	FP = 0
	TP = 0
	FN = 0
	TN = 0
	csvLines = []
	csvLines.append('Threshold, FPR, FNR\n')
	i = 1
	fhigh = float(high)
	threshold = float(low)
	#print threshold
	#print fhigh
	while (threshold < fhigh) or (abs(threshold - fhigh) < absLimit):
		#print str(threshold) + '   ' + str(fhigh) + '   ' + str(i)
		i = i + 1
		#Calculate False Negatives (leg)
		for trl in arrLeg:
			if (float(trl) <= threshold) or (abs(threshold - fhigh) < absLimit): #Abs used as two floats are not equal even when they appear equal
				#print trl
				TP = TP + 1
			else:
				FN = FN + 1

		#Calculate False Positives (ill)
		for tri in arrIll:
			if (float(tri) <= threshold) or (abs(threshold - fhigh) < absLimit): #Abs used as two floats are not equal even when they appear equal
				FP = FP + 1
			else:
				TN = TN + 1

		TPR = TP / (TP + FN)
		#print TP
		#print FN
		#print TPR
		FPR = 1 - TPR
		#print FPR

		TNR = TN / (TN + FP)
		#print TN
		#print FP
		#print TNR
		FNR = 1 - TNR
		#print FNR
		TP = 0
		FN = 0
		FP = 0
		TN = 0

		line = str(threshold) + ',' + str(FPR) + ',' + str(FNR) + '\n'
		#print line
		csvLines.append(line)

		threshold = threshold + thresholdInc
	
	fi = outDir + outCsv
	f = open(fi, 'w')
	for l in csvLines:
		f.write(l)

	print len(arrLeg)
	print len(arrIll)

	#f.close()

outDir = 'Outputs/'
#csvLeg = 'FinalCSVOrient/Legitimate/csvFinal2016_07_29_00_54_12.csv'
#csvIll = 'FinalCSVOrient/Illegitimate/csvFinal2016_07_29_01_17_51.csv'
csvLeg = 'FinalCSVOrient/Legitimate/csvFinal2016_08_16_23_53_51.csv'
csvIll = 'FinalCSVOrient/Illegitimate/csvFinal2016_08_16_23_50_51.csv'

Acc1MaePos = 1
Acc1CorPos = 2

Acc2MaePos = 4
Acc2CorPos = 5

Acc3MaePos = 7
Acc3CorPos = 8

Att1MaePos = 10
Att1CorPos = 11

Att2MaePos = 13
Att2CorPos = 14
Att2DotPos = 16
Att2DifPos = 17

Att3MaePos = 18
Att3CorPos = 19

Mag1MaePos = 21
Mag1CorPos = 22

Mag2MaePos = 24
Mag2CorPos = 25

Mag3MaePos = 27
Mag3CorPos = 28



Acc1MaeLeg = []
Acc1CorLeg = []
Acc1MaeIll = []
Acc1CorIll = []

Acc2MaeLeg = []
Acc2CorLeg = []
Acc2MaeIll = []
Acc2CorIll = []

Acc3MaeLeg = []
Acc3CorLeg = []
Acc3MaeIll = []
Acc3CorIll = []

Att1MaeLeg = []
Att1CorLeg = []
Att1MaeIll = []
Att1CorIll = []

Att2MaeLeg = []
Att2CorLeg = []
Att2DotLeg = []
Att2DifLeg = []
Att2MaeIll = []
Att2CorIll = []
Att2DotIll = []
Att2DifIll = []

Att3MaeLeg = []
Att3CorLeg = []
Att3MaeIll = []
Att3CorIll = []

Mag1MaeLeg = []
Mag1CorLeg = []
Mag1MaeIll = []
Mag1CorIll = []

Mag2MaeLeg = []
Mag2CorLeg = []
Mag2MaeIll = []
Mag2CorIll = []

Mag3MaeLeg = []
Mag3CorLeg = []
Mag3MaeIll = []
Mag3CorIll = []

f = open(csvLeg, 'r')

for line in f:
	#print line
	temp = line.split(',')

	if (temp[0] == '-'):
		continue
	if (temp[0] == 'Transaction'):
		continue

	Acc1MaeLeg.append(float(temp[Acc1MaePos]))
	Acc1CorLeg.append(float(temp[Acc1CorPos]))

	Acc2MaeLeg.append(float(temp[Acc2MaePos]))
	Acc2CorLeg.append(float(temp[Acc2CorPos]))

	Acc3MaeLeg.append(float(temp[Acc3MaePos]))
	Acc3CorLeg.append(float(temp[Acc3CorPos]))

	Att1MaeLeg.append(float(temp[Att1MaePos]))
	Att1CorLeg.append(float(temp[Att1CorPos]))

	Att2MaeLeg.append(float(temp[Att2MaePos]))
	Att2CorLeg.append(float(temp[Att2CorPos]))
	Att2DotLeg.append(float(temp[Att2DotPos]))
	Att2DifLeg.append(float(temp[Att2DifPos]))

	Att3MaeLeg.append(float(temp[Att3MaePos]))
	Att3CorLeg.append(float(temp[Att3CorPos]))

	Mag1MaeLeg.append(float(temp[Mag1MaePos]))
	Mag1CorLeg.append(float(temp[Mag1CorPos]))

	Mag2MaeLeg.append(float(temp[Mag2MaePos]))
	Mag2CorLeg.append(float(temp[Mag2CorPos]))

	Mag3MaeLeg.append(float(temp[Mag3MaePos]))
	Mag3CorLeg.append(float(temp[Mag3CorPos]))

f.close

f = open(csvIll, 'r')

for line in f:
	#print line
	temp = line.split(',')
	if (temp[0] == '-'):
		continue
	if (temp[0] == 'Transaction'):
		continue

	Acc1MaeIll.append(float(temp[Acc1MaePos]))
	Acc1CorIll.append(float(temp[Acc1CorPos]))

	Acc2MaeIll.append(float(temp[Acc2MaePos]))
	Acc2CorIll.append(float(temp[Acc2CorPos]))

	Acc3MaeIll.append(float(temp[Acc3MaePos]))
	Acc3CorIll.append(float(temp[Acc3CorPos]))

	Att1MaeIll.append(float(temp[Att1MaePos]))
	Att1CorIll.append(float(temp[Att1CorPos]))

	Att2MaeIll.append(float(temp[Att2MaePos]))
	Att2CorIll.append(float(temp[Att2CorPos]))
	Att2DotIll.append(float(temp[Att2DotPos]))
	Att2DifIll.append(float(temp[Att2DifPos]))

	Att3MaeIll.append(float(temp[Att3MaePos]))
	Att3CorIll.append(float(temp[Att3CorPos]))

	Mag1MaeIll.append(float(temp[Mag1MaePos]))
	Mag1CorIll.append(float(temp[Mag1CorPos]))

	Mag2MaeIll.append(float(temp[Mag2MaePos]))
	Mag2CorIll.append(float(temp[Mag2CorPos]))

	Mag3MaeIll.append(float(temp[Mag3MaePos]))
	Mag3CorIll.append(float(temp[Mag3CorPos]))

f.close

Acc1MaeLeg.sort()
Acc1CorLeg.sort()
Acc1MaeIll.sort()
Acc1CorIll.sort()

Acc2MaeLeg.sort()
Acc2CorLeg.sort()
Acc2MaeIll.sort()
Acc2CorIll.sort()

Acc3MaeLeg.sort()
Acc3CorLeg.sort()
Acc3MaeIll.sort()
Acc3CorIll.sort()

Att1MaeLeg.sort()
Att1CorLeg.sort()
Att1MaeIll.sort()
Att1CorIll.sort()

Att2MaeLeg.sort()
Att2CorLeg.sort()
Att2DotLeg.sort()
Att2DifLeg.sort()
Att2MaeIll.sort()
Att2CorIll.sort()
Att2DotIll.sort()
Att2DifIll.sort()

Att3MaeLeg.sort()
Att3CorLeg.sort()
Att3MaeIll.sort()
Att3CorIll.sort()

Mag1MaeLeg.sort()
Mag1CorLeg.sort()
Mag1MaeIll.sort()
Mag1CorIll.sort()

Mag2MaeLeg.sort()
Mag2CorLeg.sort()
Mag2MaeIll.sort()
Mag2CorIll.sort()

Mag3MaeLeg.sort()
Mag3CorLeg.sort()
Mag3MaeIll.sort()
Mag3CorIll.sort()



calculateFPRandFNR(Acc1MaeLeg, Acc1MaeIll, 'TestOutput.csv') #OK
#calculateFPRandFNR(Acc1CorLeg, Acc1CorIll, 'TestOutput2.csv') #OK
#calculateFPRandFNR(Acc2MaeLeg, Acc2MaeIll, 'TestOutput3.csv') #OK
#calculateFPRandFNR(Acc2CorLeg, Acc2CorIll, 'TestOutput4.csv') #OK
#calculateFPRandFNR(Acc3MaeLeg, Acc3MaeIll, 'TestOutput5.csv') #OK
#calculateFPRandFNR(Acc3CorLeg, Acc3CorIll, 'TestOutput5a.csv') #OK

#calculateFPRandFNR(Att1MaeLeg, Att1MaeIll, 'TestOutput6.csv') #OK WEIRD
#calculateFPRandFNR(Att1CorLeg, Att1CorIll, 'TestOutput7.csv') #OK
#calculateFPRandFNR(Att2MaeLeg, Att2MaeIll, 'TestOutput8.csv') #OK
#calculateFPRandFNR(Att2CorLeg, Att2CorIll, 'TestOutput9.csv') #OK
#calculateFPRandFNR(Att2DotLeg, Att2DotIll, 'TestOutput10.csv') #NOT OK NEEDS LOOKING AT
#calculateFPRandFNR(Att2DifLeg, Att2DifIll, 'TestOutput11.csv') #OK WEIRD
#calculateFPRandFNR(Att3MaeLeg, Att3MaeIll, 'TestOutput12.csv') #MATRIX NOT RATED
#calculateFPRandFNR(Att3CorLeg, Att3CorIll, 'TestOutput13.csv') #MATRIX NOT RATED

#calculateFPRandFNR(Mag1MaeLeg, Mag1MaeIll, 'TestOutput14.csv') #OK
#calculateFPRandFNR(Mag1CorLeg, Mag1CorIll, 'TestOutput15.csv') #OK
#calculateFPRandFNR(Mag2MaeLeg, Mag2MaeIll, 'TestOutput16.csv') #OK
#calculateFPRandFNR(Mag2CorLeg, Mag2CorIll, 'TestOutput17.csv') #OK
#calculateFPRandFNR(Mag3MaeLeg, Mag3MaeIll, 'TestOutput18.csv') #OK
#calculateFPRandFNR(Mag3CorLeg, Mag3CorIll, 'TestOutput19.csv') #OK

