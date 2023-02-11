
import requests
import pandas as pd

def getParentTaxID(genus: str, tax_to_return: str) -> str:
    """ Extract the tax_id using NCBI's API
        tax_to_return can be: SUPERKINGDOM ┃ KINGDOM ┃ SUBKINGDOM ┃ 
        SUPERPHYLUM ┃ SUBPHYLUM ┃ PHYLUM ┃ CLADE ┃ SUPERCLASS ┃ CLASS ┃ 
        SUBCLASS ┃ INFRACLASS ┃ COHORT ┃ SUBCOHORT ┃ SUPERORDER ┃ ORDER ┃ 
        SUBORDER ┃ INFRAORDER ┃ PARVORDER ┃ SUPERFAMILY ┃ FAMILY ┃ SUBFAMILY 
    """
    
    url = "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/taxonomy/taxon/"
    data = requests.get(url + f"{genus}/filtered_subtree?rank_limits={tax_to_return}").json()
    taxID = data["edges"]["1"]["visible_children"][0]
    return str(taxID)

def TaxIdToScientificName(taxid: str) -> str:
    """
    Using NCBI's API convert a taxid to a scientific name
    """
    url = "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/taxonomy/taxon/"
    data = requests.get(url+taxid).json()
    return data["taxonomy_nodes"][0]["taxonomy"]["organism_name"]

# Define the taxonomy for the genus to get
parents_tax = ["PHYLUM","ORDER"]
df = pd.DataFrame(columns=parents_tax.append("GENUS"))

all_genus = open("../data/all_genus.txt")

# Get the sci name for all chosen parents tax in parents_tax
# Read them to a pd dataframe called df
for genus in all_genus:
    genus = genus.strip()
    parents_gotten = dict()
    parents_gotten["GENUS"] = genus
    for tax_to_get in parents_tax:
        try:
            taxid = getParentTaxID(genus, tax_to_get)
            sci_name = TaxIdToScientificName(taxid)
            parents_gotten[tax_to_get] = sci_name
        except KeyError as e:
            print("failed on", genus,"error:", e)
            

    df = df.append(parents_gotten, ignore_index=True)

df.to_csv("../data/tax_info_full.csv", index=False)