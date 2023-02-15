
--write to csv
.headers on
.mode csv
.output ../data/gcf.csv

SELECT DISTINCT(gcf) FROM species