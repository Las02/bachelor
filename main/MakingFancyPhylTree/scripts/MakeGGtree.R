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

# VERY IMPORTANT!
treedat <- filter(treedat, !is.na(parent), !is.na(node))
summary(treedat)

# convert to treedata format
tr <- as.treedata(treedat)
as_tibble(tr)

ggtree(tr,layout="circular") +
  geom_range(range=tr$mean_n16)


ggtree(tr,layout="circular") +
  geom_tippoint(aes(color=mean_n16),shape=15, size=2, alpha=.75)

  
df <- data.frame(n16=(as.integer(treedat$mean_n16)))

rownames(df) <- treedat$node

# for genus tree
df <- na.omit(df)
p <- ggtree(tr, layout="circular")
p2 <- gheatmap(p,data = df,offset=.01, width=.2) +
  scale_fill_viridis_b(option="D",breaks=c(5,10,15,20,30),values = c(0, 0.1, 1))




# Make order mean and div. Use it for a heat map
dat_by_order <- filter(treedat, !is.na(GENUS))  %>% 
  group_by(parent) %>% 
  summarise(n16=mean(mean_n16),div=mean(mean_div))

all_genus <- filter(treedat, !is.na(GENUS)) %>% select(parent, node)

order_info <- full_join(dat_by_order,all_genus,by="parent", multiple ="all")

df2 <- data.frame(n16=(order_info$n16))
rownames(df2) <- order_info$node

library(ggnewscale)


p3 <- p2 + new_scale_fill()


gheatmap(p3,data = df2,offset=.01, width=.15)+
  scale_fill_viridis_b(option="A",breaks=c(1,2,3,4,5,6,7,8,9),values = c(0, 0.1, 1))


## JUST ORDER
dat_by_order



treedat$GENUS
  #scale_fill_viridis_d(option="D", name="Number of 16s genes",guide = guide_legend(reverse = TRUE))

as_tibble(tr)

dat_by_order <- rename(dat_by_order, ORDER = parent)
no_genus <- filter(treedat, !is.na(ORDER) | !is.na(PHYLUM))
to_plot <- left_join(no_genus, dat_by_order, by="ORDER") %>% select(parent, node, PHYLUM, ORDER, n16)
to_plot <- filter(to_plot, !is.na(n16) | !is.na(PHYLUM))

tr_plot <- as.treedata(to_plot)
pa1 <- ggtree(tr_plot, layout="circular")

df3 <- data.frame(n16=(dat_by_order$n16))
rownames(df3) <- dat_by_order$ORDER

pa2 <- gheatmap(pa1,data = df3,offset=.01, width=.2) +
  scale_fill_viridis_b(option="D",breaks=seq(1,10,1),values=c(0,0.5))

pa3 <- pa2 + new_scale_fill()

df4 <- data.frame(var=(dat_by_order$div))
rownames(df4) <- dat_by_order$ORDER

gheatmap(pa3,data = df4,offset=.01, width=.15)





#ggtree(tr) +
#  geom_label(aes(x=branch, label=label), fill='lightgreen') +
# 