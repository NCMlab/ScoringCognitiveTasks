import os
import importlib
import sys
import pandas as pd
import csv

import NCMPartv2
import ScoreNIHToolbox
importlib.reload(NCMPartv2)

BaseDir = '/home/jsteffen'
BaseDir = '/Users/jasonsteffener'
sys.path.append(os.path.join(BaseDir,'Documents','GitHub','CognitiveTasks','DataHandlingScripts'))


import DataHandlingScriptsPart1
importlib.reload(DataHandlingScriptsPart1)
import DataHandlingBehavioral
importlib.reload(DataHandlingBehavioral)

AllOutDataFolder = os.path.join(BaseDir, 'Dropbox/steffenercolumbia/Projects/MyProjects/NeuralCognitiveMapping/data/')

df = DataHandlingBehavioral.CycleOverBehDataFolders(AllOutDataFolder)

    
# Load the NIH data
dfNIH = ScoreNIHToolbox.Run()






inputFileName = [u'/Users/jasonsteffener/Dropbox/steffenercolumbia/Projects/MyProjects/NeuralCognitiveMapping/data/SurveyMonkeyExports/Participant Questionnaire.csv']
# open the file  
fid = open(inputFileName[0],'r', encoding="ISO-8859-1")

data = csv.reader(fid)
#data = pandas.read_csv(fid, sep=',', encoding='latin-1')
# Read whole file into a list
LL = list(data)
fid.close()

NPart = len(LL) - 2
HeaderLine1 = LL[0]
HeaderLine2 = LL[1]
PartData = LL[2:]
PartCount = 0
DataList = []
for i in PartData:
    print("=================================")
    # Skip rows that are test subjects
    if len(i[9]) == 8:
        if not i[9][5] == '9':
            try:
                # 14 has missing NIH data
                # 15 has missing block data
                # 16 has data that does not look good
                # Empty rows in the survey monkey file need to be removed
                part = NCMPartv2.NCMParticipant()
                part.MakeParticipant(i)
                #part.ReadBlockDataLong('DMS_Block','DMS',6)
                #part.ReadStairData('DMS')
                
                DataList.append(part)
#                print str(RowCount)+"     "+part.subid
                PartCount += 1
            except:
                print(str(PartCount)+"     "+part.subid)
                print("############# >>>>> Uhh Oh <<<<< ############")
                PartCount += 1
        else:
            print("Skipping: %s"%(i[9]))
            

# Map the psychopy ans SM data together
for i in DataList:
    SMsubid = i.subid
    dfLOC = find(df['AAsubid'] == SMsubid)
    df.loc[dfLOC,'eduSM'] = i.edu
    df.loc[dfLOC,'sex'] = i.sex
    df.loc[dfLOC,'BDIscore'] = i.BDIscore
    df.loc[dfLOC,'GDSscore'] = i.GDSscore
    df.loc[dfLOC,'FOSC'] = i.FOSC
    df.loc[dfLOC,'PAAerobic'] = i.PAAerobicMin
    df.loc[dfLOC,'PABicycling'] = i.PABicyclingMin
    df.loc[dfLOC,'PAJogging'] = i.PAJoggingMin
    df.loc[dfLOC,'PALapSwim'] = i.PALapSwimMin
    df.loc[dfLOC,'PALowIntensity'] = i.PALowIntensityMin
    df.loc[dfLOC,'PARunning'] = i.PARunningMin
    df.loc[dfLOC,'PATennis'] = i.PATennisMin
    df.loc[dfLOC,'PAWalkHike'] = i.PAWalkHikeMin
    

dfAll = df.merge(dfNIH, left_on='AAsubid', right_on='AAsubid', how='outer')

BaseFileName = 'NCM_BehavStudy_Tasks_NIH_SM'
now = datetime.datetime.now()
NowString = now.strftime("_updated_%b-%d-%Y_%H-%M.csv")
NewOutFileName = BaseFileName + NowString
OutFile = os.path.join(AllOutDataFolder, NewOutFileName)
dfAll.to_csv(OutFile)


# inputFileName = [u'/Users/jasonsteffener/Dropbox/steffenercolumbia/Projects/MyProjects/NeuralCognitiveMapping/data/SurveyMonkeyExports/Participant Questionnaire.csv']
# # open the file
# fid = open(inputFileName[0],'r', encoding="ISO-8859-1")
# 
# data = csv.reader(fid)
# data = pd.read_csv(fid, sep=',', encoding='latin-1')
# # 
# df = pd.read_csv(inputFileName[0], sep=',', encoding='latin-1')
# indices = [i for i, c in enumerate(df.columns) if not c.startswith('Unnamed')]
# questions = [c for c in df.columns if not c.startswith('Unnamed')]
# slices = [slice(i, j) for i, j in zip(indices, indices[1:] + [None])]
# for q in slices:
#     print(df.iloc[:, q])  # Use `display` if using Jupyter
# 
# def parse_response(s):
#     try:
#         return s[~s.isnull()][0]
#     except IndexError:
#         return np.nan
# 
# data = [df.iloc[:, q].apply(parse_response, axis=1)[1:] for q in slices]
# dfOUT = pd.concat(data, axis=1)
# dfOUT.columns = questions


####
