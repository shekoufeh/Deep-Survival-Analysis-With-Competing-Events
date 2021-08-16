# -*- coding: utf-8 -*-
"""
Created on Sun Apr 12 18:50:38 2020

@author: gorizadeh
"""
# Collect CIndex, Brier Scores
import os
import numpy as np

def read_file(fname):
    cnt=[]
    with open(fname,'r') as f:
        cnt=f.readlines()
    return cnt

def write_file(content,fname):
    with open(fname,'w') as f:
        f.writelines(content)
    
data_set='SYNTHETIC' # SYNTHETIC, CRASH2   
sep=os.sep
r='0.2' # 0.2,0.4,0.8
pathDrawn='..'+os.sep
pathUncen='..'+os.sep
pathInput='..'+os.sep

drawCindxPerTime=dict()
drawBrierPerTime=dict()
unceCindxPerTime=dict()
unceBrierPerTime=dict()

endng=['1','12','123','1234']
measures=['Brier Score (mean+std)','CIndex (mean+std)']
dataPreprocessing=[True,False] #iindicate is data is preprocessed or not
if(data_set=='CRASH2'):
    r='crash2'
    tlist=[]
    
    fsave=open('.'+sep+'crash2-cindex-brierscores.txt','w')
    lines=[]
    for m in measures:
        lines.append(m+'\n')
        l=""
        flag=True
        for p in dataPreprocessing:
            
            vlist=None
            j=0
            for e in endng:
                name=r+'_'+e if p else r+'_noprocessing_'+e
                path=pathDrawn if p else pathUncen
                fname='result_CINDEX_itr0.csv' if m[:6]=='CIndex' else 'result_BRIER_itr0.csv'
                # drawnName=r+'_'+e
                # uncenName=r+'_noprocessing_'+e
                vals=read_file(path+sep+name+sep+'results'+sep+fname)
                
                timePoints=vals[0].rstrip().split(',')[1:]
                tlist=timePoints
                
                v=np.asarray(vals[1].rstrip().split(',')[1:],dtype='float32')
                
                for i in range(len(timePoints)):
                    vlist=np.zeros((len(endng),len(v)),dtype='float32') if vlist is None else vlist
                    vlist[j,i]=v[i]
                
                j+=1
            tline='TimePoints    ,'+','.join(tlist)+'\n'
            l=    'One subnetwork,' if p else 'Mlt subnetwork,'
            
            means= np.round(np.mean(vlist,axis=0)*100,2) if m[:6]=='CIndex' else np.round(np.mean(vlist,axis=0),4)
            stdvs= np.round(np.std(vlist,axis=0)*100,2) if m[:6]=='CIndex' else np.round(np.std(vlist,axis=0),4)
            for k in range(means.shape[0]):
                l=l+str(means[k])+'+'+str(stdvs[k])+','
            l=l[:-1]
            l=l+'\n'
            if(flag):
                lines.append(tline)
            lines.append(l)
            flag=False
    fsave.writelines(lines)
    fsave.close()

if(data_set=='SYNTHETIC'):
    core='1_606585'
    
    tlist=[]
    
    fsave=open('.'+sep+r+'-synth-cindex-brierscores.txt','w')
    lines=[]
    for m in measures:
        lines.append(m+'\n')
        l=""
        flag=True
        for p in dataPreprocessing:
            
            vlist=None
            j=0
            for e in endng:
                name=r+'_'+core+'_'+e if p else 'uncensored_'+r+'_'+core+'_'+e
                path=pathDrawn if p else pathUncen
                fname='result_CINDEX_itr0.csv' if m[:6]=='CIndex' else 'result_BRIER_itr0.csv'
                # drawnName=r+'_'+e
                # uncenName=r+'_noprocessing_'+e
                vals=read_file(path+sep+name+sep+'results'+sep+fname)
                
                timePoints=vals[0].rstrip().split(',')[1:]
                tlist=timePoints
                
                v=np.asarray(vals[1].rstrip().split(',')[1:],dtype='float32')
                
                for i in range(len(timePoints)):
                    vlist=np.zeros((len(endng),len(v)),dtype='float32') if vlist is None else vlist
                    vlist[j,i]=v[i]
                
                j+=1
            tline='TimePoints    ,'+','.join(tlist)+'\n'
            l=    'One subnetwork,' if p else 'Mlt subnetwork,'
            
            means= np.round(np.mean(vlist,axis=0)*100,2) if m[:6]=='CIndex' else np.round(np.mean(vlist,axis=0),4)
            stdvs= np.round(np.std(vlist,axis=0)*100,2) if m[:6]=='CIndex' else np.round(np.std(vlist,axis=0),4)
            for k in range(means.shape[0]):
                l=l+str(means[k])+'+'+str(stdvs[k])+','
            l=l[:-1]
            l=l+'\n'
            if(flag):
                lines.append(tline)
            lines.append(l)
            flag=False
    fsave.writelines(lines)
    fsave.close()

    