britmuseum_acq_analysis
=======================

Philadelphia GLAM Hack project to analyze the acquisition dates and provenances of items in the British Museum collection.

Our team:

Alex Brey, Ben Carlson, Natalia Ermolaev, Michael Lesk, Megan Miller, Emily Morton-Owens, Danielle Reay

We were exploring the linked open data made available by the British Museum and became curious about whether we could 
spot any trends in where/when it was acquired, particularly whether the museum was acquiring a lot of materials from its
then-colonies.

Alex has a much more complete write-up, with results and charts, here: http://hart.blogs.brynmawr.edu/2014/02/02/glamhackphilly-empire-and-the-collection-of-the-british-museum/
His post also includes the more complicated SPARQL queries that we tried out.

There are three files here:
* sparqlquery.py is to query the linked open data for items for which a date and place of acquisition are known, and store
them by year and country in a MongoDB collection.
* report_simple.py delivers a csv report for each country, each year, which turns out to have a lot of zeroes in it.
* report_decade.py improves on the simple report by summing it by decade.

You'll need MongoDB running, plus pymongo and sparqlwrapper, to run this. You can easily plug in other SPARQL queries, like the alternate versions on Alex's blog, but you have to be very careful escaping the quotes...
