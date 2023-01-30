
import requests

# Extract all the taxid for all bacterial genuses
url = "https://api.ncbi.nlm.nih.gov/datasets/v2alpha/taxonomy/taxon/2/filtered_subtree?rank_limits=GENUS"
data = requests.get(url).json()
all_genus = data["edges"]["2"]["visible_children"]
outfile = open("../data/all_genus_taxid.dat", "w")
for genus_taxid in all_genus:
    print(genus_taxid, file = outfile)
    
    
