This folder stores the files which makes the database which stores the 16s genes ect.
The structure of the database can be seen in scripts/createDbStructure.sql
The main file is scripts/runRibDifANDmakeDB.py
This files does the following for all genuses in /in/allGenusSmall.txt
  1) Runs ribdiff on the genus
  2) Stores the information from ribdif in the database test.db
  3) TODO removes the files from runnnig ribdiff


TODO: 
#### OVERORDNET.. Alt i db skal der ikke være styr på fra starten -> den er hurtig at lave når dataen er nede
##### Aka tag det ift rækkefølgen hvor det skal bruges ! 
1) Tjek fejl output -> er der et problem
2) Tjek GCF som kommer flere gange -> problem er at de nok får dobbelt så mange copy number
3) Når man holder 16s RIBO unikke, så for man ikke et correct count af dem (!) -> lav en ny en for kun count eller noget
4) Få sat Entire genomes ind også!
5) Følgende filer har ikke nogen dna
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Chlamydia/amplicons/Chlamydia-v1v9.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Chlamydiifrater/amplicons/Chlamydiifrater-v1v9.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Neochlamydia/amplicons/Neochlamydia-v1v9.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Parachlamydia/amplicons/Parachlamydia-v1v9.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Simkania/amplicons/Simkania-v1v9.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Waddlia/amplicons/Waddlia-v1v9.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Anaerohalosphaera/amplicons/Anaerohalosphaera-v3v4.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Limihaloglobus/amplicons/Limihaloglobus-v3v4.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Sedimentisphaera/amplicons/Sedimentisphaera-v3v4.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Aureliella/amplicons/Aureliella-v3v4.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Roseimaritima/amplicons/Roseimaritima-v3v4.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Rubripirellula/amplicons/Rubripirellula-v3v4.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Mogibacterium/amplicons/Mogibacterium-v3v4.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Lachnoanaerobaculum/amplicons/Lachnoanaerobaculum-v1v9.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Thermanaerosceptrum/amplicons/Thermanaerosceptrum-v1v9.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Syntrophothermus/amplicons/Syntrophothermus-v1v9.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Anaerolinea/amplicons/Anaerolinea-v1v9.amplicons
dna is none in: FIRST HEADER ../all_genus_ribdif-ed/Dehalococcoides/amplicons/Dehalococcoides-v3v4.amplicons