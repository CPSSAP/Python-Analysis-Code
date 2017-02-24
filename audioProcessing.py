import scipy.io.wavfile as sio
import scipy
import numpy
import dataProcessing

def getAudioCorrCoef(audFilePath1, audFilePath2, relTime, recToTgt):
	(sr1, data1) = sio.read(audFilePath1)
	(sr2, data2) = sio.read(audFilePath2)
	redArr = []
	staticArr = []
	print len(data1)
	print len(data2)

	#temp = dataProcessing.equaliseLists(data1, data2) #not sure it will need this as 2 secs seems to always = 88200 samples (44100 * 2)

	sampleRed = int(44100 * relTime)
	print sampleRed
	#print sampleRed
	ms500 = 44100 / 2

	if (recToTgt == 1):
		sampToRed = data1
		staticSamp = data2
	elif (recToTgt == 2):
		sampToRed = data2
		staticSamp = data1

	print len(sampToRed)
	print len(staticSamp)

	#Equalise time wise by subtracting ammount of samples from 
	for x in range(sampleRed, len(staticSamp)): #Can be len staticSamp or sampToRed, they are same length
		redArr.append(sampToRed[x])
	
	print len(redArr)
	'''
	print redArr[0]
	print redArr[1]
	print sampToRed[6552]
	print sampToRed[6553]
	'''
	#Covert other nump array to normal array/list so work can be done on it
	staticArr = staticSamp.tolist()
	#Now equalise both
	staticArr500 = staticArr[:ms500]
	#print len(staticArr500)
	redArr500 = redArr[:ms500]
	'''
	print len(redArr500)
	print redArr500[0]
	print redArr500[1]
	'''


	signalArray1 = numpy.array(staticArr500)
	signalArray2 = numpy.array(redArr500)

	#print signalArray1
	print len(signalArray1)
	print len(signalArray2)

	ret =  numpy.corrcoef(signalArray1, signalArray2, rowvar=0)
	print ret[1,0]
	return ret[1,0]

