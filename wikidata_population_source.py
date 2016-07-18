import pywikibot
from pywikibot.data import api
import pprint
from pywikibot import pagegenerators
import csv

"""
This code will use pywikibot to insert the population data for all Kabupaten and Kota in Indonesia,
which stated in Buku Induk Kode dan Data Wilayah Administrasi Pemerintahan Per Provinsi, 
Kabupaten/Kota dan Kecamatan Seluruh Indonesia issued by Kemendagri.
"""


p_stated_in = "P248" #ID for properties 'stated in'
p_population = "P1082" #ID for properties 'population'
p_ref_url = "P854" #ID for properties 'URL reference'

population_source_qid = "Q24249960" #ID for the source of the data from Kemendagri


site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()

def get_items(site, item_title):
    """
    Requires a site and search term (item_title) and returns the results.
    """
    params = {"action": "wbsearchentities",
              "format": "json",
              "language": "id",
              "type": "item",
              "search": item_title}
    request = api.Request(site=site, **params)
    return request.submit()

def check_claim_and_uncert(item, property, value, q_id):
    """
    Requires a property, value, and returns boolean.
    Checking whether there is already a same claim with same source
    Returns true if the claim with the same source already exists.
    """
    item_dict = item.get()
    try:
        claims = item_dict["claims"][property]
        
    except:
        return None
    
    try:
        claim_exists = False
        for claim in claims:
            wb_quant = claim.getTarget()
            if wb_quant.amount == value :
                source = check_source_set(claim, key, population_source_qid)
                if source:
                    claim_exists = True

            if claim_exists: 
                return claim
    except:
        return None
    
def check_source_set(claim, property, value):
    source_claims = claim.getSources()
    if len(source_claims) == 0:
        return False

    for source in source_claims:
        try:
            stated_in_claim = source[p_stated_in]
        except:
            return False
        for claim in stated_in_claim:
            trgt = claim.target
            if trgt.id == value:
                return True

def set_claim(item, property, value):
    claim = pywikibot.Claim(repo, property)
    wb_quant = pywikibot.WbQuantity(value, )
    claim.setTarget(wb_quant)
    print(item,claim.toJSON())
    item.addClaim(claim, bot=False, summary="Menambahkan data penduduk dengan pywikibot")
    return claim

def create_source_claim(claim, source_data):
    trgt_item = source_data
    trgt_itempage = pywikibot.ItemPage(repo, trgt_item)
    source_claim = pywikibot.Claim(repo, p_stated_in, isReference=True)
    source_claim.setTarget(trgt_itempage)
    claim.addSources([source_claim])
    return True

with open('kabupaten_kota.csv', 'rt') as f:
    reader = csv.reader(f)
    for row in reader:
        key = row[0]
        if key!= "":
            search_results = get_items(site, key)
            if len(search_results["search"]) == 1 and row[9] != "":
                item = pywikibot.ItemPage(repo, search_results["search"][0]["id"])
                population_number = int(row[9].replace(".",'').replace(",", ''))

                claim = check_claim_and_uncert(item, p_population, population_number, population_source_qid)
                if claim:
                    source = check_source_set(claim, key, population_source_qid)
                    if source:
                        print("Population and source already exist")
                    else:
                        create_source_claim(claim, population_source_qid)

                else:
                    claim = set_claim(item, p_population, population_number)
                    create_source_claim(claim, population_source_qid)
            else:
                print("No result or too many found for {}.", key)


        



