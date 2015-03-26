# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 15:19:39 2015

@author: jmf
"""
import csv
import characterFeature as cf
import scipy.spatial.distance as ssd
import numpy as np

def nameMap(kaggleFile,scrapedFile):
    kag = []
    print "Read in Kaggle File"
    with open(kaggleFile,'rb') as f:
        csvr = csv.reader(f,delimiter=',')
        for row in csvr:
            if not row[1] == "team_name":
                kag.append(row)
            else:
                print row
                
    print "Read in Scraped File"
            
    with open(scrapedFile,'rb') as f2:
        a = f2.read().split("\n")
     
    empty = cf.createDict()     
    kagVecs = []
    scVecs = []
    print "Vectorize Kaggle Names"
    for row in kag:
        v = cf.toVector(row[1],empty)
        kagVecs.append(v)
    print "Vectorize Scraped Names"
    for row in a:
        v = cf.toVector(row,empty)
        scVecs.append(v)
        
    kagVecs = np.array(kagVecs)
    scVecs = np.array(scVecs)
        
    maxes=[]
    count =0
    with open("team_conversions_alg.csv",'wb') as f:
        my_write = csv.writer(f)
        for vec1 in kagVecs:
            basicSim=[]
            cosine=[]
            for vec2 in scVecs:
                s = np.multiply(vec1,vec2)
                basicSim.append(np.sum(s))
                cosine.append(ssd.cosine(vec1,vec2))
            amL=np.argsort(basicSim)[::-1][:-3]                
            amL2=np.argsort(cosine)

#            
#            if basicSim[amL[0]] == basicSim[amL[1]]:
#                temp=raw_input("wait")
#                i1 = np.where(amL2 == amL[0])[0]
#                i2 = np.where(amL2 == amL[1])[0]
#                print i1, i2
#                if i1 > i2:
#                    switch=amL[0]
#                    amL[0]=amL[1]
#                    amL[1]=switch
#                    print "switched"
#                temp=raw_input("done")
            print kag[count][1], a[amL[0]],a[amL[1]],a[amL[2]]
            my_write.writerow([kag[count][0],kag[count][1],a[amL[0]],a[amL[1]],a[amL[2]]])
            count+=1
    maxes=[]
    count =0

    
nameMap("teams.csv","teamnames.txt")
        
    