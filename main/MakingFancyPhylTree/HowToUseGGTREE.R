library(ggtree)
library(tidyverse)
library(ape)
tr <- rtree(50)
tr_tib <- as_tibble(tr) # Convert to tibble, for dplyr
as.phylo(tr_tib) # Back to tree for plotting ex.
ggtree(tr)
