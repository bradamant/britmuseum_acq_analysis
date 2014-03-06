#!/usr/bin/env python
# Simple report of all the years of data 

import sys, pymongo
from pymongo import Connection

try:
	connection = Connection()
	db = connection.britishmuseum
	acquisitions = db.acquisitions
except:
	print("Database connection problem.")
	sys.exit()

floorFetch = acquisitions.aggregate([
		{"$group": {"_id": 0, "minyear": {"$min": "$year"}}}
		])
floor = floorFetch['result'][0]['minyear']
ceilingFetch = acquisitions.aggregate([
		{"$group": {"_id": 0, "maxyear": {"$max": "$year"}}}
		])
ceiling = ceilingFetch['result'][0]['maxyear']
print "Floor is " + str(floor)
print "Ceiling is " + str(ceiling)


listOfCountries = acquisitions.find().distinct("locality")
listOfCountries.sort()
print "Number of countries is " + str(len(listOfCountries))

#print CSV header
sys.stdout.write("country,")
for year in range(floor,ceiling):
	sys.stdout.write(str(year) + ",")
#Print data
for country in listOfCountries:
	sys.stdout.write("\n")
	sys.stdout.write(country + ",")
	for year in range(floor,ceiling):
		countResult = acquisitions.find_one({"year":year,"locality":country},{"_id":0,"count":1})
		if countResult == None:
			sys.stdout.write("0")
		else:
			sys.stdout.write(str(countResult['count']))
		sys.stdout.write(",")

