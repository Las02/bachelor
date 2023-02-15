
from subprocess import run

# Read in and format all gcf from database
gcf_file = open("../data/gcf.csv")
all_gcf = gcf_file.readlines()
all_gcf = [gcf.strip() for gcf in all_gcf]
all_gcf = all_gcf[0:10]

print(all_gcf)


#run([datasets summary genome accession GCF_000390265.1 GCF_000016785.1])