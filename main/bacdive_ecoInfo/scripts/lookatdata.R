
library("tidyverse")

# Read in the output format
D <- read.csv("../data/EnvInfooutput.csv")

D <- replace(D, D == "", NA)
D <- filter(D, !is.na(optimum))
D_small <- mutate(D, temp_opt=as.integer(range)) %>% 
  select(!c(X,optimum,range))

ggplot(D_small) +
  geom_histogram(aes(x=temp_opt))

# some extramophiles
filter(D_small, temp_opt > 60)


# Read in the data from ribdif
ribdif_dat <- read.csv("../../makingNewInfo/gcf_n16s_genus.csv")
# find mean of number of 16s and total dif
# TODO maybe not mean but for each but needs more work
ribdif_genus_info= group_by(ribdif_dat, genus) %>% 
  summarise(mean_n16 = mean(number_16s), mean_div = mean(total_div), nspecies = mean(n_species))

ribdif_genus_info <- rename(ribdif_genus_info)

# Join the two datasets
D_joined <- left_join(D_small, ribdif_genus_info, by="genus")
D_joined <- filter(D_joined, mean_n16 > 0)

D_joined <- mutate(D_joined, AR = factor(ifelse(is.na(is.resistant), "no","yes")))
ggplot(D_joined) +
  geom_boxplot(aes(x=AR, y=mean_div)) 

ggplot(D_joined) +
  geom_boxplot(aes(x=AR, y=mean_n16))

# could be something
ggplot(D_joined) +
  geom_boxplot(aes(y=oxygen.tolerance, x=mean_n16))
# Sig
fit <- lm(mean_div ~ AR, data=D_joined)
anova(fit)

# Not sig
fit <- lm(mean_n16 ~ AR, data=D_joined)
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
  geom_point(aes(x=(temp_opt),y=(mean_div), col = mean_n16)) +
  geom_smooth(aes(x=temp_opt, y=mean_div))


D_motil <- mutate(D_joined, motility = factor(motility)) %>% 
  filter(motility %in% c("no","yes"))


# Motility seems to have no effect'
ggplot(D_motil) +
  geom_boxplot(aes(x=motility, y=log(mean_n16)))

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
  geom_boxplot(aes(x=gram, y=log(mean_n16)))
fit <- lm(log(mean_n16) ~ gram, data=D_gram)
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
  geom_point(aes(x=log(nspecies), y=log(mean_div)))




