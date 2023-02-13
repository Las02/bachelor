
import sys
import bacdive
import numpy as np
import pandas as pd

class nandict():
    """Quick class to return nan instead of Keyerror when trying to get a key which is not present
        Used not crash program when attributes are not present but instead add nans
    """
    def __init__(self, dict):
        self.dict = dict
    def __getitem__(self, index):
        try: 
            return self.dict[index]
        except KeyError:
            return np.nan

# Check if password for bacdive is given as argument
# To prevent password from being on git
if len(sys.argv) != 2:
    sys.exit("Please input bacdive code as input")
    
# Connect to the client
password = sys.argv[1]
client = bacdive.BacdiveClient("lasse101010@gmail.com", password)

# Get various information
client.search(taxonomy="Lysobacter tolerans")
for strain in client.retrieve():
    dat = pd.DataFrame.from_dict(strain)
    head(dat)
    """
    with open("json.html","w") as outfile:
        print(strain, file=outfile)
    
    strain = nandict(strain)
    
    # Get the temperature
    temp_info = strain['Culture and growth conditions']["culture temp"]
    for source in temp_info:
        source = nandict(source)
        temp = source["temperature"]
        type = source["range"]
        print(temp,type)
       
    # Get the PH 
    temp_info = strain['Culture and growth conditions']["culture pH"]
    for source in temp_info:
        source = nandict(source)
        pH = source["pH"]
        print(pH)
        
    morph = strain["Morphology"]
    print(morph)
    
    AR = strain["antibiotic resistance"]
    print(AR)
    
    GC = strain["GC-content"]
    print(GC)
    """