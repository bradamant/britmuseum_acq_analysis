#GLAM HACK 2014 project to retrieve and display acquisitions of the British Museum 
#by year and origin

from SPARQLWrapper import SPARQLWrapper, JSON
import pymongo,bson,sys
from pymongo import Connection

debug = True
sparql = SPARQLWrapper("http://collection.britishmuseum.org/sparql")

#This is where we attempt to connect to a local MongoDB installation for data storage
try:
	connection = Connection()
	db = connection.britmuseum
	acquisitions = db.acquisitions
except:
	print("Database connection problem.")
	sys.exit()

for year in range(1824,1999):
	query = """PREFIX ecrm: <http://erlangen-crm.org/current/>
				SELECT ?localityLabel (COUNT(?item) as ?itemCount)
				WHERE {
					?item ecrm:P30i_custody_transferred_through ?hasCustody .
					  ?hasCustody ecrm:P4_has_time-span ?hasTime .
					  ?hasTime rdfs:label \"""" + str(year) + """\" . 
					?item ecrm:P12i_was_present_at ?placeThing .
					 ?placeThing ecrm:P7_took_place_at ?locality .
					 ?locality skos:prefLabel ?localityLabel .
					 ?locality ecrm:P2_has_type ?localityType .
					 ?localityType skos:prefLabel ?localityTypeLabel .
					 FILTER(?localityTypeLabel = "country or city-state") . 
					} 
					GROUP BY ?localityLabel
					ORDER BY DESC(?itemCount)"""

	if debug:
		print query

	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	
	for result in results["results"]["bindings"]:
		if not 'localityLabel' in result:
			print "Sorry, nothing for " + str(year)
			continue		
		document = {"locality": result["localityLabel"]["value"] ,
					"count": int(result["itemCount"]["value"]),
					"year" : year}
		didItInsert = acquisitions.insert(document)
		if debug: 
			print(result["localityLabel"]["value"] + "\t" + result["itemCount"]["value"])
			print ">>>>>>>>>>>" + str(didItInsert)
	if debug:
		print "For " + str(year) + ", total inventory is " + str(acquisitions.count())
		
print "I'm done."
print "Total inventory is " + str(acquisitions.count()) + " acquisitions in the system"