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

outDir = 'OutputsAmbient/'
#Set to the csv files generated from the AmbientDataProcessing.py module
#one csv for illegitimate and one for legitimate transactions
csvLeg = 'FinalCSVAmbient/Legitimate/csvFinal2016_08_10_13_10_27.csv'
csvIll = 'FinalCSVAmbient/Illegitimate/csvFinal2016_08_10_14_25_24.csv'

LocHav = 2

Mag1MaePos = 4
Mag1CorPos = 5

Mag2MaePos = 7
Mag2CorPos = 8

Mag3MaePos = 10
Mag3CorPos = 11

Sound = 14

LocHavLeg = []
LocHavIll = []

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

SoundLeg = []
SoundIll = []

f = open(csvLeg, 'r')

for line in f:
	#print line
	temp = line.split(',')
	if (temp[0] == '-0'):
		continue
	if (temp[0] == 'Transaction'):
		continue

	#print temp[LocHav]

	LocHavLeg.append(float(temp[LocHav]))

	Mag1MaeLeg.append(float(temp[Mag1MaePos]))
	Mag1CorLeg.append(float(temp[Mag1CorPos]))

	Mag2MaeLeg.append(float(temp[Mag2MaePos]))
	Mag2CorLeg.append(float(temp[Mag2CorPos]))

	Mag3MaeLeg.append(float(temp[Mag3MaePos]))
	Mag3CorLeg.append(float(temp[Mag3CorPos]))

	SoundLeg.append(float(temp[Sound]))

f.close

f = open(csvIll, 'r')

for line in f:
	#print line
	temp = line.split(',')
	if (temp[0] == '-0'):
		continue
	if (temp[0] == 'Transaction'):
		continue

	LocHavIll.append(float(temp[LocHav]))

	Mag1MaeIll.append(float(temp[Mag1MaePos]))
	Mag1CorIll.append(float(temp[Mag1CorPos]))

	Mag2MaeIll.append(float(temp[Mag2MaePos]))
	Mag2CorIll.append(float(temp[Mag2CorPos]))

	Mag3MaeIll.append(float(temp[Mag3MaePos]))
	Mag3CorIll.append(float(temp[Mag3CorPos]))

	SoundIll.append(float(temp[Sound]))

f.close

LocHavLeg.sort()
LocHavIll.sort()

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

SoundLeg.sort()
SoundIll.sort()

#Uncomment whichever file you want to process 

#calculateFPRandFNR(LocHavLeg, LocHavIll, 'TestOutput.csv')

#calculateFPRandFNR(Mag1MaeLeg, Mag1MaeIll, 'TestOutput2.csv') #OK
#calculateFPRandFNR(Mag1CorLeg, Mag1CorIll, 'TestOutput3.csv') #OK
#calculateFPRandFNR(Mag2MaeLeg, Mag2MaeIll, 'TestOutput4.csv') #OK
#calculateFPRandFNR(Mag2CorLeg, Mag2CorIll, 'TestOutput5.csv') #OK
#calculateFPRandFNR(Mag3MaeLeg, Mag3MaeIll, 'TestOutput6.csv') #OK
#calculateFPRandFNR(Mag3CorLeg, Mag3CorIll, 'TestOutput7.csv') #OK

#calculateFPRandFNR(SoundLeg, SoundIll, 'TestOutput8.csv')

