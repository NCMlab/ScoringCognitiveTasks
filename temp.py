# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import os
import pickle
from ScoreStaircase import *

# file = '1002002_DMS_Stair_1_2019_May_31_1051.csv'

# file = '1002047/2019_Nov_18_1321_V001/1002047_DMS_Stair_1_2019_Nov_18_1352.csv'

BaseDir = '/Volumes/GoogleDrive/Shared drives/NCMLab/NCM002-MRIStudy/Data/NeuroPsych/RawData'
SearchString = 'DMS_Stair'
# Make a list of dictionaries
DataDict = []
# Find all files 

count = 0
for root, dirs, files in os.walk(BaseDir):
    for file in files:
    
        filename, file_extension = os.path.splitext(file)
        # Only look at CSV files
        if (file_extension == '.csv') and (file[0] != '9'):
            if file.find(SearchString) > 0:
                print(file)

                # Extract the Participant ID
                PartID = root.split('/')[9]
                # Read the file
                df = pd.read_csv(os.path.join(root,file))
                tempDict = {}
                tempDict['PartID'] = PartID
                tempDict['RawData'] = df
                Capacity, NTrials, NReversals, CC, CChigh, CClow, b0, b1 = ProcessStairCaseData(df)
                tempDict['RevCap'] = Capacity
                tempDict['NTrials'] = NTrials
                tempDict['NRev'] = NReversals
                tempDict['LogCap'] = CC
                tempDict['LogCapHi'] = CChigh
                tempDict['LogCapLow'] = CClow
                tempDict['b0'] = b0
                tempDict['b1'] = b1                
                RevCap2, RevCapStd, RevCapMax = FindReversals(df)
                tempDict['RevCap2'] = RevCap2
                tempDict['RevCapStd'] = RevCapStd
                tempDict['RevCapMax'] = RevCapMax
                DataDict.append(tempDict)      
                count += 1
print(count)
fid = open('DMSSTairCaseLogit.csv','w')
fid.write('PartID,NTrials,NRev,RevCap,LogCap,LogCapHi,LogCapLow,RevCap2,RevCapStd,RevCapMax,b0,b1\n')    
for i in DataDict:
    fid.write('%d,%d,%d,%0.4f,%0.4f,%0.4f,%0.4f,'%(int(i['PartID']),i['NTrials'],i['NRev'],i['RevCap'],i['LogCap'],i['LogCapHi'],i['LogCapLow']))
    fid.write('%0.4f,%0.4f,%0.4f,'%(i['RevCap2'],i['RevCapStd'],i['RevCapMax']))
    fid.write('%0.4f,%0.4f\n'%(i['b0'],i['b1']))
    print(i['PartID'])
fid.close()



# Save Data                
with open('saved_AllNCM002DMSStair.pkl', 'wb') as f:
    pickle.dump(DataDict, f)
# Load Data    
with open('saved_AllNCM002DMSStair.pkl', 'rb') as f:
    DataDict = pickle.load(f)    



SearchString = 'DigitSpan_For'

DSForDataDict = {}
# Find all files 

for root, dirs, files in os.walk(BaseDir):
    for file in files:
        filename, file_extension = os.path.splitext(file)
        # Only look at CSV files
        if file_extension == '.csv':
            if file.find(SearchString) > 0:
                print(file)

                # Extract the Participant ID
                PartID = root.split('/')[9]
                # Read the file
                df = pd.read_csv(os.path.join(root,file))
                DSForDataDict[PartID] = df

with open('saved_AllNCM002_DSB_Stair.pkl', 'wb') as f:
    pickle.dump(DSBackDataDict, f)
# Load Data    
with open('saved_AllNCM002_DSB_Stair.pkl', 'rb') as f:
    DataDict = pickle.load(f)    


for key in DSForDataDict:
    if key[0] != 'X' and key[0] != '9':
        df = DSForDataDict[key]
        # Load and clean the data in the staircase file
        Trial, Load = CleanDataBDS(df)
        bounds = ((0,0), (15,2))
        # Set initial paramaters
        p0e = [max(Load), 1]
        popt, pcov = curve_fit(exponetialModel, Trial, Load,p0e, bounds = bounds)
        x = np.linspace(0, 14, 14)
        y = exponetialModel(x, *popt)
        SDE = np.sqrt(np.diag(pcov))
        
        print('%s,%0.4f,%0.4f,%0.4f,%0.4f'%(key,popt[0],popt[1],SDE[0],SDE[1]))
        plt.plot(Trial, Load, 'o', label='data')
        plt.plot(x,y, label='fit')
        #plt.legend(loc='best')


for key in DataDict:
    if key[0] != 'X' and key[0] != '9':
        df = DataDict[key]
        # Load and clean the data in the staircase file
        Trial, Load = CleanDataDMS(df)
        bounds = ((0,0), (9,2))
        # Set initial paramaters
        p0e = [max(Load), 1]
        popt, pcov = curve_fit(exponetialModel, Trial, Load,p0e, bounds = bounds)
        x = np.linspace(0, 60, 60)
        y = exponetialModel(x, *popt)
        SDE = np.sqrt(np.diag(pcov))
        
        print('%s,%0.4f,%0.4f,%0.4f,%0.4f'%(key,popt[0],popt[1],SDE[0],SDE[1]))
        plt.plot(Trial, Load, 'o', label='data')
        plt.plot(x,y, label='fit')
        #plt.legend(loc='best')

def CleanDataBDS(DataFrameEntry):
    Trial = []
    Load = []
    count = 0
    for i in DataFrameEntry['Stairs.intensity']:
        try:
            Trial.append(np.int16(DataFrameEntry['Stairs.thisTrialN'][count]))
            k = np.int16(i)
            Load.append(k)
            count += 1
        except:
            pass
    if Trial[-1] == 0:
        Trial = Trial[0:-1]
    return Trial, Load

def CleanDataDMS(DataFrameEntry):
    Trial = []
    Load = []
    count = 0
    for i in DataFrameEntry['Load']:
        try:
            Trial.append(np.int16(DataFrameEntry['Trial'][count]))
            k = np.int16(i)
            Load.append(k)

            count += 1
        except:
            pass
    return Trial, Load

    
def AnalyzeOne(DataFraneEntry):
    Trial, Load = CleanDataDMS(DataFraneEntry)
    p0e = [max(Load), 1]
    bounds = ((0,0), (9,1))
    popt, pcov = curve_fit(exponetialModel, Trial, Load, p0e, method='dogbox',bounds=bounds )
    x = np.linspace(0, 60, 60)
    y = exponetialModel(x, *popt)    
    plt.plot(Trial, Load, 'o', label='data')
    plt.plot(x,y, label='fit')
    plt.legend(loc='best')
    print(popt)

        
def exponetialModel(x, L, k):
    y = L*(1 - np.exp(-k*x))
    return (y)    
        
def sigmoid3param(x, L ,x0, k):
    y = L / (1 + np.exp(-k*(x-x0)))
    return (y)

def WeibullCDF(x, L, k, b):
    y = L*(1 - np.exp(-(x/b)**k))
    return (y)

def sigmoid(x, L ,x0, k, b):
    y = L / (1 + np.exp(-k*(x-x0)))+b
    return (y)

p0 = [max(Load), np.median(Trial),1,min(Load)] # this is an mandatory initial guess
p03 = [max(Load), np.median(Trial),1] 

p0e = [max(Load), 1]
p0W = [max(Load), 1, 20]

# popt, pcov = curve_fit(sigmoid, Trial, Load,p0, method='dogbox')
# popt, pcov = curve_fit(exponetialModel, Trial, Load,p0e, method='dogbox')
popt, pcov = curve_fit(WeibullCDF, Trial, Load, p0W, method='lm',  maxfev=5000)



x = np.linspace(0, 60, 60)
y = WeibullCDF(x, 9, 1, 20)
y = WeibullCDF(x, *popt)

plt.plot(Trial, Load, 'o', label='data')
plt.plot(x,y, label='fit')
plt.legend(loc='best')

