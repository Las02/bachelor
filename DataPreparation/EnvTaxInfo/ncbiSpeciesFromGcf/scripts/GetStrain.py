
import subprocess
import json
import pandas as pd
import sys

def divide_chunks(l, n):
    """Divide list into chunks
       source: https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
    """
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]

def get_key_path_value(key_path, obj, default=None):
    """Safely extract several keys for dict
    source: https://stackoverflow.com/questions/45016931/how-to-use-get-multiple-times-pythonically
    """
    if not key_path:
        return obj
    try:
        for key in key_path:
            obj = obj[key]
    except (KeyError, IndexError):
        return default
    return obj

if len(sys.argv) != 2:
    sys.exit("Please input api key")

# Read in and format all gcf from database
gcf_file = open("../in/gcf.csv")
all_gcf = gcf_file.readlines()
all_gcf = [gcf.strip() for gcf in all_gcf]
all_gcf = all_gcf

df = pd.DataFrame(index=None)

# Extract information in chunks 
for gcf_chunk in divide_chunks(all_gcf, 500):
    # Running datasets in unix and saving output
    if len(sys.argv) == 2:
        dat = subprocess.run(["datasets","summary","genome","accession","--api-key",sys.argv[1]]+gcf_chunk, stdout=subprocess.PIPE)
    else: 
        print("running without API-key")
        dat = subprocess.run(["datasets","summary","genome","accession"]+gcf_chunk, stdout=subprocess.PIPE)
    dat = dat.stdout
    dat_json = json.loads(dat)

    # Loop though the json output and extract relevant information
    for entry in dat_json["reports"]:
        collect_dict = dict()
        # Tax information
        strain_full = get_key_path_value(("average_nucleotide_identity", "submitted_organism"), entry)
        strain_short = get_key_path_value(("organism", "infraspecific_names", "strain"), entry)
        species = get_key_path_value(("average_nucleotide_identity", "submitted_species"), entry)
        gc = get_key_path_value(("accession",), entry)
        acc = get_key_path_value(("organism", "organism_name"), entry)
        orgn_name = get_key_path_value(("organism", "tax_id"), entry)

        # Sequence information
        gc_percent = get_key_path_value(("assembly_stats", "gc_percent"), entry)
        components = get_key_path_value(("assembly_stats", "number_of_component_sequences"), entry)
        chromosomes = get_key_path_value(("assembly_stats", "total_number_of_chromosomes"), entry)
        total_seq_length = get_key_path_value(("assembly_stats", "total_sequence_length"), entry)

        # Gene information
        noncoding = get_key_path_value(("annotation_info", "stats", "gene_counts", "non_coding"), entry)
        proteinCoding = get_key_path_value(("annotation_info", "stats", "gene_counts", "protein_coding"), entry)
        psuedoGene = get_key_path_value(("annotation_info", "stats", "gene_counts", "pseudogene"), entry) 
        total = get_key_path_value(("annotation_info", "stats", "gene_counts", "total"), entry)

        
        # Save the found data
        # Tax
        collect_dict["strain_full"] = strain_full
        collect_dict["strain_short"] = strain_short
        collect_dict["species"] = species
        collect_dict["gc"] = gc
        collect_dict["accession"] = acc
        # seq info
        collect_dict["gc_percent"] = gc_percent 
        collect_dict["genome_components"] = components
        collect_dict["chromosomes"] = chromosomes
        collect_dict["total_seq_length"] = total_seq_length
        # Gene
        collect_dict["genes_nc"] = noncoding
        collect_dict["genes_coding"] = proteinCoding
        collect_dict["pseudogenes"] = psuedoGene
        collect_dict["total_genes"] = total
        
        # Append it to the main df
        df = pd.concat([df, pd.DataFrame.from_records([collect_dict])])

df.to_csv("../out/gcf2species.csv")
