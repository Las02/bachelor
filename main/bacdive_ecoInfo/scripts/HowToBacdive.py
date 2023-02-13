
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
            
        # Get environmental information
        try:
            data=strain["Isolation, sampling and environmental information"]["taxonmaps"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["Total samples", "soil counts", "aquatic counts","plant counts"],data, "continuous")
            bacDat.update(tmp_dict)
            
        # Get GC content
        try:
            data=strain["Sequence information"]["GC content"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["GC-content"],data, "continuous")
            bacDat.update(tmp_dict)
            
        # Get NCBI tax ID COULD BE USED FOR MATCHING SPECIES ?
        try:
            data=strain["Sequence information"]["Genome sequences"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["NCBI tax ID"],data, "continuous")
            bacDat.update(tmp_dict)

        # Is it aerobe?
        try:
            data=strain["Physiology and metabolism"]["oxygen tolerance"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["oxygen tolerance"],data, "continuous")
            bacDat.update(tmp_dict)
        
        # Antibiotics
        try:
            data=strain["Physiology and metabolism"]["antibiotic resistance"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["is resistant", "metabolite","is antibiotic"],data, "continuous")
            bacDat.update(tmp_dict)

        df = pd.concat([df, pd.DataFrame.from_records([bacDat])])
        #df = df.append(bacDat,ignore_index=True)
    return df
        
random.seed(13022023)

# Read in the genus list
with open("../data/all_genus_found.txt") as genus_file:
    all_genus = genus_file.readlines()
    # Remove \n
    all_genus=[genus.strip() for genus in all_genus]

# Work with a subset for testing
all_genus = all_genus[0:100]
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
#print(df)



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