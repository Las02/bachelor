import subprocess
import sqlite3
import pandas as pd
import numpy as np 

def read_fasta(filename):
    '''
       Reading in several fasta files
       yield each pair of header and protein seperate
    '''
    # Try to open the file, error if file does not exsist
    try: file = open(filename, "r")
    except FileNotFoundError as errormessage:
        sys.exit(f"The file '{filename}' could not be found, error: {errormessage}")

    # Extract the protein, and the headers.
    protein = None
    oldheader = "FIRST HEADER"
    for line in file:
        line = line.strip()
        #if line is header yield protein and header except FIRST HEADER
        if line.startswith(">"):    
            newheader = line[1:]
            if oldheader != "FIRST HEADER":
                yield protein, oldheader
            protein = ""
            oldheader = newheader
        else:
            protein += line
    
    if protein == None:
        #print("dna is none in:", oldheader, filename)
        pass
    # Yield the last header and protein
    yield protein, oldheader
    file.close()

def read_seq_to_db(filepath, conn, table, jointable):
    c = conn.cursor()
    
    ### Read the sequences into the database
    all_GCFid = list()
    
    for seq, header in read_fasta(filepath):
        # Get the GCFid
        header = header.split(sep = "_")
        GCFid = "_".join(header[0:2])
        # Add GCFid and sequence to the list
        all_GCFid.append((GCFid, seq))


    conn.commit()

    # read it into the database in s16info
    # connect the 16s sequence to a GCF_number in the DB 
    for GCFid, seq in all_GCFid:
        # Inset the sequence into the table:
        c.execute(f"INSERT OR IGNORE INTO {table} (sequence) VALUES (?)",(seq,))
        # Insert the sequence and GCFid relationship
        # into the "joining" table: 
        c.execute(f"""INSERT INTO {jointable} (sequence_id, gcf) VALUES (
                    (SELECT id FROM {table} WHERE sequence = ?),
                    ?)""", (seq, GCFid))
    conn.commit()


def read_species2db_insertmethod(genus_info, conn, genus):
    c = conn.cursor()

    ## Read "genus", "species", "gcf" into the table "species"
    species_subset_genus_info = genus_info[["gcf", "species"]]
    # "genus" has different names in ribdiff info
    # eg Mycoplasma - Mycoplasmopsis. I use the genus name from the start search
    # which is the ncbi tax genome name
    # therefore use genome name not from ribdif

    for gcf, species in zip(species_subset_genus_info["gcf"],species_subset_genus_info["species"]):
        try:
            c.execute("""  INSERT INTO species (gcf, species, genus) VALUES (?, ?, ?)
            """, (gcf, species, genus))
        except sqlite3.IntegrityError:
            print("the following cannot not be added:",gcf, species, genus)
            problem_genus=c.execute("""SELECT * FROM species WHERE gcf=?""", (gcf,))
            print("due to", problem_genus.fetchall())
    conn.commit()

     
def read_ani2db(genus_info, conn):
    ## INSERT ANI data into ribdif_info table for genus    
    ani_subset_genus_info = genus_info[["gcf","number_16s","mean",
                             "sd","min","max","total_div"]]
    # TODO When number_16s == 1, we do not have a mean ect. Set them to Na
    # Insert the data into ribdif_info table
    ani_subset_genus_info.to_sql("ribdif_info", conn, 
                    if_exists="append", index=False)
    conn.commit()
 
conn = sqlite3.connect("/mnt/raid2/s203512/bachelor/s16.db")
c = conn.cursor()

inpath = "../in/"
infile = open(inpath + "allGenusSmall.txt")

bacteria_not_ribdifed = open("./bacteria_not_ribdifed.txt","w")

for genus in infile:
    genus = genus.strip()
    genus = "-".join(genus.split())
    
    ### Read the data into the database
    # read summary.tsv file from ribdiff into pandas df
    path = "../all_genus_ribdif-ed/"
    
    try:
        genus_info = pd.read_csv(path + f"{genus}/{genus}-summary.tsv", sep="\t", index_col=False)
    except FileNotFoundError:
        print(genus, file = bacteria_not_ribdifed)
        continue


    # rename the columns to match the names in the db
    genus_info = genus_info.rename(columns={
        "GCF" :"gcf",
        "Genus":"genus_ribdiff",
        "Species":"species",
        "#16S":"number_16s",
        "Mean":"mean",  
        "SD"  :"sd",
        "Min" :"min",
        "Max" :"max",
        "TotalDiv":"total_div",
        })
        
    # Read "genus", "species", "gcf" into the table "species"
    read_species2db_insertmethod(genus_info, conn, genus)

    # insert ANI data into ribdif_info table for genus    
    read_ani2db(genus_info, conn)
   
    # Read the full 16s genes in the db
    filepath = path + f"{genus}/full/{genus}.16S"
    table = "s16full_sequence"
    jointable = "species2s16full_sequence"
    read_seq_to_db(filepath, conn, table, jointable)
    
    # Read in the v1v9 amplicons in the db
    filepath = path + f"{genus}/amplicons/{genus}-v1v9.amplicons"
    table = "v1v9sequence"
    jointable = "species2V1V9sequence"
    read_seq_to_db(filepath, conn, table, jointable)
    
    # Read in the v3v4 amplicons in the db
    filepath = path + f"{genus}/amplicons/{genus}-v3v4.amplicons"
    table = "v3v4sequence"
    jointable = "species2V3V4sequence"
    read_seq_to_db(filepath, conn, table, jointable)









