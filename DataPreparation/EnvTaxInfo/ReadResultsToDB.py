import sqlite3
import pandas as pd
import sys
import subprocess

# If argument set reset the tables and run the scripts in the folder again
if len(sys.argv) > 1 and sys.argv[1] == "--reset":
    # Read the errors to one file, and the output to another
    stderrFile = open("./stderr.txt", "w")
    stdoutFile = open("./stdout.txt", "w")

    # Run bacdiveEnvInfo
    print("Running bacdiveEnvInfo..")
    password = input("Please write bacdive password:")
    output=subprocess.run(["python3","./bacdiveEnvInfo/scripts/RunBacdive.py", password], 
                            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(output.stderr.decode("utf-8"), file=stderrFile)
    print(output.stdout.decode("utf-8"), file=stdoutFile)

    # Run ncbiSpeciesFromGcf
    print("Running ncbiSpeciesFromGcf...")
    print("Reading list of all GCF entries from database")
    output=subprocess.run(["sqlite3 ../../s16.sqlite < ./ncbiSpeciesFromGcf/scripts/getAllGcf.sql"],shell=True, 
                            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(output.stderr.decode("utf-8"), file=stderrFile)
    print(output.stdout.decode("utf-8"), file=stdoutFile)

    print("running GetStrain.py")
    output=subprocess.run(["python3","./ncbiSpeciesFromGcf/scripts/GetStrain.py"], 
                            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print(output.stderr.decode("utf-8"), file=stderrFile)
    print(output.stdout.decode("utf-8"), file=stdoutFile)

    # Run ncbiTaxInfo
    print("Running ncbiTaxInfo..")
    output=subprocess.run(["python3","./ncnbiTaxInfo/scripts/getTaxInfo.py"], 
                            stdout = subprocess.PIPE, stderr = subprocess.PIPE)
    print("Done Running the programs, reading data into the database...")
    print(output.stderr.decode("utf-8"), file=stderrFile)
    print(output.stdout.decode("utf-8"), file=stdoutFile)

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