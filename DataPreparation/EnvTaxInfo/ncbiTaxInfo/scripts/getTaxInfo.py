
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
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

def TaxIdToScientificName(taxid: str, tax_to_get: str) -> str:
    """
    Using NCBI's API convert a taxid to a scientific name
    """
    url = "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/taxonomy/taxon/"
    data = requests.get(url+taxid).json()
    #print(tax_to_get, data)
    try: 
        rank = data["taxonomy_nodes"][0]["taxonomy"]["rank"]
    except KeyError:
        print("no rank for", data)
    if rank == tax_to_get:
        return data["taxonomy_nodes"][0]["taxonomy"]["organism_name"]
    else:
        return None


# Define the taxonomy for the genus to get
parents_tax = ["PHYLUM","ORDER"]
df = pd.DataFrame(columns=parents_tax.append("GENUS"))

all_genus = open("../../../makeDbFromRibDif/getListOfAllGenera/out/all_genus_names.dat")
# Get the sci name for all chosen parents tax in parents_tax
# Read them to a pd dataframe called df
for i, genus in enumerate(all_genus):
    genus = genus.strip()
    parents_gotten = dict()
    parents_gotten["GENUS"] = genus
    for tax_to_get in parents_tax:
        try:
            taxid = getParentTaxID(genus, tax_to_get)
            sci_name = TaxIdToScientificName(taxid, tax_to_get)
            parents_gotten[tax_to_get] = sci_name
        except KeyError as e:
            print("failed on", genus,"error:", e)
            
    print("finised genus:",genus,"nr:",i)
    df = df.append(parents_gotten, ignore_index=True)

df.to_csv("../out/taxInfoFull.csv", index=False)