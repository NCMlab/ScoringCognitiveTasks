
''' Score all'''
import os
import sys
import datetime
import glob
import pandas as pd

# What folder is this file in?
# dir_path = os.path.dirname(os.path.realpath(__file__))
dir_path = '/Users/jasonsteffener/Documents/GitHub/ScoringCognitiveTasks'
# This will load the config file containing the location of the data folder
# If there is an error it means that the GUI program has not been run.
# The GUI checks to see if thie config file exists. If it does not then it is created.
print(dir_path)
print(dir_path)
# This is expecting this repo to sit next to the repo with the task code
sys.path.append(os.path.join(dir_path, '..','CognitiveTasks','ConfigFiles'))
sys.path.append(os.path.join(dir_path, 'code'))

import NeuropsychDataFolder
import ScoreNeuroPsych
import ScoreFMRIBehavior
import ScoreSurveyMonkey_NCM002



# Load up the data location as a global variable
AllInDataFolder = NeuropsychDataFolder.NeuropsychDataFolder
# Where to put the summary data
AllOutDataFolder = os.path.join(os.path.split(AllInDataFolder)[0], 'SummaryData')

BaseFileName = 'NCM_Master_'
# What files exist with this name?
Files = glob.glob(os.path.join(AllOutDataFolder, BaseFileName + '*.csv'))
now = datetime.datetime.now()
NowString = now.strftime("_updated_%b-%d-%Y_%H-%M.csv")
NewOutFileName = BaseFileName + NowString
if len(Files) == 0:
    FileName = os.path.join(AllOutDataFolder, NewOutFileName)
else:
    # this will open an existing file
    FileName = Files[-1] 


# Score NP Data
NPData = ScoreNeuroPsych.main()
# Save NP Data
NewOutFileName = BaseFileName + 'NPBeh' + NowString
FileName = os.path.join(AllOutDataFolder, NewOutFileName)
NPData.to_csv(FileName)



# Score fMRI data
FMRIData = ScoreFMRIBehavior.main()
# Save fMRI data
NewOutFileName = BaseFileName + 'NPfMRI' + NowString
FileName = os.path.join(AllOutDataFolder, NewOutFileName)
FMRIData.to_csv(FileName)

# Score Survey Monkey Data
LifeData, DemogData, PANASData = ScoreSurveyMonkey_NCM002.main()

# Save Survey Monkey data
NewOutFileName = BaseFileName + 'Questionnaires' + NowString
FileName = os.path.join(AllOutDataFolder, NewOutFileName)
LifeData.AllLife.to_csv(FileName)
NewOutFileName = BaseFileName + 'PANAS' + NowString
FileName = os.path.join(AllOutDataFolder, NewOutFileName)
PANASData.AllPANAS.to_csv(FileName)
NewOutFileName = BaseFileName + 'Demog' + NowString
FileName = os.path.join(AllOutDataFolder, NewOutFileName)
DemogData.AllParts.to_csv(FileName)

# Merge all files together
MM01 = pd.merge(left = DemogData.AllParts, right = LifeData.AllLife, how = 'outer', left_on='PartID',right_on='PartID')
MM02 = pd.merge(left = MM01, right = PANASData.AllPANAS, how = 'outer', left_on='PartID', right_on = 'PartID')
# Fix type of part id
NPData['AAsubid'] = NPData['AAsubid'].astype('int64')
MM03 = pd.merge(left = MM02, right = NPData, how = 'outer', left_on='PartID', right_on = 'AAsubid')
FMRIData['AAsubid'] = FMRIData['AAsubid'].astype('int64')
MM04 = pd.merge(left = MM03, right = FMRIData, how = 'outer', left_on='PartID', right_on = 'AAsubid')
# Save

NewOutFileName = BaseFileName + 'All' + NowString
FileName = os.path.join(AllOutDataFolder, NewOutFileName)
MM04.to_csv(FileName)
