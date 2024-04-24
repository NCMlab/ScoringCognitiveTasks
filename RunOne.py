#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 08:30:33 2023

@author: jasonsteffener
"""

from ScoreNeuroPsych import *

subid = '9903004'
Visid = '2023-04-12_08h55.41.468_V001'
AllInDataFolder = '/Users/jasonsteffener/Documents/GitHub/Site02Data'

Results = LoadRawData(os.path.join(AllInDataFolder, subid, Visid),subid)
FlatResults = ProcessBehavioralFunctions.FlattenDict(Results)
                # add subid and visitid
FlatResults['subid'] = subid
        # FlatResults['AAVisid'] = Visid
FlatResults['visitid'] = Visid
MakeSummarySheet.MakeSummaryPDF(FlatResults)

VisitFolder = os.path.join(AllInDataFolder, subid, Visid)
CapacityData = ReadFile(VisitFolder, subid, 'DMS_CAPACITY')    


VisitFolder = '/Volumes/GoogleDrive-112727170889491651292/My Drive/LabFiles/NCM002-MRIStudy/Data/NeuroPsych/RawData/2002030/2019_Nov_06_1304_V001'
subid = '2002030'
Data = ReadFile(VisitFolder, subid, 'VSTM_Block_BehRun1')

CapacityData = ReadFile(VisitFolder, subid, 'VSTM_CAPACITY')        
tempResults = ProcessNeuroPsychFunctions.ProcessVSTMBlockv2(Data, CapacityData)
Results['VSTMBeh1'] = Reorder_DMS_VSTM_Results(tempResults, 'VSTM')
print('\tVSTM loaded')    