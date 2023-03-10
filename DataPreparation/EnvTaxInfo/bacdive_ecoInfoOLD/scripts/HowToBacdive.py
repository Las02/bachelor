
import sys
import bacdive
import numpy as np
import pandas as pd
import random
from Bacdivefunctions import *
# Set random seed to date
random.seed(1502)


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
            tmp_dict = get_bacDat(["species","genus","family","order","class","phylum","domain"],strain["Name and taxonomic classification"]["LPSN"], "nominal")
            bacDat.update(tmp_dict)
        except KeyError:
            pass
        
        
        # Morphology
        try:
            data=strain["Morphology"]["cell morphology"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["motility","gram stain"],data, "nominal")
            bacDat.update(tmp_dict)
        
        
        # Temperature
        try:
            data=strain["Culture and growth conditions"]["culture temp"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = GetPH_or_Temp("temperature", data)
            bacDat.update(tmp_dict)
    
        # pH type
        try:
            data=strain["Culture and growth conditions"]["culture pH"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["PH range"],data, "nominal")
            bacDat.update(tmp_dict)


        # Get environmental information
        try:
            data=strain["Isolation, sampling and environmental information"]["taxonmaps"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["Total samples", "soil counts", "aquatic counts","plant counts"],data, "nominal")
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
            tmp_dict = get_bacDat(["NCBI tax ID"],data, "nominal")
            bacDat.update(tmp_dict)

        # Is it aerobe?
        try:
            data=strain["Physiology and metabolism"]["oxygen tolerance"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["oxygen tolerance"],data, "nominal")
            bacDat.update(tmp_dict)
            
        # Strain 
        try:
            data=strain["Name and taxonomic classification"]
        except KeyError:
            data=None
        if data is not None:
            tmp_dict = get_bacDat(["strain designation"],data, "nominal")
            bacDat.update(tmp_dict)
        
        # Antibiotics
        try:
            data=strain["Physiology and metabolism"]["antibiotic resistance"]
        except KeyError:
            data=None
        if data is not None:
            ar_dict = dict()
            #tmp_dict = get_bacDat(["metabolite","is antibiotic","is resistant","is sensitive"],data, "ignore")
            #tmp_dict = get_bacDat(["antibiotic resistance"],data, "ignore")
            # Parse antibiotic information
            has_AR = False
            
            if type(data) is not list:
                metabolite = data
                name = metabolite.get("metabolite")
                ar_or_not = metabolite.get("is antibiotic")
                resistent = metabolite.get("is resistant") 
                sens = metabolite.get("is sensitive")
                
                is_resistent = ar_or_not != "no" and resistent == "yes" and sens != "yes"
                if is_resistent:
                    ar_dict[name] = "R"
                    has_AR = True
                is_sensitive = ar_or_not != "no" and resistent != "yes" and sens == "yes"
                if is_sensitive:
                    ar_dict[name] = "S"
            else:
                for metabolite in data:
                    name = metabolite.get("metabolite")
                    ar_or_not = metabolite.get("is antibiotic")
                    resistent = metabolite.get("is resistant") 
                    sens = metabolite.get("is sensitive")
                    is_resistent = ar_or_not != "no" and resistent == "yes" and sens != "yes"
                    if is_resistent:
                        ar_dict[name] = "R"
                        has_AR = True
                    is_sensitive = ar_or_not != "no" and resistent != "yes" and sens == "yes"
                    if is_sensitive:
                        ar_dict[name] = "S"
            
            # Save all antibiotics as seperate columns
            tmp_dict = dict()
            if has_AR:
                tmp_dict["antibiotics"] = "R"
            tmp_dict.update(ar_dict)
            #print(tmp_dict)
            bacDat.update(tmp_dict)
                    
            #print(tmp_dict)
            #print("*"*15,"\n",bacDat)
            
            

        df = pd.concat([df, pd.DataFrame.from_records([bacDat])])
        #df = df.append(bacDat,ignore_index=True)
    return df
        

# Read in the genus list
with open("../data/all_genus_found.txt") as genus_file:
    all_genus = genus_file.readlines()
    # Remove \n
    all_genus=[genus.strip() for genus in all_genus]

# Work with a subset for testing
all_genus = all_genus
#print(all_genus)


df = pd.DataFrame()

# Check if password for bacdive is given as argument
# To prevent password from being on git
if len(sys.argv) != 2:
    sys.exit("Please input bacdive code as input")
    
# Connect to the client
password = sys.argv[1]
client = bacdive.BacdiveClient("lasse101010@gmail.com", password)

all_genus = all_genus
# Run the method in chunks

out_file = "BacdiveOut.csv"
chunk_size = 100
i = 0
for all_genus_subset in divide_chunks(all_genus, chunk_size):
    i += 1
    # ignore selected chunks, if some failed
    #if i in list(range(1,15)):
    #    continue
    
    #genus = "Lysobacter"
    for pos, genus in enumerate(all_genus_subset):
        print("Finished:",pos,"of", len(all_genus_subset),"chunk:",i,"totalsize:", len(all_genus),"at genus:",genus)
        df = retrive_tax_info(genus, df)
    # write to .csv file. Only add header to first line
    if i == 1:
        df.to_csv(f"../data/{out_file}", index = False)
    else:
        df.to_csv(f"../data/{out_file}", mode="a", index = False, header=False)
    print("*"*15)
    print("Finished chunk:", i, "of:", len(all_genus)/chunk_size, "chunksize:", chunk_size)
    print("*"*15)
#print(df)
#df.to_csv("delme.csv")


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
