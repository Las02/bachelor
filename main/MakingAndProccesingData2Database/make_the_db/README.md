This folder makes the database which stores the 16s genes ect.
The structure of the database can be seen in createDbStructure.sql
The main file is runRibDifANDmakeDB.py
This files does the following for all genuses in /in/allGenusSmall.txt
  1) Runs ribdiff on the genus
  2) Stores the information from ribdif in the database test.db
  3) TODO removes the files from runnnig ribdiff
