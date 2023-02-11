### Purpose
This directory makes a phylogenetic tree \
Since the data taxonomy data above "genus" is allready there
it is downloaded from NCBI's taxonomy api. This is done with : "getTaxInfo.py" \
Thereafter the data is formatted to indicate the relationship between the taxonomy. This is done with "FormatTreeDat.py" \
Lastly the data is visualized using the ggtree package with "MakeGGtree.R". Here the data is merged with data from the database indicating variance and 16s gene numbers.

\
"getTaxInfo.py" -> "FormatTreeDat.py" -> "MakeGGtree.R"



### Data
The data was downloaded from NCBI's API:
11-02-2023

#### Errors
It had the following errors:
---
failed on Cyclonatronum error: 'edges'
failed on Cyclonatronum error: 'edges'
failed on Cyclonatronum error: 'edges'
---

### Extra
The the book about the ggpackage can be found here: https://guangchuangyu.github.io/ggtree-book/chapter-ggtree.html#methods-and-materials-1

### TODO
Write the tax data to the database

