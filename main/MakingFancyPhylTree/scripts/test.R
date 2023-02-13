library(tidyverse)


# Read in the data from ribdif
# TODO should be changed to reading it from db?
ribdif_dat <- read.csv("../../makingNewInfo/gcf_n16s_genus.csv")
# find mean of number of 16s and total dif
ribdif_genus_info= group_by(ribdif_dat, genus) %>% 
  summarise(mean_n16 = mean(number_16s), mean_div = mean(total_div), nspecies = mean(n_species))
ribdif_genus_info <- rename(ribdif_genus_info, GENUS = genus)

ribdif_genus_info

common_dat <- read.csv("../data/hpc_tax_info_full.csv")
common_dat


joined <- left_join(ribdif_genus_info, common_dat, by="GENUS")

joined <- filter(joined, nspecies > 50)

write_csv(joined, "../data/mini.csv")

nrow(joined)
