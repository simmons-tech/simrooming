######################################
# Simmons Rooming Randomization 2014 #
######################################

import csv, random
from collections import defaultdict

INPUT_FILENAME = "in.csv"
RANDOM_SEED = 83884746
YEARS_ORDER = ["Junior", "Sophomore", "Incoming Sophomore", "Freshman", "Incoming Freshman"]
OUTPUT_FILENAME = "out.csv"

def initRandom():
        random.seed(RANDOM_SEED)	

def shuffleList(originalList):
	newList = originalList[:]
	random.shuffle(newList)
	return newList

def setupNamesDict():
	namesDict = dict()
	for year in YEARS_ORDER:
		namesDict[year] = []
	return namesDict

def importNames(inputFilename):
	namesDict = setupNamesDict()	
	csvFile = open(inputFilename, 'r')
	csvReader = csv.reader(csvFile, delimiter=',')
	for row in csvReader:
		name = row[0]
		year = row[1]
		if year not in namesDict:
			print "ERROR: ", name, "has invalid year", year
		namesDict[year].append(name)
	return namesDict

def shuffleNames(namesDict):
	shuffledNamesDict = dict()
	for (year, namesList) in namesDict.items():
		shuffledNamesDict[year] = shuffleList(namesList)
	return shuffledNamesDict

# returns list of tuples [(name, year, finalCount)]
def getFinalOrder(shuffledNamesDict):
	finalOrder = []
	finalCount = 0
	for year in YEARS_ORDER:
		shuffledNames = shuffledNamesDict[year]
		for name in shuffledNames:
			finalCount += 1
			finalOrder.append((name, year, finalCount))
	return finalOrder

def exportNames(outputFilename, finalOrder):
	outFile = open(outputFilename, 'w')
	csvWriter = csv.writer(outFile)
	for orderTuple in finalOrder:
		csvWriter.writerow(orderTuple)
	outFile.close()

def main():
	initRandom()
	namesDict = importNames(INPUT_FILENAME)
	shuffledNamesDict = shuffleNames(namesDict)
	finalOrder = getFinalOrder(shuffledNamesDict)
	exportNames(OUTPUT_FILENAME, finalOrder)

# Kick it off
main()
