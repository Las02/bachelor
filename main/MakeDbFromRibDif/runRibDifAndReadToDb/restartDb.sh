#!/usr/bin/bash
rm /mnt/raid2/s203512/bachelor/s16_2.sqlite
sqlite3 /mnt/raid2/s203512/bachelor/s16_2.sqlite < createDbStructure.sql

