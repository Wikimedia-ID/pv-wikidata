import pywikibot
from pywikibot import pagegenerators as pg
from pywikibot.data import api
import csv

"""
This script will read the query and return a list of Wikidata items, on each Wikidata items, it will check
the corresponding English Wikipedia (enwiki) article which has been linked to it, and see if it is a stub,
or a small article, or it has a 'decent' quality (has more than 300 words).
"""


with open('my_query.rq', 'r') as query_file:
	QUERY = query_file.read().replace('\n', '')

wikidata_site = pywikibot.Site("wikidata", "wikidata")
enwiki_site = pywikibot.Site("en", "wikipedia")

generator = pg.WikidataSPARQLPageGenerator(QUERY, site=wikidata_site)

items = list(generator)
for x in items:
	print (x)

with open("my_csv.csv", "wt", newline ="") as text_file:
	writer = csv.writer(text_file)
	
	for x in items:
		try:
			label = x.getSitelink(site=enwiki_site)

		except pywikibot.NoPage:
			print("There is currently no article for " + x.labels['en'])
			writer.writerow([x.labels['en'], "no article"])

		article = pywikibot.Page(enwiki_site, title=label, ns=0)
		
		if "stub}}" in article.text:
			print (label + " is a stub.")
			writer.writerow([label, "stub"])
		
		else:
			if len((article.text).split()) < 300 :
				print(label + "is a small article.")
				writer.writerow([label, "small"])

			else:
				print(label+" is a quite decent article.")
				writer.writerow([label, "decent"])
