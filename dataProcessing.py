import os
import quat
import rotMat
import functions
import numpy as np

checkFiles = '/Users/XXX/Desktop/Check/'

interpVals = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 
				100, 110, 120, 130, 140, 150, 160, 170, 180, 190,
				200, 210, 220, 230, 240, 250, 260, 270, 280, 290,
				300, 310, 320, 330, 340, 350, 360, 370, 380, 390,
				400, 410, 420, 430, 440, 450, 460, 470, 480, 490,
				500]

deviceTransactions = []
terminalTransactions = []

def processTransactions(tranSet, rootDir):
	DevTerTransactions = []
	for transactionDir in tranSet:
		deviceFiles = []
		testName = transactionDir
		#Transaction ID used to make sure the data being compared is from the same transaction
		transactionID = extractTimeStampTitle(testName)
		#First element added to array
		deviceFiles.append(transactionID)
		#Full test name, with Device/Terminal/Non BT Moniker included, secdond element in array
		deviceFiles.append(testName)
		
		filesTestDirSet = next(os.walk(os.path.join(rootDir, transactionDir)))[2]
		#Extract the file path for the log file
		for file in filesTestDirSet:
			
			if (file[-4:] == '.log'):
				logFile = os.path.join(rootDir, transactionDir, file)
				
				#Thrid element in array
				deviceFiles.append(logFile)


		testDirSet = next(os.walk(os.path.join(rootDir, transactionDir)))[1]
		#Extract the file paths for all the csv data files
		for testDir in testDirSet:
			fileSet = next(os.walk(os.path.join(rootDir, transactionDir, testDir)))[2]
			
			for file in fileSet:
				if (file == '.DS_Store'):
					pass
				else:
					tempFile = os.path.join(rootDir, transactionDir, testDir, file)
					deviceFiles.append(tempFile)

		DevTerTransactions.append(deviceFiles)
	
	return DevTerTransactions

def extractTimeStampTitle(testNm):
	#Returns title input by user with time stamp, Device or Terminal moniker removed and replaced with Leg
	#This is so both transaction names are the same. Ill added for Non BT mode
	temp = testNm.split('#')
	appendix = ''
	if (temp[1] == '_Device'):
		appendix = 'Leg'
	if (temp[1] == '_Terminal'):
		appendix = 'Leg'
	if (temp[1] == '_NonBTMode'):
		appendix = 'Ill'
	full = temp[0] + '_' + appendix
	
	return full

def getMinusTime(csv1, csv2):
	#For non-bluetooth mode we must figure out which of the csv files started recording readings before the other
	#In bluetooth mode its nearly always the slave/terminal that begins second as it must wait for signal but in non
	#bluetooth it can be either.

	#Get time for first reading on first csv
	with open(csv1, 'r') as f:
		first_line = f.readline()
	line = first_line.split(',')
	timeCS1 = line[0]

	#Get time for first reading on second csv
	with open(csv2, 'r') as f:
		first_line = f.readline()
	line = first_line.split(',')
	timeCS2 = line[0]

	if (timeCS1 >= timeCS2): 
		return timeCS1
	else: 
		return timeCS2


def getMinusTimeForSound(logFile1, logFile2):
	log1 = open(logFile1, 'r')
	log2 = open(logFile2, 'r')
	log1Time = ''
	log2Time = ''

	for line in log1:
		if '###' in line:
			temp = line.split('###')
			log1Time = float(temp[1])

	for line in log2:
		if '###' in line:
			temp = line.split('###')
			log2Time = float(temp[1])

	if (log1Time >= log2Time): 
		tempLogTime = log1Time - log2Time
		return (tempLogTime, 2)
	else: 
		tempLogTime = log2Time - log1Time
		return (tempLogTime, 1)

#because of way time shift is applied there could be for some sensors an unequal number of zero readings on either side
#this function turns any zeros on one side into zero on the other and also equalises the size of both arrays
def equaliseZerosAndLists(agg1, agg2, times1, times2):
	retAgg1 = []
	retTime1 = []
	retAgg2 = []
	retTime2 = []

	if(len(agg2) <= len(agg1)):
		l = len(agg2)
	else:
		l = len(agg1)
	
	for i in range(0, l):
		retTime1.append(times1[i])
		retTime2.append(times2[i])

		if(agg1[i] == 0):
			retAgg1.append(agg1[i])
			retAgg2.append(0)
		elif(agg2[i] == 0):
			retAgg1.append(0)
			retAgg2.append(agg2[i])
		else:
			retAgg1.append(agg1[i])
			retAgg2.append(agg2[i])
	
	return (retAgg1, retAgg2, retTime1, retTime2)

#Makes sure both lists are same length by removing elements from longer list if neccessary, used by various other modules
def equaliseLists(ls1, ls2):
	a = len(ls1)
	b = len(ls2)
	temp = []

	if (a == b):
		return (ls1, ls2)
	if (a < b):
		for i in range(0, a):
			temp.append(ls2[i])
		return (ls1, temp)
	else:
		for i in range(0, b):
			temp.append(ls1[i])
		return (temp, ls2)

def interpolateAndEqualiseReadings(cs1, cs2, checkFile, testName):
	#Open both csv files, one from device and one from terminal, represent sensor readings and time of reading
	csv1 = open(cs1)
	csv2 = open(cs2)

	#Extract the latest of the first sensor reading on device and the first sensor reading on terminal, 
	#for BT tests time for first terminal reading should always be later than time for first device reading
	#Non BT tests this is not always the case. This time is used to minus from both sides meaning the side it 
	#was extracted from goes to zero and the other side goes into a minus figure. This time is minused from 
	#from each reading on this side until a positive figure is found
	minusTime = float(getMinusTime(cs1,cs2))

	tempTime1 = []
	tempTime2 = []
	tempAggVal1 = []
	tempAggVal2 = []

	qDot1 = []
	qDot2 = []

	for line in csv1:

		temp = line.split(',')
		#This value represents the value returned by subtracting the later of the first sensor readings
		#which we get from getMinusTime(). On the side (Device or Terminal) that had that reading the relative 
		#time will now be zero and we can take the readsing associated with it. On the other side the time will 
		#now be a minus figure and the reading is discarded. We keep taking readings where the relative time is 
		#under 550ms and above zero, this syncs the two sides and gives us values that match closely time wise
		relTime = (float(temp[0]) - minusTime) * 1000

		if ((relTime >= 0) and (relTime < 550)):

			if (checkFile == 'AttitudeQuaternion'):

				q = [float(temp[1]), float(temp[2]), float(temp[3]), float(temp[4])]
				#Converts Quaternion into three Euler angles
				angles = quat.quaternionToEuler(q)
				#These three values can then be reduced to one using vector magnitude
				tempValAgg = functions.vectorMagnitude(angles[0], angles[1], angles[2])
				#Append value to array
				tempAggVal1.append(tempValAgg)
				#Append relavent time 
				tempTime1.append(relTime)

			elif (checkFile == 'AttitudeRotationMatrix'):
				rm = [float(temp[1]), float(temp[2]), float(temp[3]), float(temp[4]), float(temp[5]), 
				float(temp[6]), float(temp[7]), float(temp[8]), float(temp[9])]
				#print rm

				angles = rotMat.rotMatToEuler(rm)
				tempValAgg = functions.vectorMagnitude(angles[0], angles[1], angles[2])
				tempAggVal1.append(tempValAgg)
				tempTime1.append(relTime)

			elif (checkFile == 'QuaternionDOT'):
				if (relTime <= 500): #Needed as Quaternions are not interpolated
					q1 = [float(temp[1]), float(temp[2]), float(temp[3]), float(temp[4])]
					qDot1.append(q1)

			else:
				#Values reduced to single figure
				tempValAgg = functions.vectorMagnitude(float(temp[1]), float(temp[2]), float(temp[3]))
				#Append value to array
				tempAggVal1.append(tempValAgg)
				#Append relavent time 
				tempTime1.append(relTime)
				
		else:
			pass
	
	csv1.close()

	for line in csv2:
		temp = line.split(',')
		#See comments above
		relTime = (float(temp[0]) - minusTime) * 1000

		if ((relTime >= 0) and (relTime < 550)):

			if (checkFile == 'AttitudeQuaternion'):
				q = [float(temp[1]), float(temp[2]), float(temp[3]), float(temp[4])]
				angles = quat.quaternionToEuler(q)
				tempValAgg = functions.vectorMagnitude(angles[0], angles[1], angles[2])
				tempAggVal2.append(tempValAgg)
				tempTime2.append(relTime)

			elif (checkFile == 'AttitudeRotationMatrix'):
				rm = [float(temp[1]), float(temp[2]), float(temp[3]), float(temp[4]), float(temp[5]), 
				float(temp[6]), float(temp[7]), float(temp[8]), float(temp[9])]
				#print rm

				angles = rotMat.rotMatToEuler(rm)
				tempValAgg = functions.vectorMagnitude(angles[0], angles[1], angles[2])
				tempAggVal2.append(tempValAgg)
				tempTime2.append(relTime)

			elif (checkFile == 'QuaternionDOT'):
				if (relTime <= 500): #Needed as Quaternions are not interpolated
					q2 = [float(temp[1]), float(temp[2]), float(temp[3]), float(temp[4])]
					qDot2.append(q2)

			else:
				tempValAgg = functions.vectorMagnitude(float(temp[1]), float(temp[2]), float(temp[3]))
				tempAggVal2.append(tempValAgg)
				tempTime2.append(relTime)
			
		else:
			pass

	csv2.close()

	#Quaternions are not interpolated as there arent as many readings collected as the four values are used to calculate a single value
	#using dot product and difference of angles
	if (checkFile == 'QuaternionDOT'):
		return equaliseLists(qDot1, qDot2)
		
	tup = equaliseZerosAndLists(tempAggVal1, tempAggVal2, tempTime1, tempTime2)

	tempAggVal1 = tup[0]
	tempAggVal2 = tup[1]
	tempTime1 = tup[2]
	tempTime2 = tup[3]

	print testName
	print checkFile

	arr = np.interp(interpVals, tempTime1, tempAggVal1)
	arr2 = np.interp(interpVals, tempTime2, tempAggVal2)
	
	outName = checkFiles + testName + '/' + checkFile + '.csv'

	if not os.path.exists(os.path.dirname(outName)):
		try:
			os.makedirs(os.path.dirname(outName))
		except OSError as exc: # Guard against race condition
			if exc.errno != errno.EEXIST:
				raise

	f = open(outName, 'w')
	f.write('Inter Time (ms), Orig Time 1, Orig Time 2, Orig Val 1, Orig Val 2, Inter Val 1, Inter Val 2\n')
	for idx, val in enumerate(tempTime1):
		if (idx <= 50):
			f.write(str(idx * 10) + ',' + str(tempTime1[idx]) + ',' + str(tempTime2[idx]) + ',' + str(tempAggVal1[idx]) + ',' + str(tempAggVal2[idx]) + ',' + str(arr[idx]) + ',' + str(arr2[idx]) + '\n')
	f.close()
	
	return (arr, arr2)








