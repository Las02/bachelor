import pandas as pd
import numpy as np

order = "a"
fam = "b"
genus ="c"

# TODO add extra labels med tax info, så jeg kan vælge kun at vise nogen
df = pd.DataFrame(columns=["parent","node","mean"])

# Adding the order
add_dict = dict()
add_dict["parent"] = "bacteria"
add_dict["node"] = order
df = df.append(add_dict,ignore_index = True)

# Adding the order
add_dict = dict()
add_dict["parent"] = "bacteria"
add_dict["node"] = "order2"
df = df.append(add_dict,ignore_index = True)

# Adding the family
add_dict = dict()
add_dict["parent"] = order
add_dict["node"] = fam
df = df.append(add_dict,ignore_index = True)

# Adding the family
add_dict = dict()
add_dict["parent"] = order
add_dict["node"] = "fam2"
df = df.append(add_dict,ignore_index = True)

# Adding the genus
add_dict = dict()
add_dict["parent"] = fam
add_dict["node"] = "gen1"
add_dict["mean"] = 1
df = df.append(add_dict,ignore_index = True)

# Adding the genus
add_dict = dict()
add_dict["parent"] = fam
add_dict["node"] = "gen2"
add_dict["mean"] = 10
df = df.append(add_dict,ignore_index = True)

df.to_csv("phyloinfo.csv", index=False)
