

import os
import sys
import fnmatch
import shutil
import pandas as pd
import numpy as np
import glob
import datetime
import collections 
import ProcessNeuroPsychFunctions


import ProcessBehavioralFunctions
import ScoreFMRIBehavior
import ScoreNeuroPsych

dir_path = '/home/jsteffen/GitHub/CognitiveTasks/DataHandlingScripts'

# This will load the config file containing the location of the data folder
# If there is an error it means that the GUI program has not been run.
# The GUI checks to see if thie config file exists. If it does not then it is created.
print(dir_path)
sys.path.append(os.path.join(dir_path,'..','ConfigFiles'))
import NeuropsychDataFolder


# VisitFolder = '/Users/jasonsteffener/Dropbox/steffenercolumbia/Projects/MyProjects/NeuralCognitiveMapping/NeuroPsychData/990123454/2019_May_13_0930_V001'
subid = '2002010'
Visit = '2019_Aug_23_1718_V001'
VisitFolder = os.path.join(NeuropsychDataFolder.NeuropsychDataFolder, subid, Visit)

Data = ScoreNeuroPsych.ReadFile(VisitFolder, subid, 'VSTM_Block_MRIRun2')
ProcessNeuroPsychFunctions.ProcessVSTMBlockv2(Data,4)

