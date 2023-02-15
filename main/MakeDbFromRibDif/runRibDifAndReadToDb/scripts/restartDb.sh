#!/usr/bin/bash
rm /mnt/raid2/s203512/bachelor/s16.db
sqlite3 /mnt/raid2/s203512/bachelor/s16.db < createDbStructure.sql

