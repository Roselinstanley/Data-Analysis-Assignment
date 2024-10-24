import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from statsmodels.distributions.empirical_distribution import ECDF
from scipy.stats import norm
class Datapre:
    quan=[]
    qual=[]
    def __init__(self,dataset):
        self.dataset=dataset
        self.Lesser=[]
        self.Greater=[]
    def quanqual(self):
        for cname in self.dataset.columns:
            if(self.dataset[cname].dtype=='O'):
                self.qual.append(cname)
            else:
                self.quan.append(cname)
        return self.qual,self.quan
    def central(self):
        global centraluni
        centraluni=pd.DataFrame(index=["Mean","Median","Mode","Q1:25","Q2:50","Q3:75","Q4:100","IQR","1.5*IQR","Lesser","Greater","Min","Max"],columns=self.quan)
        for cname in self.quan:
            centraluni[cname]["Mean"]=self.dataset[cname].mean()
            centraluni[cname]["Median"]=self.dataset[cname].median()
            centraluni[cname]["Mode"]=self.dataset[cname].mode()[0]
            centraluni[cname]["Q1:25"]=self.dataset.describe()[cname]["25%"]
            centraluni[cname]["Q2:50"]=self.dataset.describe()[cname]["50%"]
            centraluni[cname]["Q3:75"]=self.dataset.describe()[cname]["75%"]
            centraluni[cname]["Q4:100"]=np.percentile(self.dataset[cname],100)
            centraluni[cname]["IQR"]=centraluni[cname]["Q3:75"]-centraluni[cname]["Q1:25"]
            centraluni[cname]["1.5*IQR"]= 1.5*centraluni[cname]["IQR"]
            centraluni[cname]["Lesser"]= centraluni[cname]["Q1:25"]-centraluni[cname]["1.5*IQR"]
            centraluni[cname]["Greater"]=centraluni[cname]["Q3:75"]+centraluni[cname]["1.5*IQR"]
            centraluni[cname]["Min"]=self.dataset[cname].min()
            centraluni[cname]["Max"]=self.dataset[cname].max()
        return centraluni
    def outliercheck(self):
        for cname in self.quan:
            if(centraluni[cname]["Min"] < centraluni[cname]["Lesser"]):
                self.Lesser.append(cname)
            if(centraluni[cname]["Max"] > centraluni[cname]["Greater"]):
                self.Greater.append(cname)
        return self.Lesser,self.Greater
    def replaceoutliers(self):
        for cname in self.Lesser:
            self.dataset[cname][self.dataset[cname] < centraluni[cname]["Lesser"]]=centraluni[cname]["Lesser"]
        for cname in self.Greater:
            self.dataset[cname][self.dataset[cname] > centraluni[cname]["Greater"]]=centraluni[cname]["Greater"]
        return self.dataset
    def calc_pdf(self):
        ax=sb.distplot(self.dataset['salary'],kde=True,kde_kws={'color':'pink'},color='green')
        plt.axvline(700000,color='yellow')
        plt.axvline(900000,color='yellow')
        plt.show()
        mean=self.dataset['salary'].mean()
        std=self.dataset['salary'].std()
        normdist=norm(mean,std)
        values=[value for value in range(700000,900000)]
        probabilities=[normdist.pdf(value) for value in values]
        prob=sum(probabilities)
        probpercent=prob * 100
        ecdf=ECDF(self.dataset['salary'])
        ecdfout=ecdf(250000)
        print("The area of Salary between the range ({},{}):({},{}){}".format(700000,900000,prob,probpercent,ecdfout))
        return  
    def std_normal(self):
        mean=self.dataset['salary'].mean()
        std=self.dataset['salary'].std()
        values=[i for i in self.dataset['salary']]
        z_score=[((j-mean)/std) for j in values]
        df=pd.DataFrame(columns=["Z_Score"])
        df["Z_Score"]=z_score
        print("The Z_SCORE plot of SALARY ")
        sb.displot(z_score,kde=True)
        plt.show()
        display(df)
        return
        
        
    
