#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
The aim is to rescore the staircase data using logistic regression and compare 
it to the method of taking the average of the reversals

Created on Tue May  3 14:40:35 2022

@author: jasonsteffener
"""

import os
import pandas as pd 
import numpy as np
import statsmodels.api as sm
from LogitHelpers import *


# DirName = '/Volumes/GoogleDrive/Shared drives/NCMLab/NCM002-MRIStudy/Data/NeuroPsych/RawData/1002016/2019_Sep_18_1301_V001'
# FileName = '1002016_DMS_Stair_1_2019_Sep_18_1334.csv'

# # Read the file
# df = pd.read_csv(os.path.join(DirName, FileName))

def ProcessStairCaseData(RawData):
# Find the Capacity which is in the last row, third column
    Capacity = float(RawData.iloc[-1:]['LevelIndex'])
    NTrials = int(RawData.iloc[-1:]['Trial'])
    NReversals = int(RawData.iloc[-1:]['Load'])
    # Remove last three rows
    RawData.drop(RawData.tail(3).index,inplace=True) 
    # Extract the data
    # x1 = pd.DataFrame(RawData['Load'])
    # y1 = pd.DataFrame(df['Correct'])
    
    x2 = pd.DataFrame(RawData['Load']).astype('str').astype('int')
    # Add an intercept term
    exog = sm.add_constant(x2)
    y2 = pd.DataFrame(RawData['Correct']).astype('category')
    
    # Fit the regression model
    logit_model=sm.Logit(y2,exog)
    result = logit_model.fit()
    
    Thr = 0.8
    [CC, CChigh, CClow] = FindCap_CI(Thr, result.params[0], result.params[1], result.normalized_cov_params)
    
    return Capacity, NTrials, NReversals, CC, CChigh, CClow, result.params[0], result.params[1]

def FindReversals(RawData):
    UpFlag = 1
    DownFlag = 0
    Prev = 0
    RevCount = 0
    RevLoads = []
    for i in RawData['Load']:
        if int(i) > Prev:
            # Going up
            if DownFlag == 1:
                RevCount += 1
                RevLoads.append(int(i))
                UpFlag = 1
                DownFlag = 0
        if int(i) < Prev:
            # Going down
            if UpFlag == 1:
                RevCount += 1
                RevLoads.append(int(i))                
                DownFlag = 1
                UpFlag = 0
        Prev = int(i)
    #     print('%d\t%d\t%d'%(int(i),UpFlag,DownFlag))
    # print(RevCount)            
    return np.mean(RevLoads), np.std(RevLoads), np.max(RevLoads)
    
    