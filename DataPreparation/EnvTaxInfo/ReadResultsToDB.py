import sqlite3
import pandas as pd
import sys
import subprocess

# If argument set reset the tables and run the scripts in the folder again
if len(sys.argv) > 1 and sys.argv[1] == "--reset":
    # Run bacdiveEnvInfo
    print("Running bacdiveEnvInfo..")
    password = input("Please write bacdive password:")
    subprocess.run(["python3","./bacdiveEnvInfo/scripts/RunBacdive.py", password])

    # Run ncbiSpeciesFromGcf
    print("Running ncbiSpeciesFromGcf...")
    print("Reading list of all GCF entries from database")
    subprocess.run(["sqlite3 ../../s16.sqlite < ./ncbiSpeciesFromGcf/scripts/getAllGcf.sql"],shell=True)
    print("running GetStrain.py")
    subprocess.run(["python3","./ncbiSpeciesFromGcf/scripts/GetStrain.py"])

    # Run ncbiTaxInfo
    print("Running ncbiTaxInfo..")
    subprocess.run(["python3","./ncnbiTaxInfo/scripts/getTaxInfo.py"])
    print("Done Running the programs, reading data into the database...")

# Connect to the DB
conn = conn = sqlite3.connect("../../s16.sqlite")
c = conn.cursor()

# Read in BacdiveOut.csv
gcf2species = pd.read_csv("./ncbiSpeciesFromGcf/out/gcf2species.csv")
gcf2species.to_sql("gcf2species.csv", conn, if_exists="replace", index=False)

# Read in taxInfoFull.txt
taxInfoFull = pd.read_csv("./ncbiTaxInfo/out/taxInfoFull.csv")
taxInfoFull.to_sql("taxInfoFull", conn, if_exists="replace", index=False)

# Read in gcf2species.csv
gcf2species = pd.read_csv("./ncbiSpeciesFromGcf/out/gcf2species.csv")
gcf2species.to_sql("gcf2species", conn, if_exists="replace", index=False)