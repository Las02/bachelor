import pandas as pd
import numpy as np

df_in = pd.read_csv("../data/mini.csv")




parents_tax = ["parent","node","PHYLUM","ORDER","GENUS"]
df_out = pd.DataFrame(columns=parents_tax)


# TODO add extra labels med tax info, 
# TODO så jeg kan vælge kun at vise nogens

# Add the taxonomy infomation into a df describing
# a parent-node relationship, for building the phylgenetic tree in "MakeGGtree.R"
for nrow, dat in df_in.iterrows():
    order = dat["ORDER"]
    phylum = dat["PHYLUM"]
    genus = dat["GENUS"]
    print(genus, order, phylum)
    
     # Adding the phylum
    add_dict = dict()
    add_dict["parent"] = "Bacteria"
    add_dict["node"] = phylum
    add_dict["PHYLUM"] = phylum
    if phylum not in df_out["node"].values:
        df_out = df_out.append(add_dict, ignore_index = True)
    
    # Adding the order
    add_dict = dict()
    add_dict["parent"] = phylum
    add_dict["node"] = order
    add_dict["ORDER"] = order
    if order not in df_out["node"].values:
        df_out = df_out.append(add_dict, ignore_index = True)
    
   
    
    # Adding the genuss
    add_dict = dict()
    add_dict["parent"] = order
    add_dict["node"] = genus
    add_dict["GENUS"] = genus
    if genus not in df_out["node"].values:
        df_out = df_out.append(add_dict, ignore_index = True)



df_out.to_csv("../data/phyloinfo.csv", index=False)



