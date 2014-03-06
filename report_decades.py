#!/usr/bin/env python
# Results display for Kivrin biography explorer

import sys, pymongo
from pymongo import Connection

# Round to encompass as many decades as possible
# via http://stackoverflow.com/questions/2272149/round-to-5or-other-number-in-python
def roundTenD(x, base=10):
	return int(base * round(float(x)/base))
def roundTenU(x, base=10):
		return int(base * round(float(x)/base)) + 10

try:
	connection = Connection()
	db = connection.britmuseum
	acquisitions = db.acquisitions
except:
	print("Database connection problem.")
	sys.exit()

floorFetch = acquisitions.aggregate([
		{"$group": {"_id": 0, "minyear": {"$min": "$year"}}}
		])
floor = roundTenD(floorFetch['result'][0]['minyear'])
ceilingFetch = acquisitions.aggregate([
		{"$group": {"_id": 0, "maxyear": {"$max": "$year"}}}
		])
ceiling = roundTenU(ceilingFetch['result'][0]['maxyear'])
print "Floor is " + str(floor)
print "Ceiling is " + str(ceiling)


listOfCountries = acquisitions.find().distinct("locality")
listOfCountries.sort()
print "Number of countries is " + str(len(listOfCountries))
listOfDates = []

#print CSV header
sys.stdout.write("country,")
for year in range(floor,ceiling):
	if year % 10 == 0:
		roundDown = year - 10 # we want to call decade ending 1760 the 1750s not the 1760s
		sys.stdout.write(str(roundDown) + "s,")
		listOfDates.append(roundDown)
		
#Print data
for country in listOfCountries:
	sys.stdout.write("\n")
	sys.stdout.write(country + ",")	
	for decade in listOfDates:
		runningCount = 0
		for increment in range(0,9):
			year = decade + increment	
			countResult = acquisitions.find_one({"year":year,"locality":country},{"_id":0,"count":1})
			if countResult != None:
				runningCount += countResult['count']
		#Then when it *is* the decade, add final year's data and sum
		sys.stdout.write(str(runningCount) + ",")
