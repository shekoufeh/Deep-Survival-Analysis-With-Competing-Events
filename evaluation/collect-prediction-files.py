# -*- coding: utf-8 -*-
"""
Created on Mon Mar 30 12:21:09 2020

@author: gorizadeh
"""
import os

def read_file(fname):
    cnt=[]
    with open(fname,'r') as f:
        cnt=f.readlines()
    return cnt

def write_file(content,fname):
    with open(fname,'w') as f:
        f.writelines(content)
    
data_set='CRASH2bo' # SYNTHETIC, CRASH2   ,ICU, SEER, CRASH2bo, CRASH2da
sep=os.sep

pathDrawn='..'+os.sep
pathUncen='..'+os.sep
pathOneEvent='..'+os.sep
pathInput='..'+os.sep



endng=['1','12','123','1234','4123','5123','6123','7123','8123','9123']
if(data_set=='SEER'):
    r='SEER'
    for e in endng:
        drawnName=r+'_'+e
        uncenName=r+'_noprocessing_'+e
        oneeventName=r+'_noPreprocessOneEvent_'+e
        
        inputName='test_'+e
        inputNameUncens='noprocessing_test_'+e
        inputNameOneevent='noPreprocessOneEvent_test_'+e
        
        drawCnt=read_file(pathDrawn+sep+drawnName+sep+'results'+sep+'predictions-event-1.txt')
        unceCnt=read_file(pathUncen+sep+uncenName+sep+'results'+sep+'predictions-event-1.txt')
        oneeventCnt=read_file(pathOneEvent+sep+oneeventName+sep+'results'+sep+'predictions-event-1.txt')
     
        inptCnt=read_file(pathDrawn+sep+'SEER-test-files'+sep+'drawn-input'+sep+inputName+'.txt')
        inptUncsCnt=read_file(pathUncen+sep+'SEER-test-files'+sep+'uncens-input'+sep+inputNameUncens+'.txt')
        inptOneEventCnt=read_file(pathOneEvent+sep+'SEER-test-files'+sep+'nopreoneevent-input'+sep+inputNameOneevent+'.txt')
        
        write_file(drawCnt, '.'+sep+r+'-drawn-'+e+'.txt')
        write_file(unceCnt, '.'+sep+r+'-uncen-'+e+'.txt')
        write_file(oneeventCnt, '.'+sep+r+'-oneevent-'+e+'.txt')
        write_file(inptCnt, '.'+sep+r+'-input-'+e+'.txt')
        write_file(inptUncsCnt, '.'+sep+r+'-input-unc-'+e+'.txt')
        
if(data_set=='ICU'):
    r='ICU'
    for e in endng:
        drawnName=r+'_'+e
        uncenName=r+'_noprocessing_'+e
        oneeventName=r+'_noPreprocessOneEvent_'+e
        
        inputName='test_'+e
        inputNameUncens='noprocessing_test_'+e
        inputNameOneevent='noPreprocessOneEvent_test_'+e
        
        drawCnt=read_file(pathDrawn+sep+drawnName+sep+'results'+sep+'predictions-event-1.txt')
        unceCnt=read_file(pathUncen+sep+uncenName+sep+'results'+sep+'predictions-event-1.txt')
        oneeventCnt=read_file(pathOneEvent+sep+oneeventName+sep+'results'+sep+'predictions-event-1.txt')
     
        inptCnt=read_file(pathDrawn+sep+'ICU-test-files'+sep+'drawn-input'+sep+inputName+'.txt')
        inptUncsCnt=read_file(pathUncen+sep+'ICU-test-files'+sep+'uncens-input'+sep+inputNameUncens+'.txt')
        inptOneEventCnt=read_file(pathOneEvent+sep+'ICU-test-files'+sep+'nopreoneevent-input'+sep+inputNameOneevent+'.txt')
        
        write_file(drawCnt, '.'+sep+r+'-drawn-'+e+'.txt')
        write_file(unceCnt, '.'+sep+r+'-uncen-'+e+'.txt')
        write_file(oneeventCnt, '.'+sep+r+'-oneevent-'+e+'.txt')
        write_file(inptCnt, '.'+sep+r+'-input-'+e+'.txt')
        write_file(inptUncsCnt, '.'+sep+r+'-input-unc-'+e+'.txt')
        
if(data_set=='CRASH2'):
    r='crash2'
    for e in endng:
        drawnName=r+'_'+e
        uncenName=r+'_noprocessing_'+e
        oneeventName=r+'_noPreprocessOneEvent_'+e
        
        inputName='test_'+e
        inputNameUncens='noprocessing_test_'+e
        inputNameOneevent='noPreprocessOneEvent_test_'+e
        
        drawCnt=read_file(pathDrawn+sep+drawnName+sep+'results'+sep+'predictions-event-1.txt')
        unceCnt=read_file(pathUncen+sep+uncenName+sep+'results'+sep+'predictions-event-1.txt')
        oneeventCnt=read_file(pathOneEvent+sep+oneeventName+sep+'results'+sep+'predictions-event-1.txt')
     
        inptCnt=read_file(pathDrawn+sep+'CRASH2-test-files'+sep+'drawn-input'+sep+inputName+'.txt')
        inptUncsCnt=read_file(pathUncen+sep+'CRASH2-test-files'+sep+'uncens-input'+sep+inputNameUncens+'.txt')
        inptOneEventCnt=read_file(pathOneEvent+sep+'CRASH2-test-files'+sep+'nopreoneevent-input'+sep+inputNameOneevent+'.txt')
        
        write_file(drawCnt, '.'+sep+r+'-drawn-'+e+'.txt')
        write_file(unceCnt, '.'+sep+r+'-uncen-'+e+'.txt')
        write_file(oneeventCnt, '.'+sep+r+'-oneevent-'+e+'.txt')
        write_file(inptCnt, '.'+sep+r+'-input-'+e+'.txt')
        write_file(inptUncsCnt, '.'+sep+r+'-input-unc-'+e+'.txt')
        
if(data_set=='CRASH2bo'):
    r='crash2bo'
    for e in endng:
        drawnName=r+'_'+e
        uncenName=r+'_noprocessing_'+e
        oneeventName=r+'_noPreprocessOneEvent_'+e
        
        inputName='test_'+e
        inputNameUncens='noprocessing_test_'+e
        inputNameOneevent='noPreprocessOneEvent_test_'+e
        
        drawCnt=read_file(pathDrawn+sep+drawnName+sep+'results'+sep+'predictions-event-1.txt')
        unceCnt=read_file(pathUncen+sep+uncenName+sep+'results'+sep+'predictions-event-1.txt')
        oneeventCnt=read_file(pathOneEvent+sep+oneeventName+sep+'results'+sep+'predictions-event-1.txt')
     
        inptCnt=read_file(pathDrawn+sep+'CRASH2bo-test-files'+sep+'drawn-input'+sep+inputName+'.txt')
        inptUncsCnt=read_file(pathUncen+sep+'CRASH2bo-test-files'+sep+'uncens-input'+sep+inputNameUncens+'.txt')
        inptOneEventCnt=read_file(pathOneEvent+sep+'CRASH2bo-test-files'+sep+'nopreoneevent-input'+sep+inputNameOneevent+'.txt')
        
        write_file(drawCnt, '.'+sep+r+'-drawn-'+e+'.txt')
        write_file(unceCnt, '.'+sep+r+'-uncen-'+e+'.txt')
        write_file(oneeventCnt, '.'+sep+r+'-oneevent-'+e+'.txt')
        write_file(inptCnt, '.'+sep+r+'-input-'+e+'.txt')
        write_file(inptUncsCnt, '.'+sep+r+'-input-unc-'+e+'.txt')
        
if(data_set=='CRASH2da'):
    r='crash2da'
    for e in endng:
        drawnName=r+'_'+e
        uncenName=r+'_noprocessing_'+e
        oneeventName=r+'_noPreprocessOneEvent_'+e
        
        inputName='test_'+e
        inputNameUncens='noprocessing_test_'+e
        inputNameOneevent='noPreprocessOneEvent_test_'+e
        
        drawCnt=read_file(pathDrawn+sep+drawnName+sep+'results'+sep+'predictions-event-1.txt')
        unceCnt=read_file(pathUncen+sep+uncenName+sep+'results'+sep+'predictions-event-1.txt')
        oneeventCnt=read_file(pathOneEvent+sep+oneeventName+sep+'results'+sep+'predictions-event-1.txt')
     
        inptCnt=read_file(pathDrawn+sep+'CRASH2da-test-files'+sep+'drawn-input'+sep+inputName+'.txt')
        inptUncsCnt=read_file(pathUncen+sep+'CRASH2da-test-files'+sep+'uncens-input'+sep+inputNameUncens+'.txt')
        inptOneEventCnt=read_file(pathOneEvent+sep+'CRASH2da-test-files'+sep+'nopreoneevent-input'+sep+inputNameOneevent+'.txt')
        
        write_file(drawCnt, '.'+sep+r+'-drawn-'+e+'.txt')
        write_file(unceCnt, '.'+sep+r+'-uncen-'+e+'.txt')
        write_file(oneeventCnt, '.'+sep+r+'-oneevent-'+e+'.txt')
        write_file(inptCnt, '.'+sep+r+'-input-'+e+'.txt')
        write_file(inptUncsCnt, '.'+sep+r+'-input-unc-'+e+'.txt')
                                    
if(data_set=='SYNTHETIC'):
    core='1_606585'
    rates=['0.2','0.4','0.8']
    for r in rates:
        for e in endng:
            drawnName=r+'_'+core+'_'+e
            uncenName='uncensored_'+r+'_'+core+'_'+e
            oneeventName='noPreprocessOneEvent_'+r+'_'+core+'_'+e
            
            inputName='test_'+r+'_'+core+'_'+e
            inputNameUncens='uncensored_test_'+r+'_'+core+'_'+e
            inputNameOneevent='noPreprocessOneEvent_test_'+r+'_'+core+'_'+e
            
            drawCnt=read_file(pathDrawn+sep+drawnName+sep+'results'+sep+'predictions-event-1.txt')
            unceCnt=read_file(pathUncen+sep+uncenName+sep+'results'+sep+'predictions-event-1.txt')
            oneeventCnt=read_file(pathOneEvent+sep+oneeventName+sep+'results'+sep+'predictions-event-1.txt')
           
            inptCnt=read_file(pathUncen+sep+'SYNTH-test-files'+sep+'drawn-input'+sep+inputName+'.txt')
            inptUncsCnt=read_file(pathUncen+sep+'SYNTH-test-files'+sep+'uncens-input'+sep+inputNameUncens+'.txt')
            inptOneEventCnt=read_file(pathOneEvent+sep+'SYNTH-test-files'+sep+'nopreoneevent-input'+sep+inputNameOneevent+'.txt')
        
            write_file(drawCnt, '.'+sep+r+'-drawn-'+e+'.txt')
            write_file(unceCnt, '.'+sep+r+'-uncen-'+e+'.txt')
            write_file(oneeventCnt, '.'+sep+r+'-oneevent-'+e+'.txt')
            write_file(inptCnt, '.'+sep+r+'-input-'+e+'.txt')
            write_file(inptUncsCnt, '.'+sep+r+'-input-unc-'+e+'.txt')
            