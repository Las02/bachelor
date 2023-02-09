#library(ggplot2)
#library(dplyr)
library(tidyverse)

D = read.table("./gcf_n16s_genus.csv", header = TRUE, sep = ",")

plot(D)
D_small = filter(D, n_species > 10)
#D_small = filter(D_small, row_number() < 50)

ggplot(D_small, aes(x=genus, y=number_16s)) +
    geom_boxplot() +
    coord_flip()

# Hard to estimate dist, since some genus have
# been sequenced alot more than others
hist(D_small$number_16s)

### Husk de er discrete data
# Ways to solve this
# 1) random pick out 5 for each or something
# 2) Use some sort of real life distribution ??

#1) 
## Random pick out 5 for each genus
Dbygenus = filter(D, n_species > 5)
Dbygenus = group_by(Dbygenus, genus)
D_sampled = slice_sample(Dbygenus, n=5, replace=T)
par(mfrow=c(2,2))
hist(D_sampled$number_16s,breaks = 10)
hist(D$number_16s,breaks = 20)
hist(log(D_sampled$number_16s),breaks = 10)
hist(log(D$number_16s),breaks = 10)



# Here it looks a lot better
# Can you log transform discrete?
hist(log(D_sampled$number_16s))
hist(sqrt(D_sampled$number_16s))

ggplot(D_sampled, aes(x=log(number_16s))) +
    geom_histogram(binwidth=0.5)


## Looking at the var as the total_div
D_small = filter(D, n_species > 5) 
summary(D_small)
# all values are very small
ggplot(D_small, aes(x=(total_div))) +
    geom_histogram()

# Log transform
ggplot(D_small, aes(x=log(total_div))) +
    geom_histogram()
# Is removing 0 
# Looks ok but needs more work

# Trying with the same sample tecnique as before
ggplot(D_sampled, aes(x=log(total_div))) +
    geom_histogram(bins=30)
# Looks okish, looks like two different distributions

# Look more into this
ggplot(D_sampled, aes(x=(number_16s), y=(total_div))) +
    geom_point()


# Adding the log transformed for now and
# plotting
D = mutate(D,
    log_n16 = log(number_16s), 
    log_div = log(total_div)
    )
plot(D)


