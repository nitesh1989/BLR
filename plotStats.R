# Nitesh Turaga
# nitesh.turaga@gmail.com

#############################################
# ggplot2 implementation to plot the trend
#############################################
library(ggplot2)


##################################################################
# Time taken vs index divisions
##################################################################
dat = data.frame(divisions,time_taken)
dat = read.table("BenLangmeadResearch/CE_FMIndex/figs/time_stats.txt")
colnames(dat) = c("divisions","time_taken")
fig1 = ggplot(dat, aes(x=divisions, y=time_taken)) + geom_point(shape=1) +  geom_smooth(method=lm) + geom_point(size=3, colour="#CC0000") + labs(title = "Number of divisions of Bowtie Index vs Time taken to Align") + ylab("Time Taken in seconds") + xlab("Number of Divisions of Index")
fig1
##################################################################


##################################################################
# Alignment % vs index divisions
##################################################################
# number of reads aligned vs index divisions
align_dat = read.table("BenLangmeadResearch/CE_FMIndex/figs/align_stat.txt",sep="\t")
V1 = gsub("genome ","",align_dat$V1)
V1 = gsub(" splits","",V1)
align_dat$V1 = as.numeric(V1)

fig_align = ggplot(align_dat, aes(x=V1, y=V2)) + 
      geom_point(shape=1) + 
      geom_point(size=3, colour="#CC0000") + 
      labs(title = "Number of divisions of Bowtie Index vs Reads Aligned") +
      ylab("Reads with atleast 1 alignment") +
      xlab("Number of Divisions of Index") +
      scale_y_continuous(breaks=align_dat$V2)


fig_align
##################################################################



