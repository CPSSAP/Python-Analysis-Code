#Python modules
import os
import time
import datetime

#User defined modules
import quat
import location
import statFunctions
import dataProcessing
import audioProcessing

#Uncomment to process legitimate Ambient transactions
'''
#Path for the output csv file to be written for legitimate transactions
finalCSVDir = 'FinalCSVAmbient/Legitimate/'
#Path for the csv file containing legitimate transaction results for the Device
rootdirDev = 'Transactions_Ambient/Tests_Device_Leg'
#Path for the csv file containing legitimate transaction results for the Terminal
rootdirTer = 'Transactions_Ambient/Tests_Terminal_Leg'
'''

#Uncomment to process illegitimate Ambient transactions
'''
#Path for the final csv to be written for illegitimate transactions
finalCSVDir = 'FinalCSVAmbient/Illegitimate/'
#Path for the csv file containing illegitimate transaction results for the Device
rootdirDev = 'Transactions_Ambient/Tests_Device_Ill'
#Path for the csv file containing illegitimate transaction results for the Terminal
rootdirTer = 'Transactions_Ambient/Tests_Terminal_Ill'
'''

#Used for writing all info to file for each individual test so that it can be checked
checkFileNames = ['Location',
				'CLManager', 
				'CMManagerDevMotMag', 
				'CMManagerMag',  
				'Sound']

#Gets sub-directories of each root dir representing individual transactions, each member of set is a different transaction
#there should be an equal number of each. Each transaction has 9 csv files
deviceTransactionsSet = next(os.walk(rootdirDev))[1]
terminalTransactionsSet = next(os.walk(rootdirTer))[1]

#Get all the five csv files for each transaction, one each for Location and Sound, and three for Magnetometer
#Also retrieve the ID for comparison later [0]
#Full transaction name [1]
#Full path for log file [2]
#CSV files then start at [3]
deviceTransactions = dataProcessing.processTransactions(deviceTransactionsSet, rootdirDev)
terminalTransactions =  dataProcessing.processTransactions(terminalTransactionsSet, rootdirTer)

#Set up top two rows for final csv output
finalCSV = []
topRow = '-,-,'
secondRow = 'Transaction,'

for x in range (0, 4):
	topRow = topRow + checkFileNames[x] + ',-,-,'
topRow = topRow + checkFileNames[4] + ',-\n'
finalCSV.append(topRow)

#Second row setup
for x in range (0, 4):
	if (x == 0): #Location
		secondRow = secondRow + 'MAE,HAV,COR1,'
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
			print deviceTransactions[idx][0]
			tempRow = []
			tempRow.append(deviceTransactions[idx][0]) #Transaction ID
			#Starts at 3 because thats where csv files start
			for x in range(3, 8): #<8

				if (x == 3):
					#Location
					tup = location.processLocationData(deviceTransactions[idx][x], terminalTransactions[idx][x])
					print tup[0]
					print tup[1]
					eqTup = dataProcessing.equaliseLists(tup[0], tup[1])
					MAE = '-'
					HAV = location.getMeanHaversine(eqTup[0], eqTup[1])
					COR2 = '-'

					tempRow.append(MAE)
					tempRow.append(HAV)
					tempRow.append(COR2)

				elif (x == 7):
					#Sound
					relTimeTup = dataProcessing.getMinusTimeForSound(deviceTransactions[idx][2], terminalTransactions[idx][2])
					relTime = relTimeTup[0]
					print relTime
					recToTarget = relTimeTup[1]
					print recToTarget
					MAE = '-'
					COR = audioProcessing.getAudioCorrCoef(deviceTransactions[idx][x], terminalTransactions[idx][x], relTime, recToTarget)
					COR2 = '-'

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
			print 'Error, transaction IDs different'
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
