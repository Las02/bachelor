
library(tidyverse)

# Define function to calculate mode
mode <- function(factors, if_empty) {
  factors <- factors[factors != ""]
  # If it does not have any factors but only " " set it to specific value
  if (length(factors) == 0) {
    return(factor(if_empty))
  }
  # Else find the mode
  max <- factors %>%
    table() %>%
      which.max() %>%
        as.data.frame() %>%
          rownames() %>%
            factor()
  return(max)
}

#### Reading in the data + cleaning####
setwd("/mnt/raid2/s203512/bachelor/main/bacdive_ecoInfo/scripts")
# Read in environment data from bacdive
EnvD <- read.csv("../data/EnvInfooutput_15_02_2023.csv")

# For antibiotic comuns replace "" with "NR" for each species
# If several are defined, find the mode
# For the other columns if they are nominal find the mode, else the mean
EnvD_by_species <- group_by(EnvD, species)
EnvD_summarised <- EnvD_by_species %>%
  summarise(
    across(antibiotics:spiramycin.II, ~mode(.x, "NR")),
    across(family:growth, ~mode(.x, NA)),
    across(c(genus, oxygen.tolerance, PH.range), ~mode(.x, NA)),
    across(c(GC.content, Total.samples, soil.counts, aquatic.counts, plant.counts, optimum),
    ~mean(as.numeric(.x), na.rm = TRUE))
  )

# Read in the data from NCBI about specsies/strains ects
ncbiD <- read.csv("../data/speciesinfo.csv")

# Read in the data from ribdif
ribdifD <- read.csv("../data/ribdif_info.csv")

# Joining the datasets
ncbiD <- rename(ncbiD, gcf = gc)
rib_ncbi_D <- left_join(ribdifD, ncbiD, by="gcf")
rib_ncbi_D <- replace(rib_ncbi_D, rib_ncbi_D == "", NA)

# Get the mean of relevant data and group by species
rib_ncbi_D_by_species <- group_by(rib_ncbi_D, species) %>%
  summarise(
    n16 = mean(number_16s, na.rm = TRUE),
    div = mean(total_div, na.rm = TRUE),
    gc_percent = mean(gc_percent, na.rm = TRUE),
    genome_components = mean(genome_components, na.rm = TRUE),
    chromosomes = mean(chromosomes, na.rm = TRUE),
    total_seq_length = mean(total_seq_length, na.rm = TRUE),
    genes_nc = mean(genes_nc, na.rm = TRUE),
    genes_coding = mean(genes_coding, na.rm = TRUE),
    pseudogenes = mean(pseudogenes, na.rm = TRUE),
    total_genes = mean(total_genes, na.rm = TRUE)
    )

dat <- inner_join(EnvD_summarised, rib_ncbi_D_by_species, by = "species")







#### OLD ####
D <- filter(D, !is.na(optimum))
D_small <- mutate(D, temp_opt=as.integer(range)) %>% 
  select(!c(X,optimum,range))


# find species seen twice
group_by(D, species) %>% 
  summarise(number=n()) %>% 
  filter(number > 1)
  


ggplot(D_small) +
  geom_histogram(aes(x=temp_opt))

# some extramophiles
filter(D_small, temp_opt > 60)


# Read in the data from ribdif
ribdif_dat <- read.csv("../../PrelimitaryAnalysis/gcf_n16s_genus.csv")
# find mean of number of 16s and total dif
# TODO maybe not mean but for each but needs more work
ribdif_genus_info= group_by(ribdif_dat, genus) %>% 
  summarise(mean_n16 = mean(number_16s), mean_div = mean(total_div), nspecies = mean(n_species))

ribdif_genus_info <- rename(ribdif_genus_info)

# Join the two datasets
D_joined <- left_join(D_small, ribdif_genus_info, by="genus")
D_joined <- filter(D_joined, mean_n16 > 0)

D_joined <- mutate(D_joined, AR = factor(ifelse(is.na(is.resistant), "no","yes")))
# Less div -> needs selected AR ribosomes
ggplot(D_joined) +
  geom_boxplot(aes(x=AR, y=log(mean_div+1)))

# Lower 16s ribosome -> often C-selected: do not change much in terms of conditons.. 
# AKA do not need large amount of changebility
ggplot(D_joined) +
  geom_boxplot(aes(x=AR, y=mean_n16))

# could be something
ggplot(D_joined) +
  geom_boxplot(aes(y=oxygen.tolerance, x=mean_n16))
# Sig
fit <- lm(log10(mean_div+1) ~ AR, data=D_joined)
anova(fit)

#sig
fit <- lm(log(mean_n16+1) ~ AR, data=D_joined)
anova(fit)

D_test <- D_joined %>% filter(!is.na(soil.counts), !is.na(aquatic.counts),!is.na(plant.counts)) 

# What is
which_sample <- function(soil,aquatic,plant){
  if (soil > aquatic && soil > plant){
    return("soil")
    }
  else if (aquatic > soil && aquatic > plant){
    return("aquatic")
    }
  else if (plant > aquatic && plant > soil){
    return("plant")}
  else {
    return("none")

    }
  }

# Does work
tst <- mutate(D_test, sample = pmap_chr(list(soil.counts, aquatic.counts,plant.counts),which_sample))

tst <- filter(tst, sample != "none")

ggplot(tst) +
  geom_boxplot(aes(y=log(mean_n16), x=sample))

ggplot(tst) +
  geom_boxplot(aes(y=log(mean_div+1), x=sample))

# Sig !! between types of sample
fit <- lm(mean_div ~ sample, data=tst)
anova(fit)

# BIG sig
fit <- lm(mean_n16 ~ sample, data=tst)
anova(fit)




# It seems to be kinda genus specific. BUT THATS BEcause we took mean n16
ggplot(D_joined) + 
  geom_point(aes(x=temp_opt,y=(mean_n16), col = genus)) +
  theme(legend.position="none") +
  facet_wrap(~genus)

ggplot(D_joined) + 
  geom_point(aes(x=temp_opt,y=(mean_n16), col = genus)) +
  theme(legend.position="none")

ggplot(D_joined) + 
  geom_point(aes(x=(mean_n16),y=(mean_div), col = genus)) +
  theme(legend.position="none")

ggplot(D_joined) + 
  geom_point(aes(x=(temp_opt),y=log(mean_div), col = mean_n16)) 


D_motil <- mutate(D_joined, motility = factor(motility)) %>% 
  filter(motility %in% c("no","yes"))


# Motility seems to have no effect' But with big it might
ggplot(D_motil) +
  geom_boxplot(aes(x=motility, y=(mean_n16)))

# sig
fit <- lm(log(mean_n16) ~ motility, data=D_motil)
anova(fit)
par(mfrow=c(2,2))
plot(fit)

# Gram or not #### 
D_gram <- mutate(D_joined, gram = factor(gram.stain)) %>% 
  filter(gram %in% c("positive", "negative"))
str(D_gram)

# There is sig but it might just be due to taxonomy relationship
# would be good idea to take more tax data into consideration
ggplot(D_gram) +
  geom_boxplot(aes(x=gram, y=(mean_n16)))
fit <- lm(log(mean_n16) ~ gram, data=D_gram)
# it also has
anova(fit)
#par(mfrow=c(2,2))
#plot(fit)


## More VIRKER IKKE alle df == 1
D_gram_mortil <- mutate(D_motil, gram = factor(gram.stain)) %>% 
  filter(gram %in% c("positive", "negative")) %>% 
  filter(!is.na(temp_opt)) %>% 
  mutate(mean_n16 = as.numeric(mean_n16),
         temp_opt = as.numeric(temp_opt))


str(D_gram_mortil)

fit <- lm(log(mean_n16) ~ temp_opt + gram + motility + gram:temp_opt , data=D_gram_mortil)


anova(fit)
fit2 <- step(fit, k=log(nrow(D_gram_mortil)))
library(car)
anova(fit2)
#plot(fit2)

ggplot(D_gram) +
  geom_point(aes(x=temp_opt, y=log(mean_n16),col=gram))


fit <- lm(mean_n16 ~ temp_opt ,data = D_gram_mortil)
Anova(fit)

sml <- mutate(D_gram_mortil, log_std_n16 = (log(mean_n16) - mean(log(mean_n16)))/sd(log(mean_n16)),
              std_temp = (temp_opt - mean(temp_opt))/sd(temp_opt)
              )
ggplot(sml) +
  geom_point(aes(x=std_temp, y=log_std_n16))



### Does nspecies have effect:: NO
ggplot(D_joined) +
  geom_point(aes(x=(nspecies), y=(mean_div)))

ggplot(D_joined) +
  geom_point(aes(x=log(mean_div+1), y=log(mean_n16+1))) +
  geom_smooth(aes(x=log(mean_div+1), y=log(mean_n16+1)),method = lm)


ggplot(D_joined) +
  geom_point(aes(x=(mean_div),y =(mean_n16))) 
