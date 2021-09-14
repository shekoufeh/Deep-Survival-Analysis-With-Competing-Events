# -*- coding: utf-8 -*-
"""
Created on Fri Aug 13 16:48:09 2021

@author: gorizadeh
"""

# First create input data folders


import os
import shutil
import numpy as np
import pandas as pd
from os import walk

sep=os.sep

def read_txt(fname):
    data=np.loadtxt(fname,dtype=str,delimiter=' ')
    return data

def write_txt(fname,cnt):
    strCnt=[' '.join(r)+'\n' for r in cnt]
    with open(fname,'w') as f:
        f.writelines(strCnt)
        
def save_txt(fname,data):
    lines=[]
    for i in range(data.shape[0]):
        l=' '.join(data[i,:])+'\n'
        lines.append(l)
    
    with open(fname,'w') as f: 
        f.writelines(lines)

def trim_row(r):
    return [int(e.split(':')[0]) for e in r]

def change_format(mat):
    # drop column 2
    mat = np.delete(mat,1,axis=1)
    mat = [trim_row(r) for r in mat]
    return mat

def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

# create final directories
savePathNamesInput  = ["SYNTHETIC-ALL-DRAWN","SYNTHETIC-ALL-NOPREONEEVENT","SYNTHETIC-ALL-UNCENSORED"] 
savePathNamesTest   = ["drawn-input","uncens-input","nopreoneevent-input"]
for d in savePathNamesInput:
    create_dir(d)
for d in savePathNamesTest:
    create_dir(d)
    
lt=["imputed","no-imputation-signle-event","multi-event"] #drawn-sub-dist-hazard,no-preprocessing
path = "."+sep+"raw"+sep+"606585"+sep+"feateng"+sep

if(True):
    # Create data version with competing event time as censoring time  
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        break
    
    for fname in f:
        if(fname[:15]=='uncensored_test'):
            test=read_txt(path+fname)
            vald=read_txt(path+"uncensored_validation"+fname[15:])
            trin=read_txt(path+"uncensored_train"+fname[15:])
            
            test[np.where(test[:,0]=='2'),0]='0'
            vald[np.where(vald[:,0]=='2'),0]='0'
            trin[np.where(trin[:,0]=='2'),0]='0'
            
            
            write_txt(path+'noPreprocessOneEvent_test'+fname[15:],test)
            write_txt(path+'noPreprocessOneEvent_validation'+fname[15:],vald)
            write_txt(path+'noPreprocessOneEvent_train'+fname[15:],trin)
    
    
    for l in lt:
        savePath="."+sep+l+sep
        create_dir(savePath)
    
    f = []
    for (dirpath, dirnames, filenames) in walk(path):
        f.extend(filenames)
        break
    
    
    # Fix number of test and validation
    for fname in f:
        if(fname[:4] == 'test'):
           
            test=read_txt(path+fname)
            vald=read_txt(path+"validation"+fname[4:])
            
            gen=np.concatenate((vald,test))
            vald=gen[:5000,:]
            test=gen[5000:,:]
            save_txt(path+fname, test)
            save_txt(path+"validation"+fname[4:], vald)
            
            sp = '.'+sep+savePathNamesTest[0]+sep
            shutil.copy(path+fname, sp)
            shutil.copy(path+"validation"+fname[4:], sp)
            shutil.copy(path+"train"+fname[4:], sp)
            
        elif(fname[:15]=='uncensored_test'):
           
            test=read_txt(path+fname)
            vald=read_txt(path+"uncensored_validation"+fname[15:])
    
            gen=np.concatenate((vald,test))
            vald=gen[:5000,:]
            test=gen[5000:,:]
            
            save_txt(path+fname, test)
            save_txt(path+"uncensored_validation"+fname[15:], vald)
            
            sp = '.'+sep+savePathNamesTest[1]+sep
            shutil.copy(path+fname, sp)
            shutil.copy(path+"uncensored_validation"+fname[15:], sp)
            shutil.copy(path+"uncensored_train"+fname[15:], sp)
            
        elif(fname[:25]=='noPreprocessOneEvent_test'):
            
            test=read_txt(path+fname)
            vald=read_txt(path+"noPreprocessOneEvent_validation"+fname[25:])
    
            gen=np.concatenate((vald,test))
            vald=gen[:5000,:]
            test=gen[5000:,:]
            
            save_txt(path+fname, test)
            save_txt(path+"noPreprocessOneEvent_validation"+fname[25:], vald)
            
            sp = '.'+sep+savePathNamesTest[2]+sep
            shutil.copy(path+fname, sp)
            shutil.copy(path+"noPreprocessOneEvent_validation"+fname[25:], sp)
            shutil.copy(path+"noPreprocessOneEvent_train"+fname[25:], sp)
        
    # Add column names
    colNames= ["status", "x1", "x2", "x3", "x4", "time"]
    for fname in f:
        if (fname == 'featindex.txt' or fname=='uncensored_featindex.txt' or fname==".gitignore"):
            continue
        
        newForm=change_format(read_txt(path+fname))
        newData=pd.DataFrame(newForm,columns=colNames)
        
        savePath = "."+sep+lt[0]+sep 
        if(fname[:10]=="uncensored"):
            savePath = "."+sep+lt[1]+sep
        elif(fname[:20]=="noPreprocessOneEvent"):
            savePath = "."+sep+lt[2]+sep
            
        # Save
        newData.to_csv(savePath+fname[:-4]+".csv",index=False)


# Put trainn validation and test datasets together
for i in range(3):
    source = lt[i]
    dest   = savePathNamesInput[i]

    f = []
    for (dirpath, dirnames, filenames) in walk(source):
        f.extend(filenames)
        break
    
    sortedF=sorted(f)
    numOfDataSets=int(len(sortedF)/3)
    path ='.'+sep+source+sep
    #savePath = 'C:\\Users\\gorizadeh\\Desktop\\a\\'+sep+dest+sep
    for i in range(numOfDataSets):
        testname =sortedF[i]
        trainname=sortedF[numOfDataSets+i]
        validname=sortedF[numOfDataSets*2+i]
        print(testname)
        print(trainname)
        print(validname)
        # get train/test/validation subjects
        dataTrn=pd.read_csv(path+trainname,sep=",")
        dataTst=pd.read_csv(path+testname,sep=",")
        dataVld=pd.read_csv(path+validname,sep=",")
    
    
        # Stack three set on top of each other train/validation/test
        speciallySortedData=dataTrn.append(dataVld,ignore_index=True)
        speciallySortedData=speciallySortedData.append(dataTst,ignore_index=True)
    
        print(dataTrn.shape)
        print(dataVld.shape)
        print(dataTst.shape)
    
        # Rename columns and drop unimportant data
        finData=speciallySortedData.rename(columns={"status": "label"})
    
        # bring time and label to front. 
        # finData=finData.drop(columns=['Unnamed: 0'])
        finData=finData.reindex(columns=['time', 'label', 'x1', 'x2', 'x3', 'x4'])
        savename = ""
        if testname[:4] == 'test':
            savename = testname[5:]
        elif testname[:15] == 'uncensored_test':
            savename =  testname[:11]+testname[16:]
        elif testname[:25] == 'noPreprocessOneEvent_test':  
            savename =  testname[:21]+testname[26:]
       # savename=testname[5:] if testname[:4]=='test' else testname[:11]+testname[16:]
        
        create_dir(savePath+savename[:-4]+sep)
        print(finData.shape)
        print(savePath+savename[:-4]+sep+savename)
        # Write final CSV file
        finData.to_csv(savePath+savename[:-4]+sep+savename,index=False)
    
    
    
    
    
