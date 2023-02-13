
import sys
import bacdive
import numpy as np
import pandas as pd
import random
from Bacdivefunctions import *

def retrive_tax_info(genus, df):
    # Get various information
    number_found = client.search(taxonomy=genus)
    
    if number_found == 0:
        return df
    
    for strain in client.retrieve():
        #print(strain)
        #strain = nandict(strain)
        
        bacDat = dict()
        bacDat["genus"] = genus
        
        # Taxonomy
        try:
            tmp_dict = get_bacDat(["species"],strain["Name and taxonomic classification"]["LPSN"], "continuous")
            bacDat.update(tmp_dict)
        except KeyError:
            pass
        
        
        # Morphology
        try:
            data=strain["Morphology"]["cell morphology"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["motility","gram stain"],data, "continuous")
            bacDat.update(tmp_dict)
            
        # Temperature
        try:
            data=strain["Culture and growth conditions"]["culture temp"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = GetPH_or_Temp("temperature", data, "continuous")
            bacDat.update(tmp_dict)


        #df = pd.concat([df, pd.DataFrame.from_records([bacDat])])
        df = df.append(bacDat,ignore_index=True)
    return df
        
random.seed(13022023)

# Read in the genus list
with open("../data/all_genus_found.txt") as genus_file:
    all_genus = genus_file.readlines()
    # Remove \n
    all_genus=[genus.strip() for genus in all_genus]

# Work with a subset for testing
all_genus = all_genus[0:500]
print(all_genus)


df = pd.DataFrame()

# Check if password for bacdive is given as argument
# To prevent password from being on git
if len(sys.argv) != 2:
    sys.exit("Please input bacdive code as input")
    
# Connect to the client
password = sys.argv[1]
client = bacdive.BacdiveClient("lasse101010@gmail.com", password)


#genus = "Lysobacter"
for genus in all_genus:
    df = retrive_tax_info(genus, df)

df.to_csv("../data/EnvInfooutput.csv")




"""
    # Temperature
    try:
        tmp_dict = GetPH_or_Temp("temperature", strain["Culture and growth conditions"]["culture temp"], "continuous")
        bacDat.update(tmp_dict)
    except KeyError:
        pass
    
    df = df.append(bacDat,ignore_index=True)
    
    print(df)
"""
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