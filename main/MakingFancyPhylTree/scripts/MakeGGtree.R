library(ggtree)
library(tidyverse)
library(ape)
library(tidytree)

# Read in the data from ribdif
# TODO should be changed to reading it from db?
ribdif_dat <- read.csv("../../makingNewInfo/gcf_n16s_genus.csv")
# find mean of number of 16s and total dif
ribdif_genus_info= group_by(ribdif_dat, genus) %>% 
  summarise(mean_n16 = mean(number_16s), mean_div = mean(total_div), nspecies = mean(n_species))
ribdif_genus_info <- rename(ribdif_genus_info, GENUS = genus)

# Read in formmated tree data about the phylogenetic relationship
tree <- read.csv("../data/phyloinfo.csv")
# Replace all eppmpty strings with NA
tree[tree == ""] <- NA

#Join ribdif dat with tree taxonomy data
treedat <- left_join(tree, ribdif_genus_info, "GENUS" )
# Drop all that is genus and does not have mean_n16
treedat <- filter(treedat, !is.na(mean_n16) | is.na(GENUS) )

treedat

treedat2 <- filter(treedat, nspecies > 2 | is.na(GENUS))

# convert to treedata format
tr <- as.treedata(treedat2)
as_tibble(tr)

ggtree(tr) +
  geom_label(aes(x=branch, label=label), fill='lightgreen') +
  geom_tippoint(aes(color=mean_n16), size=10, alpha=.75) 

as_tibble(tr)



#ggtree(tr) +
#  geom_label(aes(x=branch, label=label), fill='lightgreen') +
# 








