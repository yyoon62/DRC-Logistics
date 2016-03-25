from Tkinter import *
from tkFileDialog import *
import numpy as np
import csv

class polio:

    def __init__(self,win):

        win.wm_title("DRC Path Optimizer")  

        # Label Frame
        w1=LabelFrame(win, text="Upload Distance Matrix",width=50)
        w2=LabelFrame(win, text="Select a Province",width=50)
        w3=LabelFrame(win, text="Season")
        self.w4=LabelFrame(win, text="Choose City")
        self.w5=LabelFrame(win, text="Solution")
        w1.grid(row=0,columnspan=2,sticky="WE",padx=15,pady=10)
        w2.grid(row=1,column=0,sticky="WE",padx=15,pady=4)
        w3.grid(row=2,column=0,sticky="WE",padx=15) 
        self.w4.grid(row=1,column=1,sticky="WE",padx=15)
    
        # File Upload
        l1=Label(w1, text="Distance Matrix File:")
        l1.grid(row=0,column=0)
        
        self.e=Entry(w1,width=50)
        self.e.grid(row=0,column=1,columnspan=1)    
        self.e.insert(END,"...")
        self.e.config(state="readonly")
        b = Button(w1, text="choose file", command=self.openFileClicked)
        b.grid(row=0,column=4)

        #Province
        self.v = IntVar()
        self.rb1 = Radiobutton(w2,text="Katanga", variable=self.v, value=1,command=self.fileParser)
        rb2 = Radiobutton(w2,text="Equateur", variable=self.v, value=2,command=self.fileParser)
        rb3 = Radiobutton(w2,text="Orientale", variable=self.v, value=3,command=self.fileParser)
        self.rb1.grid(row=0,column=0,sticky="WE"); rb2.grid(row=0,column=1,sticky="WE"); rb3.grid(row=0,column=2,sticky="E")

        #Seasonality
        self.v2 = IntVar()

        rb4 = Radiobutton(w3,text="Rainy", variable=self.v2, value=1)
        rb5 = Radiobutton(w3,text="Dry", variable=self.v2, value=0)
        rb4.grid(row=0,column=0); rb5.grid(row=0,column=1)
    
        #city application

        self.var = StringVar(self.w4)
        self.var.set("...")
            
        #Optimize Button        
        b2 = Button(win, text="Optimize!", command=self.optimize)
        b2.grid(row=3,column=1,sticky="WE",padx=80,pady=12)

    def openFileClicked(self):
        
        self.fileName = askopenfilename()
        
        if self.fileName:
            
            self.e.config(state=NORMAL)
            self.e.delete(0,END)
            self.e.insert(END,self.fileName)
            self.e.config(state="readonly")
            with open(self.fileName,"rb") as csvfile:
                reader = csv.reader(csvfile,delimiter=",")
                row1= next(reader)

            temp = row1[1:]
            indexDict={}
            for i in range(len(temp)):
                indexDict[temp[i]]=i

    def fileParser(self):

        def menu():
            
            try:
                self.option.grid_remove()
            except:
                pass
            self.option = OptionMenu(self.w4,self.var,*self.cities)
            self.option.grid(row=0,column=0)

        if self.v.get()== 1:
                
            with open("data/kStarting.csv","rb") as csvfile:
                read = csv.reader(csvfile,delimiter=",")
                self.cities=["..."]
                for item in read:
                    self.cities.extend(item)
                    menu()

        elif self.v.get()==2:
            with open("data/eStarting.csv","rb") as csvfile:
                read = csv.reader(csvfile,delimiter=",")
                self.cities=["..."]
                for item in read:
                    self.cities.extend(item)
                    menu()

        elif self.v.get()==3:
            with open("data/oStarting.csv","rb") as csvfile:
                read = csv.reader(csvfile,delimiter=",")
                self.cities=["..."]
                for item in read:
                    self.cities.extend(item)
                    menu()

        
    def optimize(self):
        print("button clicked!")
        print(self.var.get())
        with open("data/kPath.csv","rb") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            row1 = next(reader)

        temp = row1[1:]
        indexDict = {}
        for i in range(len(temp)):

            indexDict[temp[i]] =i 



        distm = np.loadtxt(open(self.fileName,"rb"),delimiter=',')
        cm = np.loadtxt(open("data/kConditionMat.csv","rb"),delimiter=",")
        iid,jid = range(len(distm)),range(len(distm))

        seasonality = self.v2.get()
        print(self.v2.get())
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

        source = [indexDict[self.var.get()]]
        sink =[indexDict["Lubumbashi"]]
        itm = [source[0],sink[0]]
        season = "d"

        self.w5.grid(row=5,column=1,sticky="SNEW")
        Label(self.w5,text="cat is good").grid(row=0,column=0)
        Label(self.w5,text="how to get to Kinshasa").grid(row=1,column=0)

mw = Tk()
app = polio(mw)
mw.mainloop

