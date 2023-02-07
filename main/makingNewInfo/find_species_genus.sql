
--write to csv
.headers on
.mode csv
.output gcf_n16s_genus.csv

--Create a table with the amount of species
--In each genus
CREATE TEMPORARY TABLE genus_count AS 
select genus, count(genus) AS n_species
from species 
group by genus;

--Add n-species pr genus, to each gcf and their number
-- of 16s genes
SELECT total_div, gcf, number_16s ,genus, n_species
FROM ribdif_info 
LEFT JOIN species USING(gcf) 
LEFT JOIN genus_count USING(genus)
