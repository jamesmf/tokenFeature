# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 15:05:10 2015

@author: jmf
"""

import numpy as np
import characterFeature
from sklearn.svm import LinearSVC
import re
import wikirandom
import cPickle
from os.path import isfile
import sys
from sklearn import linear_model
from sklearn.utils import shuffle


def getSampleProteins(mod,sampsize):
    m=mod
    with open("../data/dedupe.txt",'rb') as f:
        names1 = f.read().split("\n")
        
    print len(names1)
    #names2=[]
    #empty = characterFeature.createDict(N=4)
    protDict = {}
    excounts={}


    for i in range(0,sampsize):
        if (i-1)%1000 == 0:
            print str(i-1) + "/" + str(sampsize)
        j = np.random.randint(0,len(names1)-1)
        sample = names1[j]
        y = sample.strip().split(" ")[1:]
        n = " ".join(y)
        if excounts.has_key(len(y)):
            excounts[len(y)] = excounts[len(y)]+1
        else:
            excounts[len(y)] = 1
        cf = characterFeature.toVector(n,N=4,mod=m)
        protDict[n] = cf
    return protDict, excounts


def getRandomWords(mod,sampsize,excounts):
         
    wikirand, wikititles = wikirandom.get_random_wikipedia_articles(400)
    randText = ""
    count = 0
    for art in wikirand:
        if art.find("protein") == -1:
            if wikititles[count].lower().find("list") == -1:
                randText += art
        count+=1
    
    pat = re.compile("&quot")
    randText = re.sub(pat, '',randText).lower()
    strip = re.compile("[^a-z0-9 ]")
    nums = re.compile("[0-9]")
    randText=re.sub(strip,' ',randText)
    randText=re.sub(nums,'#',randText)
    pat = re.compile("\s")
    randWords = re.split(pat,randText)
    l = len(randWords)
    d = []
    for a,c in excounts.iteritems():
        print c*1./sampsize
        if c*1./sampsize > 0.05:
            for k in range(0,c/2):
                a=int(a)
                ind = np.random.randint(0,l-a)
                s = "!".join(randWords[ind:ind+a])
                plain = characterFeature.toVector(s,N=4,mod=mod)
                d.append(plain)
    return d
    
def getExamples(mod,sampsize):
    prot, excounts = getSampleProteins(mod,sampsize)
    prot = prot.values()
    prot = np.array(prot,ndmin=1)
    print prot.shape
    lab1 = np.ones(len(prot))
    wordExamples = getRandomWords(mod,sampsize,excounts) 
    wordExamples = np.array(wordExamples,ndmin=1)
    lab0 = np.zeros(len(wordExamples))
    return np.append(prot,wordExamples,axis=0), np.append(lab1,lab0)
 
def main():

    mod=5000 
    sampsize=5000      
    
    if len(sys.argv) > 1:
        modelF = sys.argv[1]
    else:
        modelF = "../model/SVM1.pickle"
        
    if len(sys.argv) > 2: 
        useSGD = True
        update = True
        if sys.argv[2] == "new":
            update = False
            
    if useSGD:
        print "using SGD"
        if not update:
            print "creating new model"            
            clf = linear_model.SGDClassifier(shuffle=True)
        else:
            print "loading old model: "+ str(modelF) 
            with open(modelF,'rb') as effsies:
                clf = cPickle.load(effsies)

        data, labels = getExamples(mod,sampsize)
        data, labels = shuffle(data,labels)
        clf.partial_fit(data,labels,np.array([1.,0.]))
        
        numIts = modelF.split("/")[-1].split("_")[-1]
        numIts = int(numIts[:numIts.find(".")])
        modelF2 = modelF.replace("_"+str(numIts),"_"+str(numIts+1))
        
        with open(modelF2,'wb') as f:
            cp = cPickle.Pickler(f)
            cp.dump(clf)
        
    if (not isfile(modelF)) & (not useSGD):
        data, labels = getExamples(mod,sampsize)
        
        print data.shape, labels.shape
        clf = LinearSVC()
        clf.fit(data,labels)
        
        with open(modelF,'wb') as f:
            cp = cPickle.Pickler(f)
            cp.dump(clf)
    elif not useSGD:
        print "loading LinearSVC"
        with open(modelF,'rb') as f:
            clf = cPickle.load(f)
        print "loaded"
    
    st = ["I am an American","I met with 4 ducks","isomerase 14","MAPK1","Nothing4","farnesyl","farnesyl transferase","number 4"]
    d = []
    print mod
    for x in st:
        d = characterFeature.toVector(x,N=4,mod=mod)
        print str(x) + ":\t" + str(clf.predict(d))     


        
if __name__ == '__main__':
    main()
    
    