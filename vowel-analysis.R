library(lme4)
library(languageR)
library(plyr)
library(ggplot2)
library(reshape2)
library(scales)
library(arm)

setwd("/Users/oriana/Dropbox/Grad/Evaluation2/data/CSJ")


df = read.csv("basicdata.txt",sep="\t")

summary(df)


inEnvt <- subset(df, HVD.envt == "Y")
inEnvt$dv = 0
inEnvt$dv[inEnvt$devoiced=="Y"]=1
summary(inEnvt)


inEnvt[inEnvt$devoiced == "N",]
bytone1 <- ddply(inEnvt, .(tone,devoiced), summarize, freq=(length(devoiced)) )
bytone <- reshape(bytone1, idvar=c("tone"), timevar="devoiced",direction="wide")

summary(bytone)
head(bytone)
bytone
bytone$ratio = "NA" # HOW TO ADD THIS RATIO COLUMN FOR ALL TABLES? 

for(i in 1:nrow(bytone)){
	bytone$ratio[i] = bytone$freq.N[i]:bytone$freq.N[i]
}
bytone # THIS ONE

bybreak1 <- ddply(inEnvt, .(follBreak,devoiced), summarize, freq=(length(devoiced)) )
bybreak <- reshape(bybreak1, idvar=c("follBreak"), timevar="devoiced",direction="wide")

bybreak # this one too

byPpoa1 <- ddply(inEnvt, .(prevPOA,devoiced), summarize, freq=(length(devoiced)) )
byPpoa <- reshape(byPpoa1, idvar=c("prevPOA"), timevar="devoiced",direction="wide")

byPpoa


byprevSeg1 <- ddply(inEnvt, .(prevSeg,devoiced), summarize, freq=(length(devoiced)) )
byprevSeg <- reshape(byprevSeg1, idvar=c("prevSeg"), timevar="devoiced",direction="wide")

byprevSeg



bySegs1 <- ddply(inEnvt, .(prevSeg,follSeg,devoiced), summarize, freq=(length(devoiced)) )
bySegs <- reshape(bySegs1, idvar=c("prevSeg","follSeg"), timevar="devoiced",direction="wide")

bySegs


mean(df$syllDur, na.rm=TRUE)
df$syllDur <- as.numeric(as.character(df$syllDur))
df$vDur <- as.numeric(as.character(df$vDur))
mean(df$vDur,na.rm=T)

shorties <- df[df$syllDur < 0.5,]

summary(shorties)
summary(df$tone)

ggplot(df,aes(x=HVD.envt,y=log(syllDur),fill=devoiced )) + geom_boxplot() 
#+ geom_jitter(alpha=0.02)


which()
head(inEnvt)

#### What is the effect of follBreak == 3 versus following pause length? 

## Proportion of vowels which are devoiced, by following break type. 
ddply(inEnvt,.(follBreak.type),summarise, prop.devoiced= length(devoiced[devoiced=="Y"])/length(devoiced),mean.follPz=mean(follPz,na.rm=T))

## Boxplot for log duration of following pause, by devoiced Y/N
ggplot(inEnvt,aes(y=log(follPz),x=devoiced)) + geom_boxplot() +geom_jitter(alpha=0.2) + ggtitle("Length of following pause, by devoicing")

ggplot(inEnvt,aes(y=log(follPz),x=follBreak.type,fill=devoiced)) + geom_boxplot() +ylab("Log of following pause duration")+xlab("Following break type") + ggtitle("Dur of following pause by break type")

## Mean follPz for voiced/devoiced Vs
dvpz <- ddply(inEnvt,.(devoiced),summarise,mean.follPz=mean(follPz,na.rm=T))
## Excludes 2s with BPM 
ddply(inEnvt[inEnvt$follBreak.bpm!="Y",],.(devoiced),summarise,mean.follPz=mean(follPz,na.rm=T))

## Mean follPz by BPM
ddply(inEnvt,.(follBreak.bpm),summarise,mean.follPz=mean(follPz,na.rm=T))
summary(inEnvt$follBreak)

## Count of breaktype by devoiced
ggplot(inEnvt, aes(x=follBreak.type,fill=devoiced)) + geom_bar(position="fill") + ggtitle("Proportion of devoiced vowels by following break type") + ylab("Proportion devoiced") + xlab("Following break type")

## Prec breaktype
ggplot(inEnvt, aes(x=prevBreak.type,fill=devoiced)) + geom_bar(position="fill") + ggtitle("Proportion of devoiced vowels by preceding break type") + ylab("Proportion devoiced") + xlab("Preceding break type")
ggplot(inEnvt,aes(y=log(prevPz),x=devoiced)) + geom_boxplot() +geom_jitter(alpha=0.2) + ggtitle("Length of following pause, by devoicing") ## need to make prevPz numeric


## %devoiced by BPM
ggplot(inEnvt[inEnvt$follBreak.type=="2",], aes(x=follBreak.bpm,fill=devoiced)) + geom_bar(position="fill") + ggtitle("Proportion devoiced by BPM presence") + ylab("Proportion devoiced") + xlab("Boundary pitch movement")


## Only for breaktype 1 
type1 <- ggplot(inEnvt[inEnvt$follBreak.type=="1",], aes(x=follBreak,fill=devoiced)) + geom_bar(position="fill") + ggtitle("Break 1") + ylab("% devoiced") + xlab("Following break")

type2 <- ggplot(inEnvt[inEnvt$follBreak.type=="2",], aes(x=follBreak,fill=devoiced)) + geom_bar(position="fill") + ggtitle("Break 2") + ylab("% devoiced") + xlab("Following break") 

type3 <- ggplot(inEnvt[inEnvt$follBreak.type=="3",], aes(x=follBreak,fill=devoiced)) + geom_bar(position="fill") + ggtitle("Break 3") + ylab("% devoiced") + xlab("Following break")

type4 <- ggplot(inEnvt[inEnvt$follBreak.type=="Other",], aes(x=follBreak,fill=devoiced)) + geom_bar(position="fill") + ggtitle("Other") + ylab("% devoiced") + xlab("Following break")

multiplot(type1,type2,type3,type4,cols=2)


## %devoiced by POA
precPOA <- ggplot(inEnvt, aes(x=precPOA,fill=devoiced)) + geom_bar(position="fill")
follPOA <- ggplot(df, aes(x=follPOA,fill=devoiced)) + geom_bar(position="fill")
multiplot(precPOA,follPOA)

## Devoiced by coda/onset

 ggplot(inEnvt, aes(x=onset,fill=devoiced)) + geom_bar(position="fill") + facet_wrap(~ coda) + ylab("devoiced") + xlab("Onset, separated by Coda")



## Logistic regressino NO IDEA
mod1 <- glm(dv ~ follBreak.type + follPz,data=inEnvt,family="binomial")
summary(mod1)

## Histogram of log follPz for break 3 and break 2
hist(log(inEnvt$follPz[inEnvt$follBreak.type=="3"])) # Looks normally distributed
hist(log(inEnvt$follPz[inEnvt$follBreak.type=="2"])) # Left-skewed.
hist(log(inEnvt$follPz[inEnvt$follBreak.type=="1"]))
hist(log(inEnvt$follPz))



df$tone.type = "Other"
df$tone.type[df$tone %in% c("%L","%Lx","")]




