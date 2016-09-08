import pywikibot
from pywikibot import pagegenerators as pg

"""
This code will use pywikibot to generate the result from WikidataSPARQL Query 
and print it to the user's console.
"""

with open('your_query.rq', 'r') as query_file: #replace your_query.rq with your own Wikidata SPARQL Query
  QUERY = query_file.read().replace('\n', ' ')

wikidata_site = pywikibot.Site("wikidata", "wikidata")
generator = pg.WikidataSPARQLPageGenerator(QUERY, site=wikidata_site)

items = list(generator)

for x in items:
	print(x.id)
