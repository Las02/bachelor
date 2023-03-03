#!/usr/bin/bash

### Get data from sql:
#sqlite3 ../../s16.sqlite  <<'END_SQL'
#.mode column
#
#SELECT genus, sequence_id FROM species LEFT JOIN species2V3V4sequence ON species.gcf = species2V3V4sequence.gcf;
#END_SQL 
#> genus_seq.dat


# Format data for cytoscape
awk '{print $1 " pp " $2}' genus_seq.dat > genus_seq_cyto.dat

# Make annotaion data
awk '{printf("%s genus\n" ,$1)}' genus_seq.dat > ann_cytodat
awk '{printf("%s seq\n" ,$2)}' genus_seq.dat >> ann_cyto.dat

# Make smaller dataset with only overlapping
python3 find_joined.py genus_seq.dat genus_seq_cyto.dat > JOINED_genus_seq_cyto.dat

