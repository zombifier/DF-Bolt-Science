import sys
import re
from statistics import mean
from statistics import stdev
import matplotlib.pyplot as plt

if len(sys.argv) == 1:
    print('Provide a list of file names')
    exit()

class Data:
    def __init__(self):
        self.count = 0
        self.uncCount = 0

HIT = 'strikes Goblin (\d+)'
FALL = 'Goblin (\d+) falls over'
UNC = 'Goblin (\d+) gives in'
UNC2 = 'Goblin (\d+) has been knocked unconscious'
DEAD = 'Goblin (\d+) has suffocated'
DEAD2 = 'Goblin (\d+) has bled to death'
DEAD3 = 'Goblin (\d+) has been shot and killed'

values = []

for fileName in sys.argv[1:]:
    dataDict = {}
    file = open(fileName, 'r')
    for line in file:
        hitMatch = re.search(HIT, line)
        if hitMatch:
            number = hitMatch.group(1)
            if number not in dataDict:
                dataDict[number] = Data()
            dataDict[number].count += 1
        uncMatch = re.search(UNC, line) or re.search(UNC2, line) or re.search(DEAD, line) or re.search(DEAD2, line) or re.search(DEAD3, line)
        if uncMatch:
            number = uncMatch.group(1)
            dataDict[number].uncCount = dataDict[number].uncCount or dataDict[number].count
    values.extend(dataDict.values())

totalValues = list(map(lambda data: data.count, values))
uncValues = list(filter(lambda value: value > 0, map(lambda data: data.uncCount, values)))

print('average bolts to render unconscious: ', mean(uncValues))
print('stdev: ', stdev(uncValues))
print('ratio of goblins knocked unconscious after 250 bolts - only use above values if this is 1.0: ', len(uncValues) / len(totalValues))
