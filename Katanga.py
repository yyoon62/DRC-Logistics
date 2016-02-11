from pymprog import *
import csv
import numpy as np
#data and index
distm = np.loadtxt(open("kMat.csv","rb"),delimiter=',')

iid,jid = range(len(distm)),range(len(distm))
E= [(i,j) for i in iid for j in jid if i!=j]

source = [1]
sink =[12]
itm = [source[0],sink[0]]
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


st([sum( x[i,j] for i in iid if i!=j)== sum( x[j,i] for i in iid if i!=j) for j in jid if j not in itm])
solve("float")

print("Total Cost= %g"%vobj())

for item in E:
	if x[item].primal > 0:
		print x[item]

