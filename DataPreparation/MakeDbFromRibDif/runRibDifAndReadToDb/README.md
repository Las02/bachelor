This folder stores the files which makes the database which stores the 16s genes ect.
The structure of the database can be seen in scripts/createDbStructure.sql
The main file is scripts/runRibDifANDmakeDB.py
This files does the following for all genuses in /in/allGenusSmall.txt
  1) Runs ribdiff on the genus
  2) Stores the information from ribdif in the database s16.sqlite


#### TODO: DONE! 
1) Tjek fejl output -> er der et problem 
          * ser ok ud

2) Tjek GCF som kommer flere gange -> problem er at de nok får dobbelt så mange copy number |
          * 229 GCF's was seen more than once, a list of them can be found in /runRibDifAndReadToDb/scripts/list_over_identical_1_pr_line.txt v
          * They are now not added as sequences if seen more than once. They are still added to ani data -> find mean of values::more accurate
3) Når man holder 16s RIBO unikke, så for man ikke et correct count af dem (!) -> lav en ny en for kun count eller noget
          *You can use join table for fixing this
4) Få sat Entire genomes ind også!
          *I'm doing it when it is relevant
5) Følgende filer har ikke nogen dna
          *No Ribosomes are found for them
          *Now they are not addded
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
6) Where does wrong header come from?
     * Denne:
     sqlite> select * from species WHERE GCF NOT LIKE "GCF_%";
     23S_rRNA::GCF|Campylobacter|CP038868.1 Campylobacter coli strain 16SHKX65C chromosome complete
     --> kommer fra Campylobacter-summary.tsv fra ribdif
     --> parsed forkert fra 23S_rRNA::GCF_010232325.1
     * solution -> just drop it since it's only one and it looks meesed up:
     6	0	0	0	0	1484.7212607594	<- div from ribdif
     -> im adding DELETE FROM species WHERE GCF LIKE "23S%"; to readDataToDb AND DELETE FROM ribdif_info WHERE GCF LIKE "23S%";

## Known throuwn errors from running ribdif:
```
Ignored unknown character X (seen 2 times)
---
Error in apply(str_split_fixed(ucFile$V9, "_", 8)[, 1:2], 1, paste, collapse = "_") : 
  dim(X) must have a positive length
---
Error in cut.default(x, breaks = breaks, include.lowest = T) : 
  'breaks' are not unique
Calls: pheatmap ... scale_colours -> matrix -> scale_vec_colours -> cut -> cut.default
Error in cut.default(x, breaks = breaks, include.lowest = T) : 
  'breaks' are not unique
Calls: pheatmap ... scale_colours -> matrix -> scale_vec_colours -> cut -> cut.default
---
rm: cannot remove 'Rplots.pdf': No such file or directory
---
-Error in hclust(dist(binClusterMat), "ward.D2") : 
  must have n >= 2 objects to cluster
Execution halted
---
```