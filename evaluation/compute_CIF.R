remove(list=ls()) 
setwd("C:/Users/gorizadeh/Desktop/RemoteDesktop/CompetingRisk-DeepHit/SurvAnalysisCompetingRisks/DeepHit-master-one-event/evaluation/")
library(survival)
library(Epi)
library(prodlim)
library(pec)
library(cmprsk)
library(riskRegression)
library(prodlim)
source ("CumIncidence.R")

"myplotCIF" <- function (x, event = 1, xlab = "Time", ylab = "Cumulative incidence", 
          ylim = c(0, 1), lty = 1, col = "black", ...) 
{
  ng <- length(x$n)
  co <- rep(col, ng)[1:ng]
  lt <- rep(lty, ng)[1:ng]
  ne <- dim(x$pstate)[2] - 1
  if (event %in% 1:ne) {
    time <- x$time
    gr <- rep(1, length(time))
    if (ng > 1) 
      for (g in 2:ng) for (t in (cumsum(x$strata)[g - 
                                                  1] + 1):cumsum(x$strata)[g]) gr[t] <- g
    CI <- x$pstate[, 2]
    for (e in 1:ne) if (event == e) 
      CI <- x$pstate[, e + 1]
    #plot(c(0, time[gr == 1], max(time[gr == 1])), c(0, CI[gr == 
    #                                                        1], max(CI[gr == 1])), type = "s", ylim = ylim, 
    #     xlab = xlab, ylab = ylab, col = co[1], lty = lt[1], 
    #     ...)
    returnTimes<-c(0, time[gr == 1], max(time[gr == 1]))
    returnCIs  <-c(0, CI[gr == 1], max(CI[gr == 1]))
    
    if (ng > 1) 
      for (g in 2:ng) lines(c(0, time[gr == g], max(time[gr == 
                                                           g])), c(0, CI[gr == g], max(CI[gr == g])), type = "s", 
                            lty = lt[g], col = co[g], ...)
  }
  else print(paste("Error: event must be an integer from 1 to", 
                   ne))
  return(list(returnTimes,returnCIs))
}


dataset  <-'crash2bo'# 0.2,0.4,0.8,crash2,ICU,SEER

instances <-c('1','12','123','1234','4123','5123','6123','7123','8123','9123')#,'12','123','1234','4123','5123','6123','7123','8123','9123')
tmax   <-if(dataset=='crash2' || dataset=='crash2bo' || dataset=='crash2da') 28 else 20
tmax   <-if(dataset=='ICU') 60 else tmax
tmax   <-if(dataset=='SEER') 13 else tmax
tcs<-if(dataset=='ICU') 2 else 1 # Starting time point for Cindex calculation
tce<-if(dataset=='ICU') tmax-1 else tmax # ending time point for Cindex calculation
tce<-if(dataset=='SEER') tmax-1 else tmax # ending time point for Cindex calculation


fsep<-.Platform$file.sep
dataName<-""

avgGT<-NULL
avgSpr<-NULL
avgMpr<-NULL
avgOEpr<-NULL # No preprocessing, one event

avgScindx<-NULL
avgMcindx<-NULL
avgOEcindx<-NULL

avgSbrier<-NULL
avgMbrier<-NULL
avgOEbrier<-NULL

avgPECref<-NULL
avgPECSmat<-NULL
avgPECMmat<-NULL
avgPECOEmat<-NULL

fullDataTable<-list()

for(ending in instances)
{ 
# Name of files of interest 
gtName<-paste(".",fsep,dataset,"-input-unc-",ending,".txt",sep = "")
prSngleSubNetName <-paste(dataset,"-drawn-",ending,".txt","",sep="")
prMultiSubNetName <-paste(dataset,"-uncen-",ending,".txt",sep="")
prOneEventSubNetName <-paste(dataset,"-oneevent-",ending,".txt",sep="")

if(dataset=='crash2'){
  varNames <- c("state", "None","isex", "iage", "ninjurytime", "iinjurytype",
                "isbp", "ihr", "irr", "icc", "igcs", "time.discrete")  
}else{
  varNames <- c("state", "None","x1","x2","x3","x4", "time.discrete")
}
if(dataset=='crash2bo' || dataset=='crash2da'){
  varNames <- c("state", "None","isex", "iage", "ninjurytime", "iinjurytype",
                "isbp", "ihr", "irr", "icc",  "time.discrete")  
}
if(dataset=='ICU')
{
  varNames <- c("state", "None","age", "SAPS_II", "female", "intubation", "pneumonia",
                "LRT", "harn", "other_inf", "hospital", "elective", "emergency",
                "card_pul", "neurological", "met_ren", "time.discrete") 
}
if(dataset=='SEER')
{
  
  varNames <- c("state", "None","marstat", "racrecy", "nhia", "agedx", "siteo2",
                "lateral", "grade", "eod10pn", "eod10ne", "radiatn", "radsurg",
                "numprims", "erstatus", "prstatus", "adjtm6value", "adjnm6value",
                "tumorsize", "surgprimRecode", "time.discrete") 
}
# Read files
gtr <- read.table(paste(".",fsep,dataset,"-input-unc-",ending,".txt",sep = ""))#[1:10000,]

if(dataset=='crash2da')
{
  spr <- read.table(paste(".",fsep,prSngleSubNetName, sep = ""))[3:6851,]
  mpr <- read.table(paste(".",fsep,prMultiSubNetName, sep = ""))[3:6851,]
  oepr <- read.table(paste(".",fsep,prOneEventSubNetName, sep = ""))[3:6851,]
}
else{
spr <- read.table(paste(".",fsep,prSngleSubNetName, sep = ""))#[3:6486,]
mpr <- read.table(paste(".",fsep,prMultiSubNetName, sep = ""))#[3:6486,]
oepr <- read.table(paste(".",fsep,prOneEventSubNetName, sep = ""))#[3:6486,]
}


names(gtr) <- varNames
table(gtr$state)
# Use fine-Gray for True CIF
if(FALSE)
{
# Call 'cuminc' function from cmprsk package.
fit<-CumIncidence (gtr$time.discrete, gtr$state,  
                   cencode = 0, 
                   xlab = "Time Intervals")
time <- pretty(c(0, max(gtr$time.discrete)), 6)
time <- sort(unique(c(gtr$time.discrete, time)))
x <- timepoints(fit, time)

# CIF Baseline for E1 and E2
cifE1<-x$est[1,]
cifE2<-x$est[2,]
}
# Use Aalen-Johansen for True CIF

x<-survfit( Surv( time.discrete, state,type='mstate' ) ~ 1, data=gtr )
pl<-myplotCIF( x, event = 1,
         xlab = "Time",
         ylab = "Cumulative incidence",
         ylim = c(0, 1),
         lty = 1,
         col = "black" )
time <-as.numeric(unlist(pl[1]))
## CIF Baseline for E1
cifE1<-as.numeric(unlist(pl[2]))


#### Compute CIF from predicted values ####
sprCIF <- apply(spr, 1, cumsum)
mprCIF <- apply(mpr, 1, cumsum)
oeprCIF <- apply(oepr, 1, cumsum)

sprCIF <- t(sprCIF[1:tmax,])
mprCIF <- t(mprCIF[1:tmax,])
oeprCIF <- t(oeprCIF[1:tmax,])

###########################
# CIndex computation
###########################
print(table(gtr$state))
cINDs<-cindex(sprCIF, 
              formula=Hist(time.discrete, state) ~ 1,
              data = gtr, 
              eval.times = seq(1, tmax, 1), 
              #pred.times = seq(1, 14, 1), 
              cause=1, 
              lyl = FALSE,
              cens.model = "marginal"
)

cINDm<-cindex(mprCIF, 
               formula=Hist(time.discrete, state) ~ 1, 
               data = gtr, 
               eval.times = seq(1, tmax, 1), 
               #pred.times = seq(1, 14, 1), 
               cause=1, 
               lyl = FALSE,
               cens.model = "marginal"
)

cINDoe<-cindex(oeprCIF, 
              formula=Hist(time.discrete, state) ~ 1, 
              data = gtr, 
              eval.times = seq(1, tmax, 1), 
              #pred.times = seq(1, 14, 1), 
              cause=1, 
              lyl = FALSE,
              cens.model = "marginal"
)

###########################
# Brier Score Computation
###########################
upval<-tmax-1
# prediction error curves
PECS <- pec(sprCIF, # matrix containing the predicted survival curves
            formula = Hist(time.discrete, state) ~ 1, # the formula for the censoring model
            data = gtr, # test data
            #traindata = dat, # training data
            times = seq(1, upval, 1), # vector of time points on which to evaluate
            cens.model = "marginal",
            cause=1,
            exact = FALSE
)

print("S:================")
print(ibs(PECS))

PECM <- pec(mprCIF, # matrix containing the predicted survival curves
            formula = Hist(time.discrete, state) ~ 1, # the formula for the censoring model
            data = gtr, # test data
            #traindata = dat, # training data
            times = seq(1, upval, 1), # vector of time points on which to evaluate
            cens.model = "marginal",
            cause=1,
            exact = FALSE
)

print("M:================")
print(ibs(PECM))

PECOE <- pec(oeprCIF, # matrix containing the predicted survival curves
            formula = Hist(time.discrete, state) ~ 1, # the formula for the censoring model
            data = gtr, # test data
            #traindata = dat, # training data
            times = seq(1, upval, 1), # vector of time points on which to evaluate
            cens.model = "marginal",
            cause=1,
            exact = FALSE
)

print("OE:================")
print(ibs(PECOE))

# Take the average value
meanSpreCIF <- c(0,apply(sprCIF[,1:tmax], 2, mean))
meanMpreCIF <- c(0,apply(mprCIF[,1:tmax], 2, mean))
meanOEpreCIF <- c(0,apply(oeprCIF[,1:tmax], 2, mean))

fullDataTable[['cind-single']]<-append(fullDataTable[['cind-single']],cINDs$AppCindex$matrix[tcs:tce])
fullDataTable[['cind-multiple']]<-append(fullDataTable[['cind-multiple']],cINDm$AppCindex$matrix[tcs:tce])
fullDataTable[['cind-oneevent']]<-append(fullDataTable[['cind-oneevent']],cINDoe$AppCindex$matrix[tcs:tce])

fullDataTable[['brier-single']]<-append(fullDataTable[['brier-single']],PECS$AppErr$matrix[2:tmax])
fullDataTable[['brier-multiple']]<-append(fullDataTable[['brier-multiple']],PECM$AppErr$matrix[2:tmax])
fullDataTable[['brier-oneevent']]<-append(fullDataTable[['brier-oneevent']],PECOE$AppErr$matrix[2:tmax])
fullDataTable[['brier-ref']]<-append(fullDataTable[['brier-ref']],PECM$AppErr$Reference[2:tmax])

fullDataTable[['ibs-single']]<-append(fullDataTable[['ibs-single']],ibs(PECS)[2])
fullDataTable[['ibs-multiple']]<-append(fullDataTable[['ibs-multiple']],ibs(PECM)[2])
fullDataTable[['ibs-oneevent']]<-append(fullDataTable[['ibs-oneevent']],ibs(PECOE)[2])
fullDataTable[['ibs-ref']]<-append(fullDataTable[['ibs-ref']],ibs(PECS)[1])

if(is.null(avgGT))
{
  avgGT<-cifE1
  avgSpr<-meanSpreCIF
  avgMpr<-meanMpreCIF
  avgOEpr<-meanOEpreCIF
  
  avgScindx<-cINDs$AppCindex$matrix[tcs:tce]
  avgMcindx<-cINDm$AppCindex$matrix[tcs:tce]
  avgOEcindx<-cINDoe$AppCindex$matrix[tcs:tce]
  
  avgPECref<-PECM$AppErr$Reference[2:tmax]
  avgPECSmat<-PECS$AppErr$matrix[2:tmax]
  avgPECMmat<-PECM$AppErr$matrix[2:tmax]
  avgPECOEmat<-PECOE$AppErr$matrix[2:tmax]
  
}else{
  avgGT<-avgGT+cifE1
  avgSpr<-avgSpr+meanSpreCIF
  avgMpr<-avgMpr+meanMpreCIF
  avgOEpr<-avgOEpr+meanOEpreCIF
  
  avgScindx<-avgScindx+cINDs$AppCindex$matrix[tcs:tce]
  avgMcindx<-avgMcindx+cINDm$AppCindex$matrix[tcs:tce]
  avgOEcindx<-avgOEcindx+cINDoe$AppCindex$matrix[tcs:tce]
  
  avgPECref<-PECM$AppErr$Reference[2:tmax]+avgPECref
  avgPECSmat<-PECS$AppErr$matrix[2:tmax]+avgPECSmat
  avgPECMmat<-PECM$AppErr$matrix[2:tmax]+avgPECMmat
  avgPECOEmat<-PECOE$AppErr$matrix[2:tmax]+avgPECOEmat
}
}
denom<-length(instances)
avgGT<-avgGT/denom
avgSpr<-avgSpr/denom
avgMpr<-avgMpr/denom
avgOEpr<-avgOEpr/denom

avgScindx<-avgScindx/denom
avgMcindx<-avgMcindx/denom
avgOEcindx<-avgOEcindx/denom

print("S=========")
print(avgScindx)
print("M=========")
print(avgMcindx)
print("OE========")
print(avgOEcindx)

if(denom>1){ending<-'mean'}
#### PLOT CINDEX #####
legendLocation <- c(0.0,1.0)
strErate<-if(dataset=='crash2' || dataset=='crash2bo' || dataset=='crash2da') 5 else as.numeric(dataset)*100 
strErate<-if(dataset=='ICU') 90.3 else strErate 
strErate<-if(dataset=='SEER') 85 else strErate 
#strErate<-as.numeric(erate)*100
title <- paste(dataName,"C-index - Rate of event of interest ",strErate,"%",sep = "")

png(paste('.',fsep,'CNX-',
          dataset,"-deepHit-featureEng-",ending,".png",sep = ""),
    width = 842, height = 651,res=100)

par(mar=c(5,5,3,3))#,oma=c(5,5,5,5)

#type="s", ylim = c(0,1), xlab="t",ylab = "CIF",col="red",lwd=lineThickness,
# Draw in the same plot
plot(avgScindx,ylab = "", xlab = "time", lwd = 2, type = "l",col="#0066FF",ylim = c(0,1),main = title) # the fitted model
lines(avgMcindx, type = "l", lwd = 2, col = "black") # marginal model, should have a smaller error
lines(avgOEcindx, type = "l", lwd = 2, col = "#00E6E6") # marginal model, should have a smaller error

legend(10, 1, legend=c("Multiple sub-networks","Single sub-network","Single sub-network, no imputation"),
       col=c("black","#0066FF","#00E6E6"), lwd = 2, lty=1, cex=1.0)
dev.off()

#### PLOT PEC #####
legendLocation <- c(0.0,1.0)
strErate<-if(dataset=='crash2' || dataset=='crash2bo' || dataset=='crash2da') 5 else as.numeric(dataset)*100 
strErate<-if(dataset=='ICU') 90.3 else strErate 
strErate<-if(dataset=='SEER') 85 else strErate
#strErate<-as.numeric(erate)*100
title <- paste(dataName,"PEC - Rate of event of interest ",strErate,"%",sep = "")

png(paste('.',fsep,'PEC-',
          dataset,"-deepHit-featureEng-",ending,".png",sep = ""),
    width = 842, height = 651,res=100)

par(mar=c(5,5,3,3))#,oma=c(5,5,5,5)

#type="s", ylim = c(0,1), xlab="t",ylab = "CIF",col="red",lwd=lineThickness,
plot(avgPECref,ylab = "", lwd=3, xlab = "time", type = "l",col="red",ylim = c(0,2),main=title) # the fitted model
lines(avgPECSmat, type = "l", lwd=3,col = "#0066FF") # marginal model, should have a smaller error
lines(avgPECMmat, type = "l", lwd=3, col = "black") # marginal model, should have a smaller error
lines(avgPECOEmat, type = "l", lwd=3, col = "#00E6E6") # marginal model, should have a smaller error

legend(legendLocation[1],legendLocation[2], legend=c("Aalen-Johansen", "DeepHit with multiple subnetwork", "DeepHit with single subnetwork", "DeepHit with single subnetwork-No preprocessing"),
       col=c("red", "black", "#0066FF","#00E6E6"), lwd=3, lty=1, cex=1.5,bty = 'n')

dev.off()


####  PLOT #####
strErate<-if(dataset=='crash2' || dataset=='crash2bo' || dataset=='crash2da') 5 else as.numeric(dataset)*100 
strErate<-if(dataset=='ICU') 90.3 else strErate 
strErate<-if(dataset=='SEER') 85 else strErate
legendLocation<-if(dataset=='crash2' || dataset=='crash2bo' || dataset=='crash2da') c(0.0,0.3) else c(0.0,1.0)
limfory<-if(dataset=='crash2' || dataset=='crash2bo' || dataset=='crash2da') c(0.0,0.3) else c(0.0,1.0)
legendLocation<-if(dataset=='SEER') c(0.0,0.3) else legendLocation
limfory<-if(dataset=='SEER') c(0.0,0.3) else limfory
#strErate<-as.numeric(erate)*100
title <- paste(dataName,"Rate of event of interest ",strErate,"%",sep = "")
title<-" "
png(paste('.',fsep,'CIF-',
          dataset,"-deepHit-featureEng-",ending,".png",sep = ""),
    width = 842, height = 651,res=100)

par(mar=c(5,5,3,3))#,oma=c(5,5,5,5)

lineThickness<-4
matplot(time, avgGT, type="s", ylim = limfory, xlab="t",ylab = "CIF",col="red",lwd=lineThickness,main=title,cex.lab=2.0,cex.axis=2)
#plot( cifE1,  col = "red", xlab="t",ylab = "S(t)", ylim = c(0,1),lwd=1.5,cex.lab=2.5,cex.axis=2,main = "CIF",cex.main=2)

lines(0:tmax, avgMpr, lty=1, col = "#999999",lwd=lineThickness)
lines(0:tmax, avgSpr,  col = "#00e3e3",lwd=lineThickness)
lines(0:tmax, avgOEpr,  col = "#e39b00",lwd=lineThickness)  

legend(legendLocation[1],legendLocation[2], legend=c(expression(paste("",DeepHit^2,"",sep = "")),
                                                     expression(paste(DeepHit^1)),
                                                     expression(paste(DeepHit^1,", no imputation")),
                                                     "Aalen-Johansen"),
       col=c("#999999","#00e3e3","#e39b00","red"), lty=c(1,1,1,1), lwd=c(4,4,4,4),cex=2.0,bty = 'n')
dev.off()

method<-c("Single subnet-with preprocessing","Multiple subnets-no preprocessing","Single subnet-no preprocessing")
Cindex<-c()
for(n in names(fullDataTable)){
  if(grepl('cind',n, fixed = TRUE)){
    strval<-paste(round(mean(fullDataTable[[n]])*100,2),"+",round(sd(fullDataTable[[n]])*100,2),sep="")
    Cindex<-c(Cindex,strval)
  }
}
df<-data.frame(method,Cindex)
write.csv(df,paste('.',fsep,'cind-',
                   dataset,"-deepHit-featureEng-",ending,".csv",sep = ""), row.names = FALSE)