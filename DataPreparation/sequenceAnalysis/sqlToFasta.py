
import sqlite3
import sys
import pandas as pd

def queryToFasta(table_to_get_seq = "s16full_sequence", 
                 join_table = "species2s16full_sequence", 
                 WHERE = "WHERE species.gcf = 'GCF_000020945.1'"):

    """ Based on a query, get fasta formatted files to std.out """
    # Connect to the db
    con = sqlite3.connect("../../s16.sqlite")
    c = con.cursor()
    
    # Get the sequences query
    query = f"""
    select * from species  
    LEFT JOIN {join_table} 
    ON species.gcf = {join_table}.gcf 
    LEFT JOIN gcf2species
    ON gcf2species.gc = species.gcf
    LEFT JOIN {table_to_get_seq} 
    ON {join_table}.sequence_id  = {table_to_get_seq}.id 
    {WHERE}
            """
            
    search = c.execute(query)
    i = 0
    for result in search.fetchall():
        i += 1
        gcf = result[0]
        strain = result[2]
        print(f">seq{i}_{gcf}_{strain}")
        sequence = result[-1]
        print(sequence)

"""
# Read in speciesinfo if not done before
con = sqlite3.connect("../s16.sqlite")
df = pd.read_csv("./speciesinfo.csv")
df.to_sql("ncbi_dat", con)
"""

if __name__ == "__main__":
        # Res to tobramycin
        tobraR = """Aeromonas encheleia         
        Aeromonas sanarellii        
        Agarilytica rhodophyticola  
        Alteromonas pelagimontana   
        Brucella pseudintermedia    
        Catenovulum sediminis       
        Dyella caseinilytica        
        Enterobacter bugandensis    
        Enterobacter huaxiensis     
        Flavobacterium cerinum      
        Indioceanicola profundi     
        Marinobacter nauticus       
        Mycobacterium intracellulare
        Priestia aryabhattai        
        Pseudomonas asiatica        
        Staphylospora marina        
        Streptomyces spongiicola"""
        tobraR = tobraR.split("\n")
        tobraR = [x.strip() for x in tobraR]

        # Query the data
        for entry in tobraR:
                queryToFasta(table_to_get_seq = "s16full_sequence", 
                                join_table = "species2s16full_sequence", 
                                WHERE = f"WHERE gcf2species.species IN ('{entry}')")
