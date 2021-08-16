# -*- coding: utf-8 -*-
"""
Created on Tue Jun 16 15:44:31 2020

@author: gorizadeh
"""

"""
Read in the overall average processing time /iteration of Deephit1 vs Deephit2
"""
import numpy as np

from os import listdir
from os.path import isfile, join

fpath = './time-iteration' #./

def read_content(fname):
    with open(join(fpath,fname),'r') as f:
        content=f.readlines()
        it=float(content[0])
        t=float(content[1])
    return it,t

files = [f for f in listdir(fpath) if isfile(join(fpath, f))]
dataName='0.8'#SEER,0.2,0.4,0.8,crash2

deephit1=dict({'iterations':list(),'time':list()})
deephit2=dict({'iterations':list(),'time':list()})


for f in files:
    if(f[-18:]!='time-iteration.txt'):
        continue
    if(dataName=='crash2'):
        if(f[:6]!='crash2'):
            continue
        nparts=f.split('_')
        if(len(nparts)==2): # DeepHit1, no imputation
            it,t=read_content(f)
            deephit1["iterations"].append(it)
            deephit1["time"].append(t)
        elif(len(nparts)==3 and nparts[1]=='noprocessing'): # Deephit2
            it,t=read_content(f)
            deephit2["iterations"].append(it)
            deephit2["time"].append(t)
    elif(dataName=='SEER'):
        if(f[:4]!='SEER'):
            continue
        nparts=f.split('_')
        if(len(nparts)==2): # DeepHit1, no imputation
            it,t=read_content(f)
            deephit1["iterations"].append(it)
            deephit1["time"].append(t)
        elif(len(nparts)==3 and nparts[1]=='noprocessing'): # Deephit2
            it,t=read_content(f)
            deephit2["iterations"].append(it)
            deephit2["time"].append(t)
    else:
        nparts=f.split('_')
        if(len(nparts)==4): # DeepHit1, no imputation
            it,t=read_content(f)
            deephit1["iterations"].append(it)
            deephit1["time"].append(t)
        elif(len(nparts)==5 and nparts[0]=='uncensored'): # Deephit2
            it,t=read_content(f)
            deephit2["iterations"].append(it)
            deephit2["time"].append(t)
            
print("For the data set:", dataName)
print("========== DeepHit 1 =========")
a1 = np.mean(np.asarray(deephit1["iterations"]))
b1 = np.mean(np.asarray(deephit1["time"]))
print("Average iteration num is:")
print(a1)
print("Average iteration time is:")
print(b1)
print("Total average time:",a1*b1)
print("========== DeepHit 2 =========")
a2 = np.mean(np.asarray(deephit2["iterations"]))
b2 = np.mean(np.asarray(deephit2["time"]))
print("Average iteration num is:")
print(a2)
print("Average iteration time is:")
print(b2)
print("Total average time:",a2*b2)