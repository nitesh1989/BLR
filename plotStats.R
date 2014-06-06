divisions = c(2, 4, 8, 12, 16, 20, 24)
time_taken = c(125.673305035, 204.298361063, 362.651827812, 518.877280951, 659.774741888, 783.794388056, 923.709709883)

pdf(file = "BenLangmeadResearch/CE_FMIndex/figs/timeVsdivisions.pdf")

yticks =  c(125, 204, 362, 518, 659, 783, 923)
xticks = c(2, 4, 8, 12, 16, 20, 24)
plot(divisions,time_taken,pch=".",cex = 10,col = "red",yaxt="n",xaxt="n",main = "Number of divisions of Bowtie Index vs Time taken to Align",ylab="Time Taken in seconds",xlab="Number of Divisions of Index")
axis(2,at=yticks,labels=yticks)
axis(1,at=xticks,labels=xticks)
lines(formula=time_taken~divisions,col="blue",lwd=2)
#abline(v=divisions)
#abline(h=time_taken)
dev.off()

# ggplot2 implementation to plot the trend

library(ggplot2)
dat = data.frame(divisions,time_taken)
dat

fig = ggplot(dat, aes(x=divisions, y=time_taken)) + geom_point(shape=1) +  geom_smooth(method=lm) + geom_point(size=3, colour="#CC0000") + labs(title = "Number of divisions of Bowtie Index vs Time taken to Align") + ylab("Time Taken in seconds") + xlab("Number of Divisions of Index")

fig

dev.off()

