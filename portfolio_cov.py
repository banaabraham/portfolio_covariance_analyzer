# -*- coding: utf-8 -*-
"""
Created on Sun Jul  2 19:52:29 2017

@author: bana
"""
from matplotlib import pyplot as plt
import statistics
import pandas as pd
import itertools
from multiprocessing import Process, Manager
import urllib


#average function
def average(s):
    op=[]
    for i in s:
        op.append(stock_dict[i])
    return sum(op)/len(op) 


#portfolio generator and return its covariance to a shared variable and choose which has the lowest covariance
def analyze(dow,n,return_dict):
    count=0
    a=10000
    for c in itertools.combinations(dow, n):
        count+=1
        if a>average(c):
            a=average(c)
            tick=c
    return_dict[tick] =[a,count]        

#dow 30 list stocks
#dow="amzn aapl ba cat csco cvx dd dis fitb ge goog gs hd ibm intc jnj jpm ko mcd mmm mrk pfe pg trv tsla unh v vz wfc wmt xom yhoo"
#dow=dow.split(" ")
f = open("SP100.txt","r")
dow = [x.strip("\n") for x in f.readlines()]
stock_dict={}
portfolio=[]
CVs=[]


for ticker in dow:
    stock=ticker+".csv"
    try:
        d=pd.read_csv(stock)
    except:
        try:
            url="https://www.google.com/finance/historical?output=csv&q="+ticker
            urllib.request.urlretrieve(url,stock)
            d=pd.read_csv(stock)
        except:
            pass    
    data = d['Close'].values
    #calculate monthly return
    mth_return = []  
    for i in range(len(data)-1,0,-30):
        mth_return.append((data[i]-data[i-30])/data[i-30])
    #calculating risk and covariance 
    resiko = statistics.stdev(mth_return)
    laba=(data[0]-data[-1])/data[-1]
    if laba<0:
        stock_dict[ticker] = 10000.0
    else:    
        stock_dict[ticker] = float(resiko/(laba**2))
    
if __name__ == '__main__':
    
    manager = Manager()
    return_dict = manager.dict()
    n=list(range(3,5))
    #calculating average covariance of the combinations of stocks using multi process
    thread=[]
    for i in n:
        t=Process(target=analyze, args=(dow,i,return_dict))
        thread.append(t)
        t.start()        
    for t in thread:
        t.join()
        
    #print (return_dict)    
    a=[]
    b=[]
    #print(return_dict)  
    for i in return_dict.values():
       a.append(i[0])
       b.append(i[1])
    plt.plot(a)
    print (sum(b))   
    print (return_dict)
