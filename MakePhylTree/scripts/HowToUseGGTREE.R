library(ggtree)
library(tidyverse)
library(ape)
library(tidytree)
set.seed(1)
tr <- rtree(4)
tr_tib <- as_tibble(tr) # Convert to tibble, for dplyr
as.phylo(tr_tib) # Back to tree for plotting ex.
# Denne er bedre
# as.treedata
ggtree(tr)

# Example tree
d <- tibble(label = paste0('t', 1:4),
            trait = c("a","b","c","d"))
tr_lbl <- full_join(tr_tib,d, by="label")
tr <- as.treedata(tr_lbl)
ggtree(tr) +
  geom_tiplab() +
  geom_label(aes(x=branch, label=trait, col=branch.length))
