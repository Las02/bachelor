import sys

s16_genus = dict()

file = open("genus_seq.dat")

# Add all genus seen for each 16s sequence
for line in file:
    line = line.split()
    if len(line) != 2:
        continue
   
    genus = line[0]
    s16 = line[1]
    
    if s16 not in s16_genus: 
        s16_genus[s16] = {genus}
    else: 
        s16_genus[s16].add(genus)
            
joined = set()  
            
# Get all for which two different genera share 16s seq
for genus_set in s16_genus.values():
    if len(genus_set) > 1:
        joined.update(genus_set)
  
   
with open("genus_seq_cyto.dat") as cytofile:
    for line in cytofile:     
        linelist = line.split()
        if linelist[0] in joined:
            print(line, end="")
# Print the joined
#for genus in joined:
#    print(genus)