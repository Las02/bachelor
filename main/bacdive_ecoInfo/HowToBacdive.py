
import sys
import bacdive
import numpy as np
import pandas as pd



class nandict():
    """Quick class to return nan instead of Keyerror when trying to get a key which is not present
        Used to not crash program when attributes are not present but instead add nans
    """
    def __init__(self, dict):
        self.dict = dict
    def __getitem__(self, index):
        try: 
            return self.dict[index]
        except KeyError:
            return np.nan


def get_bacDat(to_get: list, strain_dat:dict, bacDat:dict, dat_type) -> None:
    import random
    import statistics
    
    # If strain_dat is not a list then there is only one ref
    # add it to the bacDat dict
    if type(strain_dat) is not list:
        for get in to_get:
            try:
                bacDat[get] = strain_dat[get]
            except KeyError:
                pass
        return
    
    tmp_dict = dict()
    # Go through each entry
    for entry in strain_dat: 
        # Get the requested info from to_get
        for get in to_get:
            try:
                if entry[get] not in tmp_dict:
                    tmp_dict[get] = [entry[get]]
                else:
                    tmp_dict[get].append(entry[get])
            except KeyError:
                pass
    print(tmp_dict)
    

    


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
    strain = nandict(strain)
    
    bacDat = dict()
    
    # Morphology
    #get_bacDat(["motility"],strain["Morphology"]["cell morphology"], bacDat,"factor")
    get_bacDat(["temperature"],strain["Culture and growth conditions"]["culture temp"], bacDat, "continuous")
    """
    
    print(morph)
    
    
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
        
    
    AR = strain["antibiotic resistance"]
    print(AR)
    
    GC = strain["GC-content"]
    print(GC)
    """