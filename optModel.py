from pymprog import *
import csv
import numpy as np

#data and index
with open("data/kPath.csv","rb") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        row1 = next(reader)

temp = row1[1:]
indexDict = {}

for i in range(len(temp)):

        indexDict[temp[i]] =i 


distm = np.loadtxt(open("data/kMat.csv","rb"),delimiter=',')
cm = np.loadtxt(open("data/kConditionMat.csv","rb"),delimiter=",")

iid,jid = range(len(distm)),range(len(distm))
seasonality = 0
if seasonality ==1:
        for i in iid:
            for j in jid:
                if cm[i][j]==1:
                    distm[i][j] = distm[i][j]*1.05
                elif cm[i][j]==2:
                    distm[i][j] = distm[i][j]*1.2
                elif cm[i][j]==3:
                    distm[i][j] = distm[i][j]*1.3
                elif cm[i][j]==4:
                    distm[i][j] = distm[i][j]*1.4
                else:
                    pass
                

E= [(i,j) for i in iid for j in jid if i!=j]

cities=[]
with open("data/kStarting.csv","rb") as csvfile:
    read = csv.reader(csvfile,delimiter=",")
    for item in read:
        cities.extend(item)
 


source = [indexDict["Kiambi"]]
sink =[indexDict["Lubumbashi"]]
itm = [source[0],sink[0]]
season = "d"
#Modeling
beginModel("katanga")
x=var(E,'x', bool) #decision variable

#Objective function
minimize( sum(distm[i][j]*x[i,j] for i,j in E),"Total Time")

#constraints

#source
st([sum( x[i,j] for j in jid if i!=j)==1 for i in source],"leave")
st([(x[i,j])==0  for j in source for i in iid if i!=j],'no enter')

#sink
st([sum( x[i,j] for i in iid if j!=i)==1 for j in sink],"enter") 
st([(x[i,j])==0 for i in sink for j in jid if i!=j])

#conservation of flow
st([sum( x[i,j] for i in iid if i!=j)== sum( x[j,i] for i in iid if i!=j) for j in jid if j not in itm])

solve("float")
print("Total Cost= %g"%(vobj()))
tempList = []
for item in E:
    if x[item].primal > 0:
        tempList.append(x[item])
        print x[item]
        print temp[item[0]],temp[item[1]]



