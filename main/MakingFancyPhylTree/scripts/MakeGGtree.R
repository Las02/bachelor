
tree <- read.csv("phyloinfo.csv")
tr <- as.treedata(tree)
ggtree(tr) +
  geom_label(aes(x=branch, label=label), fill='lightgreen') +
  geom_tippoint(aes(color=mean), size=10, alpha=.75) 
as_tibble(tr)
s