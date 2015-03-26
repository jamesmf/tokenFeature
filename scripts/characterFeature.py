# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 13:55:52 2015

@author: jmf
"""
import re
import operator
import numpy as np
import scipy.spatial.distance as ssd
import hashlib
import time

def createDict(N=3,h=True,mod=20000):   
    t1 = time.time()
    l=[]
    for i in range(ord('a'),ord('z')+1):
        l.append(chr(i))
    l.append('!')
    l.append('#')
    d = {}
    for x in l:
        key = myhash(x,mod)
        if h:
            d[key]=0
        else:
            d[x]=0
        if N > 1:
            for y in l:
                key = myhash((x+y),mod)
                if h:
                    d[key] = 0
                else:
                    d[x+y] = 0  
                if N > 2:
                    for z in l:
                        key = myhash((x+y+z),mod)
                        if h:
                            d[key] =0
                        else:
                            d[x+y+z] = 0
                        if N > 3:
                            for a in l:
                                key = myhash((x+y+z+a),mod)
                                if h:
                                    d[key]=0
                                else:
                                    d[x+y+z+a] = 0
                                if N > 4:
                                    for b in l:
                                        key = myhash((x+y+z+a+b),mod)
                                        if h:
                                            d[key]=0
                                        else:
                                            d[x+y+z+a+b] = 0
                                        if N > 5:
                                            for c in l:
                                                key = myhash((x+y+z+a+b+c),mod)
                                                if h:
                                                    d[key] = 0
                                                else:
                                                    d[x+y+z+a+b+c] = 0
                                                if N > 6:
                                                    for e in l:
                                                        key = myhash((x+y+z+a+b+c+e),mod)
                                                        if h:
                                                            d[key] = 0
                                                        else:
                                                            d[x+y+z+a+b+c+e] = 0
                                                        
    print "dict length " + str( len(d))
    print d.items()[0:100]
    print time.time()-t1
    return d
    
def myhash(s,mod):
    return int(int(hashlib.md5(s.encode()).hexdigest(),16)%mod)
    
def toList(d):
    return [value for key, value in sorted(d.items(),key=operator.itemgetter(0))]
    
def trimLower(s):
    sp = re.compile("\s+")
    s=re.sub(sp,' ',s.lower())
    return s
    

def processToken(token):
    token = " "+token+" "
    strip = re.compile("[^a-z0-9 ]")
    nums = re.compile("[0-9]")
    t=trimLower(token) 
    t=re.sub(strip,' ',t)
    t=re.sub(nums,'#',t)
    t=t.replace(' ','!')
    return t
    
def nGrams(token,n,d,h=True,mod=20000):
    l = len(token)
    for i in range(0,l+1-n):
        t = token[i:i+n]
        if h:
            t = myhash(t,mod)
#        if not d.has_key(t):
#            print t
        d[0,t] = 1
        
def abbrev(token,d,N,mod=20000,h=True):
    m=mod
    small = token
    count = 0
    abbrev = ''
    r = re.compile("\![a-z]")
    match = re.search(r,token)
    while match :
        count = match.start()+1
        abbrev+=small[count]
        small = small[count:]
        match = re.search(r,small)
    if not abbrev == '':
        abbrev='!'+abbrev+'!'
        for i in range(2,N):
            if h:
                nGrams(abbrev,i,d,mod=m,h=True)
            else:
                nGrams(abbrev,i,d,mod=m)
        
        
def toVector(token,empty={},mod=20000,N=3,h=True):
    m=mod
    #t1 = time.time()
    if h:
        d=np.zeros((1,mod))
    else:
        d = empty.copy()
        
    t = processToken(token)
    abbrev(t,d,N,h=h,mod=m)
    for i in range(1,N+1):
        if h:
            nGrams(t,i,d,mod=m,h=True)
        else:
            nGrams(t,i,d,mod=m)
    #print time.time() - t1
    return d[0]
        

def main():        
        
    n = 4
    empty = createDict(h=False)


    emptyh1 = createDict()

    emptyh2 = createDict(N=n)
    stop=raw_input("")
    query = "hello.  This, above all else, is important and must be remembered"
    wordlist = ["aardvark","hello","hellow","kitten","hallow","this above all","hallow","smitty Werbenjagermanjensen"]
    

    q = toVector(query,empty)
    qh1 = toVector(query,emptyh1,h=True)
    qh2 = toVector(query,emptyh2,h=True,N=n)
    
    wl=[]
    wlh1 = []
    wlh2 = []
    for x in wordlist:
        
        wl.append(toVector(x,empty))
        
        wlh1.append(toVector(x,emptyh1,h=True))

        wlh2.append(toVector(x,emptyh2,h=True,N=n))
    wl = np.array(wl)

    print "dict no hash :"
    count =0
    print q
    for x in wl:
        print wordlist[count] + ":"
        score = ssd.cosine(q,x)
        print "\t" +str(score)
        count+=1

    print "dict with hash, N=3 :"
    count=0
    print qh1
    for x in wlh1:
        print wordlist[count] + ":"
        score = ssd.cosine(qh1,x)
        print "\t" +str(score)
        count+=1

    print "dict with hash, N=4 :" 
    count=0
    print qh2
    for x in wlh2:
        print wordlist[count] + ":"
        score = ssd.cosine(qh2,x)
        print "\t" +str(score)
        count+=1
if __name__ == "__main__":
    main()