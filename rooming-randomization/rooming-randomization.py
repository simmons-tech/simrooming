#################################
# Simmons Rooming Randomization #
#################################

#################################
# Instructions:
#
# 1. Create a csv file named "in.csv" with the following format:
#    - Column 1 has names of students in any format you wish.
#    - Column 2 has years matching the format specified in YEARS_ORDER below.
#
# 2. Place the csv file in the same directory as this file.
#
# 3. Agree upon a randomly chosen seed: chosen with witnesses or from
#       an agreed-upon external source of randomness (day's lottery numbers...)
#    By choosing this seed, the randomization process can be repeated and code
#       verified by interested third parties.
#
# 4. Set RANDOM_SEED to this value.
#
# 5. Run 'python rooming-randomization.py'.
#
# 6. The randomized ordering will be written to the file "out.csv".
#
#################################

RANDOM_SEED = 1842
YEARS_ORDER = ["Senior", "Incoming Senior", "9th/10th term", "Incoming 9th/10th term", "Junior", "Incoming Junior", "Sophomore", "Incoming Sophomore"]
INPUT_FILENAME = "in.csv"
OUTPUT_FILENAME = "out.csv"

import csv, random
from collections import defaultdict

# Reads the names dictionary from the input file.
def importNames(inputFilename):
    # Setting up namesDict, a mapping from year names to lists of names in that year.
    namesDict = dict()
    for year in YEARS_ORDER:
        namesDict[year] = []

    # Reads the names and years from the input CSV file.
    csvFile = open(inputFilename, 'r')
    csvReader = csv.reader(csvFile, delimiter=',')
    for row in csvReader:
        name = row[0]
        year = row[1]
        if year not in namesDict:
            print "ERROR:", name, "has invalid year", year
        block = ''
        if len(row) > 2:
            block = row[2]
        namesDict[year].append((name, block))
    return namesDict

# Randomizes the name list for each year in the names dict.
def shuffleNames(namesDict):
    shuffledNamesDict = dict()
    for (year, namesList) in namesDict.items():
        # Copies and randomly shuffles the names list.
        shuffledNamesDict[year] = namesList[:]
        random.shuffle(shuffledNamesDict[year])
    return shuffledNamesDict

# Merges the years into a list of tuples [(name, year, block, pick)]
# with pick being the pre-blocked pick for each name.
def getPickOrder(shuffledNamesDict):
    pickOrder = []
    for year in YEARS_ORDER:
        shuffledNames = shuffledNamesDict[year]
        for (name, block) in shuffledNames:
            pickOrder.append((name, year, block))
    return pickOrder

# Merges the blocks to have the same pick for all members of the block.
def getBlockedOrder(pickOrder):
    # Group the blocks into lists, stored in blockedPicks.
    blockedPicks = dict()
    for pick in xrange(len(pickOrder)):
        (name, year, block) = pickOrder[pick]
        if block == '':
            blockedPicks[name] = [(name, year, block, pick)]
        else:
            if '#' + block not in blockedPicks:
                blockedPicks['#' + block] = []
            blockedPicks['#' + block].append((name, year, block, pick))

    # Average the picks for each block, stored in averagedBlockPicks.
    averagedBlockPicks = []
    tieBreakers = range(len(blockedPicks))
    random.shuffle(tieBreakers)
    blockCount = 0
    for (block, blockList) in blockedPicks.items():
        blockPicks = [pick for (name, year, block, pick) in blockList]
        averageBlockPick = 1.0 * sum(blockPicks) / len(blockPicks)
        averagedBlockPicks.append((block, blockList, averageBlockPick, tieBreakers[blockCount]))
        blockCount += 1

    # Sort on average block pick first and then the tiebreaker value.
    sortedBlockOrder = sorted(averagedBlockPicks,
                              key = lambda (block, blockList, averageBlockPick, tieBreaker): (averageBlockPick, tieBreaker))

    # Extract blocks into a list of names.
    finalPickOrder = []
    finalRank = 0
    for (block, blockList, finalBlockPick, tieBreaker) in sortedBlockOrder:
        for (name, year, block, pick) in blockList:
            finalPickOrder.append((finalRank, name, year, block, pick, finalBlockPick, tieBreaker))
            finalRank += 1
    return finalPickOrder

# Writes the final ordering to the output file.
def exportNames(outputFilename, finalOrder):
    outFile = open(outputFilename, 'w')
    csvWriter = csv.writer(outFile, lineterminator='\n')
    csvWriter.writerow(('Final Rank', 'Kerberos', 'Year', 'Block', 'Initial Rank', 'Weighted Rank', 'Tie Breaker'))
    csvWriter.writerow(('-1', 'jessig & emessig', '', '', '-1', '-1', '-1'))
    for orderTuple in finalOrder:
        csvWriter.writerow(orderTuple)
    outFile.close()


# Kick it off!
random.seed(RANDOM_SEED)
namesDict = importNames(INPUT_FILENAME)
shuffledNamesDict = shuffleNames(namesDict)
pickOrder = getPickOrder(shuffledNamesDict)
blockedOrder = getBlockedOrder(pickOrder)
exportNames(OUTPUT_FILENAME, blockedOrder)
