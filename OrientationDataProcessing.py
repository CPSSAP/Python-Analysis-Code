#Python modules
import os
import time
import datetime

#User defined modules
import quat
import statFunctions
import dataProcessing

#STEP 1. Comment out the file paths not being used

#Uncomment to process legitimate Orientation transactions
'''
#Path for the final csv file to be written for legitimate transactions
finalCSVDir = 'FinalCSVOrient/Legitimate/'
#Path for the csv file containing legitimate transaction results for the Device
rootdirDev = 'Transactions_Orient/Tests_Device_Leg'
#Path for the csv file containing legitimate transaction results for the Terminal
rootdirTer = 'Transactions_Orient/Tests_Terminal_Leg'
'''

#Uncomment to process illegitimate Orientation transactions

#Path for the final csv to be written for illegitimate transactions
finalCSVDir = 'FinalCSVOrient/Illegitimate/'
#Path for the csv file containing illegitimate transaction results for the Device
rootdirDev = 'Transactions_Orient/Tests_Device_Ill'
#Path for the csv file containing illegitimate transaction results for the Terminal
rootdirTer = 'Transactions_Orient/Tests_Terminal_Ill'


#Used for writing all info to file for each individual test so that it can be checked
checkFileNames = ['CMManagerAcc', 
				'CMManagerDevMotAcc', 
				'CMManagerDevMotAccGrav', 
				'Attitdue', 
				'AttitudeQuaternion', 
				'AttitudeRotationMatrix', 
				'CLManager', 
				'CMManagerDevMotMag', 
				'CMManagerMag']

#Gets sub-directories of each root dir representing individual transactions, each member of set is a different transaction
#there should be an equal number of each. Each transaction has 9 csv files
deviceTransactionsSet = next(os.walk(rootdirDev))[1]
terminalTransactionsSet = next(os.walk(rootdirTer))[1]

#Get all the nine csv files for each transaction, three each for Magnetometer, Attitude and Accelerometer
#Also retrieve the ID for comparison later [0]
#Full transaction name [1]
#Full path for log file [2]
#CSV files then start at [3]
terminalTransactions =  dataProcessing.processTransactions(terminalTransactionsSet, rootdirTer)
deviceTransactions = dataProcessing.processTransactions(deviceTransactionsSet, rootdirDev)

#Set up top row for final csv output
finalCSV = []
topRow = '-,-,'
secondRow = 'Transaction,'

for x in range (0, 8):
	if (x == 4): #Quaternion
		topRow = topRow + '-,' + checkFileNames[x] + ',-,-,-,'
	else:
		topRow = topRow + checkFileNames[x] + ',-,-,'
topRow = topRow + checkFileNames[8] + ',\n'
finalCSV.append(topRow)

#Second row
for x in range (0, 8):
	if (x == 4): #Quaternion
		secondRow = secondRow + 'MAE,COR,COR1,DOT,DIFF,'
	else:
		secondRow = secondRow + 'MAE,COR,COR1,'
secondRow = secondRow + 'MAE,COR,COR1\n'
finalCSV.append(secondRow)

#List of lists, each list being a collection of objects that will make in row in csv (TranID, MAE, COR ....) 
Rows = []

#Make sure there are an equal number of trnsactions on both sides Device/Terminal
if (len(deviceTransactions) == len(terminalTransactions)):
	#Iterate through both transaction directories using length of deviceTransactions as iterator
	#Both are same size so could have used either length of deviceTransactions or terminalTransactions
	for idx, val in enumerate(deviceTransactions):
		#Compare transaction IDs
		if (deviceTransactions[idx][0] == terminalTransactions[idx][0]):
			#Its same transaction, one from device and one from terminal
			tempRow = []
			tempRow.append(deviceTransactions[idx][0]) #Transaction ID
			#Starts at 3 because thats where csv files start
			for x in range(3, 12): #x < 12 Iterates through nine csv files

				if (x == 7): #Quaternion is special case
					
					tup = dataProcessing.interpolateAndEqualiseReadings(deviceTransactions[idx][x], terminalTransactions[idx][x], checkFileNames[x - 3], deviceTransactions[idx][1])
					#Interpolated values used to obtain MAE, COR .etc
					MAE = statFunctions.meanAbsoluteError(tup[0], tup[1])
					COR = statFunctions.correlationCoefficient(tup[0], tup[1])
					COR2 = statFunctions.pearsonCorrelationCoefficient(tup[0], tup[1])

					tup2 = dataProcessing.interpolateAndEqualiseReadings(deviceTransactions[idx][x], terminalTransactions[idx][x], 'QuaternionDOT', deviceTransactions[idx][1])
					DOT = quat.dotProductMean(tup2[0], tup2[1])
					DIFF = quat.angleDiffMean(tup2[0], tup2[1])

					#Returns five values for comparison as opposed to three
					tempRow.append(MAE)
					tempRow.append(COR)
					tempRow.append(COR2)
					tempRow.append(DOT)
					tempRow.append(DIFF)
				
				elif (x == 8):
					#rotation Matrix not yet implemented
					tup = dataProcessing.interpolateAndEqualiseReadings(deviceTransactions[idx][x], terminalTransactions[idx][x], checkFileNames[x - 3], deviceTransactions[idx][1])
					#MAE = '-'
					#COR = '-'
					#COR2 = '-'
					MAE = statFunctions.meanAbsoluteError(tup[0], tup[1])
					COR = statFunctions.correlationCoefficient(tup[0], tup[1])
					COR2 = statFunctions.pearsonCorrelationCoefficient(tup[0], tup[1])

					tempRow.append(MAE)
					tempRow.append(COR)
					tempRow.append(COR2)

				else:
					tup = dataProcessing.interpolateAndEqualiseReadings(deviceTransactions[idx][x], terminalTransactions[idx][x], checkFileNames[x - 3], deviceTransactions[idx][1])
					MAE = statFunctions.meanAbsoluteError(tup[0], tup[1])
					COR = statFunctions.correlationCoefficient(tup[0], tup[1])
					COR2 = statFunctions.pearsonCorrelationCoefficient(tup[0], tup[1])

					tempRow.append(MAE)
					tempRow.append(COR)
					tempRow.append(COR2)
				
			Rows.append(tempRow)

		else:
			print 'Error, transaction IDs different ' + str(deviceTransactions[idx][0]) + ' != ' + str(terminalTransactions[idx][0])
else:
	print 'Error, device and terminal transaction arrays are different lengths'


#Process row lists into csv format and then add to final csv
rowString = ''
for x in Rows:
	for y in range(0, (len(x) - 1)):
		rowString = rowString + str(x[y]) + ','
	rowString = rowString + str(x[len(x) - 1]) + '\n'
	finalCSV.append(rowString)
	rowString = ''

#Write final csv to file
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y_%m_%d_%H_%M_%S')
fileOut = finalCSVDir + 'csvFinal' + str(st) + '.csv'
f = open(fileOut, 'w')
for x in finalCSV:
	f.write(x)
f.close()