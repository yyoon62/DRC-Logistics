csvfile <- read.csv("cdcData.csv")

library(dplyr)#/

csvfile$Date1stStool <- as.Date(csvfile$Date1stStool,"%m/%d/%Y")
csvfile$Date2ndStool <- as.Date(csvfile$Date2ndStool,"%m/%d/%Y")
csvfile$DateOfOnset <- as.Date(csvfile$DateOfOnset,"%m/%d/%Y")
csvfile$DateNotified <- as.Date(csvfile$DateNotified,"%m/%d/%Y")
csvfile$DateStoolSentolab <- as.Date(csvfile$DateStoolSentolab,"%m/%d/%Y")
csvfile$DateSpecRecbyNatLab <- as.Date(csvfile$DateSpecRecbyNatLab,"%m/%d/%Y")
csvfile$DateCaseinvestigated <- as.Date(csvfile$DateCaseinvestigated,"%m/%d/%Y")
#lower case the District and Province names
csvfile<-mutate(csvfile,District=tolower(District))
csvfile<-mutate(csvfile,Province=tolower(Province))
csvfile<-mutate(csvfile,Towncity=tolower(Towncity))
csvfile$Province[csvfile$Province=="oriental"]="orientale"
csvfile$Province[csvfile$Province=="kasai-or"]="kasai-oriental"
csvfile$Province[csvfile$Province=="kasai-occ"]="kasai-occidental"

#create 1st and 2nd leg times

csvfile <- mutate(csvfile,leg1=as.numeric(DateStoolSentolab-Date2ndStool))
csvfile <- mutate(csvfile,leg2=as.numeric(DateSpecRecbyNatLab-DateStoolSentolab))
csvfile <- mutate(csvfile,invTime=as.numeric(DateCaseinvestigated-DateNotified))
csvfile <- mutate(csvfile,totalTime=leg1+leg2)
