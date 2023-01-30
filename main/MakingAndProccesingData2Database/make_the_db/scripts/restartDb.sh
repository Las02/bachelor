#!/usr/bin/bash
rm test.db
sqlite3 test.db < createDbStructure.sql

