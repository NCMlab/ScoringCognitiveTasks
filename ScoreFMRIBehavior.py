"""
Use this scoring program in other programs as:
    
    import ScoreNeuroPsych
    ScoreNeuroPsych.ScoreAll()
    
    This could be added to the end of the GUI program, so that when the GUI is closed
    the data os scored and updated.

"""
import os
import sys
import fnmatch
import shutil
import pandas as pd
import numpy as np
import glob
import datetime
import collections

# What folder is this file in?
dir_path = os.path.dirname(os.path.realpath(__file__))
Task_path =  '/Users/jasonsteffener/Documents/GitHub/CognitiveTasks'
# This will load the config file containing the location of the data folder
# If there is an error it means that the GUI program has not been run.
# The GUI checks to see if thie config file exists. If it does not then it is created.
print(dir_path)
sys.path.append(os.path.join(Task_path,'ConfigFiles'))
#sys.path.append(os.path.join(dir_path, '..','CognitiveTasks','ConfigFiles'))
sys.path.append(os.path.join(dir_path, 'code'))
import ProcessNeuroPsychFunctions
import ProcessBehavioralFunctions
import ScoreNeuroPsych
import NeuropsychDataFolder
# Load up the data location as a global variable
AllInDataFolder = NeuropsychDataFolder.NeuropsychDataFolder
# Where to put the summary data
AllOutDataFolder = os.path.join(os.path.split(AllInDataFolder)[0])

def main():
    # Cycle over all data folders and load them up
    NewData = CycleOverDataFolders()
    # find the name of the existing results file
    ExistingDataFileName = LocateOutDataFile()
    # Load the existing results file
    if os.path.exists(ExistingDataFileName):
        # Found the existing data file
        OldData = LoadOutDataFile(ExistingDataFileName)
        # created an updated results datafram, respectivein the "locked down" 
        # data rows
        UpdatedData = CreateUpdatedDataFrameOfResults(NewData, OldData)
        # Create an updated output file name
        UpdatedDataFileName = CreateOutFileName()
        # write out the updated data and move the old data file
        WriteOutNewdataMoveOldData(UpdatedData, UpdatedDataFileName, ExistingDataFileName)
    else:
        # There is no old data file
        OldData = []
        NewData.to_csv(ExistingDataFileName, index = False, float_format='%.3f')        
    return NewData 
    
def CycleOverDataFolders():
    # Take as input the folder that contains folders of data
    #cycle over folders
    # Enter each folder and identify the visit folders in them. 
    # These start with the letter V
    df = pd.DataFrame()
    ListOfDict = []
    # get all sub dirs
    subdirs = glob.glob(os.path.join(AllInDataFolder,'*/'))
    for subdir in subdirs:
        # check subdir based on some criteria
        CurDir = os.path.split(subdir)[0]
        CurDir = os.path.split(CurDir)[-1]
        if CurDir.isdigit() and CurDir[0] != '9':
            #enter the directory and find visit folders

            VisitFolders = glob.glob(os.path.join(subdir,'*/'))
            # What if there are no visit folders?
            # Then define teh visit as V001 and use a filename to idetify the visitid
            # Check to see if there is a visiti folder in the subject folder and if there is 
            # no visit folder, check to see if there are data files
            if (len(VisitFolders) > 0): 
                for visFold in VisitFolders:
                    CurVis = os.path.split(visFold)[0]
                    CurVis = os.path.split(CurVis)[-1]
                    if CurVis[-4:-2] == 'V0':
                        # From the directory structre extract the subject ID and the visit ID
                        subid = CurDir
                        Visid = CurVis
                        print('%s, %s'%(subid, Visid))
                        # Load up the raw data from the files in the visit folder
                        Results = LoadRawData(os.path.join(AllInDataFolder, subid, Visid),subid)
                        # Only add results if results are found to avoid a file with lots of empty rows
                        if len(Results) > 0:
                            FlatResults = FlattenDict(Results)
                            # add subid and visitid
                            FlatResults['AAsubid'] = subid
                            FlatResults['AAVisid'] = Visid
                            FlatResults['AAChecked'] = 0
                            ListOfDict.append(FlatResults)
            elif len(os.listdir(subdir)) > 0:
                # This seems to be data in a subject folder with no visit folder
                # Create the visit ID
                subid = CurDir
                Visid = FindVisitIDFromFileNames(subdir)
                
                # Load up the raw data from the files in the visit folder
                Results = LoadRawData(os.path.join(AllInDataFolder, subid),subid)
                FlatResults = FlattenDict(Results)
                # add subid and visitid
                FlatResults['AAsubid'] = subid
                FlatResults['AAVisid'] = Visid
                FlatResults['AAChecked'] = 0
                ListOfDict.append(FlatResults)
                
    df = pd.DataFrame(ListOfDict)
    return df

def FindVisitIDFromFileNames(subdir):
    # Make a list of the files in the folder
    ListOfFiles = glob.glob(os.path.join(subdir,'*.csv'))
    # Find the date and time stamps encoded in teh file names
    for filePath in ListOfFiles:
        Visid = ProcessBehavioralFunctions.ParseFileNamesForDateTime(filePath)
        break
    return Visid

    

def LoadRawData(VisitFolder, subid):
    # Given a visit folder, check for the existance of specific files
    # read the file and process teh results
    # This function looks for very specific files
    
    print('working on %s'%(subid))
    Results = collections.OrderedDict()
    
        
    # DMS
    Data1 = ReadFile(VisitFolder, subid, 'DMS_Block_MRIRun1')
    if len(Data1) > 0:        
        try:
            CapacityData = ReadFile(VisitFolder, subid, 'DMS_CAPACITY')    
            Data1 = ProcessNeuroPsychFunctions.CheckDMSDataFrameForLoad(Data1)
            tempResults = ProcessNeuroPsychFunctions.ProcessDMSBlockv2(Data1, CapacityData)
            Results['DMSMRI1'] = ScoreNeuroPsych.Reorder_DMS_VSTM_Results(tempResults, 'DMS')    
            print('\tDMS loaded')
        except:
            pass
            
          
    Data2 = ReadFile(VisitFolder, subid, 'DMS_Block_MRIRun2')
    if len(Data2) > 0:
        try:
            CapacityData = ReadFile(VisitFolder, subid, 'DMS_CAPACITY')    
            Data2 = ProcessNeuroPsychFunctions.CheckDMSDataFrameForLoad(Data2)
            tempResults = ProcessNeuroPsychFunctions.ProcessDMSBlockv2(Data2, CapacityData)
            Results['DMSMRI2'] = ScoreNeuroPsych.Reorder_DMS_VSTM_Results(tempResults, 'DMS')    
            print('\tDMS loaded')
        except:
            pass

    if len(Data1) > 0 and len(Data2) > 0: 
        AllData = Data1.append(Data2)
        if len(AllData) > 0:
            try:
                CapacityData = ReadFile(VisitFolder, subid, 'DMS_CAPACITY')    
                AllData = ProcessNeuroPsychFunctions.CheckDMSDataFrameForLoad(AllData)
                tempResults = ProcessNeuroPsychFunctions.ProcessDMSBlockv2(AllData, CapacityData)
                Results['DMSMRIAll'] = ScoreNeuroPsych.Reorder_DMS_VSTM_Results(tempResults, 'DMS')    
                print('\tBoth DMS loaded')
            except:
                pass
                
    # VSTM
    VSTMData1 = ReadFile(VisitFolder, subid, 'VSTM_Block_MRIRun1')
    if len(VSTMData1) > 0:
        try:
            CapacityData = ReadFile(VisitFolder, subid, 'VSTM_CAPACITY')            
            tempResults = ProcessNeuroPsychFunctions.ProcessVSTMBlockv2(VSTMData1, CapacityData)
            Results['VSTMMRI1'] = ScoreNeuroPsych.Reorder_DMS_VSTM_Results(tempResults, 'VSTM')   
            print('\tVSTM loaded')   
        except:
            pass

    VSTMData2 = ReadFile(VisitFolder, subid, 'VSTM_Block_MRIRun2')
    if len(VSTMData2) > 0:
        try:
            CapacityData = ReadFile(VisitFolder, subid, 'VSTM_CAPACITY')            
            tempResults = ProcessNeuroPsychFunctions.ProcessVSTMBlockv2(VSTMData2, CapacityData)
            Results['VSTMMRI2'] = ScoreNeuroPsych.Reorder_DMS_VSTM_Results(tempResults, 'VSTM')   
            print('\tVSTM loaded') 
        except:
            pass

    if len(VSTMData1) > 0 and len(VSTMData2) > 0: 
        VSTMAllData = VSTMData1.append(VSTMData2)
        if len(VSTMAllData) > 0:
            try:
                tempResults = ProcessNeuroPsychFunctions.ProcessVSTMBlockv2(VSTMAllData, CapacityData)
                Results['VSTMMRIAll'] = ScoreNeuroPsych.Reorder_DMS_VSTM_Results(tempResults, 'VSTM')   
                print('\tVBoth VSTM loaded')    
            except:
                pass
                            
    # N-Back
    Data1 = ReadFile(VisitFolder, subid, 'NBack_012012_MRIRun01')
    if len(Data1) > 0:
        Results['NBackMRI1'] = ProcessNeuroPsychFunctions.ProcessNBack(Data1)
        print('\tN-Back loaded')    
    Data2 = ReadFile(VisitFolder, subid, 'NBack_012012_MRIRun02')
    if len(Data2) > 0:
        Results['NBackMRI2'] = ProcessNeuroPsychFunctions.ProcessNBack(Data2)
        print('\tN-Back loaded')    
    if len(Data1) > 0 and len(Data2) > 0:     
        AllData = Data1.append(Data2)
        if len(AllData) > 0:
            Results['NBackMRIAll'] = ProcessNeuroPsychFunctions.ProcessNBack(AllData)
            print('\tBoth N-Back loaded')    
        
       
#     Data = ReadFile(VisitFolder, subid, 'DMS_Block_MRIRun1')
#     Data = CheckDMSDataFrameForLoad(Data)
#     Results['DMSMRI1'] = ProcessDMSBlockv2(Data)
# 
#     Data = ReadFile(VisitFolder, subid, 'DMS_Block_MRIRun2')
#     Data = CheckDMSDataFrameForLoad(Data)
#     Results['DMSMRI2'] = ProcessDMSBlockv2(Data)
# 
#     Data = ReadFile(VisitFolder, subid, 'DMS_Block_BehRun1')
#     Data = CheckDMSDataFrameForLoad(Data)
#     Results['DMSBeh1'] = ProcessDMSBlockv2(Data)
#     
    return Results

def ReadFile(VisitFolder, subid, TaskTag):
    # Find the file that matches the TaskTag
    # If multiple CSV files are found then the user is prompted to pick one.
    # Un selected files are renamed with XXX at their beginning.
    # The next time this program is run on this folder there will now only be one file 
    # available and the user will not be prompted again
    Data = []
    # List all files in the visit folder
    ll = os.listdir(VisitFolder)
    # create the string you are looking for which is a combo of the subid and the task name
    SearchString = subid + '_' + TaskTag
    matching = fnmatch.filter(ll,SearchString+'*.csv')
    # It is possible that there are multipel files with similar names.
    # The following asks the user for the correct one and then renames the others
    count = 1
    if len(matching) > 1:
        # There are more than one file!
        print('There are multiple files found for %s in folder: %s'%(SearchString, VisitFolder))
        for i in matching:
            # print the name and size of files
            SizeOfFile = np.round(os.stat(os.path.join(VisitFolder,matching[0])).st_size/1048)
            print('\t%d) %s, size = %0.0f kB'%(count, i,SizeOfFile))
            count += 1
        sel = input('Which one should be kept?  (Press return to skip) ')
        if len(sel) > 0:
            SelectedFile = matching[int(sel)-1]
            # Rename the unselected files so they will hopefully not be selected the next time!
            count = 1
            for i in matching:
                if not count == int(sel):
                    OutName = 'XXX_' + i
                    print(OutName)
                    shutil.move(os.path.join(VisitFolder,i), os.path.join(VisitFolder, OutName))
                count += 1    
        else:
            # If none of teh files are selected, rename them so they are not viewed again
            count = 1
            for i in matching:
                OutName = 'XXX_' + i
                print(OutName)
                shutil.move(os.path.join(VisitFolder,i), os.path.join(VisitFolder, OutName))
            SelectedFile = False
    elif len(matching) == 1:
        SelectedFile= matching[0]
    else:
        SelectedFile = False
        print('Did not find any files!!!')
    if SelectedFile != False:
        
        
        
        # Now open the file
        InputFile = os.path.join(VisitFolder, SelectedFile)
        # Read whole file into a dataframe
        # Note, in order for the data to be read as a dataframe all columns need to have headings.
        # If not an error is thrown
        # Check to see what size the file is to make sure it is not empty
        if os.stat(InputFile).st_size == 0:
            print('File is empty')
        else:
            Data = pd.read_csv(InputFile)
        # If the data is to be read into a big list use this:
        #    fid = open(InputFile, 'r')
        #    Data = csv.reader(fid)
        #    Data = list(Data)
    return Data

def FlattenDict(Results):
    # The process functions all return a dictionary of their results. 
    # In order to write these results to a CSV fuile the dictionaries need to be flattened first
    #
    # cycle over tasks
    # Use an ordered dictionary
    FlatResults = collections.OrderedDict()
    for i in Results.keys():
        for j in Results[i].keys():
            FlatResults['%s_%s'%(i,j)] = Results[i][j]
    return FlatResults    
    
def PutDataIntoOutputFile():
    # There will be a single output resultsvfile
    # it will have these columns:
    #   partID
    #   visitID, which will often be 1,2,3
    #   data checked, this cannot be changed by the program but only by a human
    #   data completeness flag
    #
    # 
    # First, the part id and visit id are read from the folder names.
    # Then the output data is checked to find this person. If found the data checked flag is TRUE
    # if yes, check to see if data is complete in out file. 
    # if not, then load all data and see if the missing data is now available
    df2 = pd.DataFrame.from_dict(FlatResults, orient='index')
    pass
        
def LoadOutDataFile(OutDataFilePathName):
    # Make a data frame from CSV file
    OutDF = pd.read_csv(OutDataFilePathName)
    return OutDF   
    
def CreateOutFileName():
    # Create a file to hold processed data using the time and date
    # to indicate when it was made
    BaseFileName = 'NCM_Master_MRI'
    now = datetime.datetime.now()
    NowString = now.strftime("_updated_%b-%d-%Y_%H-%M.csv")
    NewOutFileName = os.path.join(AllOutDataFolder, BaseFileName + NowString)
    return NewOutFileName
    
def LocateOutDataFile():
    # Locate an existing processed data file and if it does not exist, then make it.
    BaseFileName = 'NCM_Master_MRI'
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
    return FileName

def CreateUpdatedDataFrameOfResults(NewData, OldData):    
    # Create a dataframe to hold teh updated data
    OutDataFrame = pd.DataFrame()
    # Now cycle over each row and compare
    for index, NewRow in NewData.iterrows():
        # Add the new data
    
        NewDataSubId = NewRow['AAsubid']
        NewDataVisitId = NewRow['AAVisid']
        print(NewDataSubId)
        print(NewDataVisitId)
        # for each subid and visit found in the new data look for it in the old data
        # If the same subid/visitid is found in both check the Old data column 
        # labeled AAChecked to see if it is 1. If so then skip this data line in the new data 
        # and go onto the next one.
        
        # If the value is 0 in the old data file, then the data line has NOT been checked 
        # by a human and it is OK for this program to overwrite it.
        # Data is written out as follows:
        OldRow = OldData.loc[(OldData['AAsubid'] == int(NewDataSubId)) & (OldData['AAVisid'] == NewDataVisitId)] 
        
        if len(OldRow) > 0:
            # found this data in the exisiting data file
            # Check to see if the data has been checked by a human
            if int(OldRow['AAChecked']) == 1:
                # It has been checked
                # write temp to the out data file
                OutDataRow = OldRow
            else:
                # Data is in the out file but it has not been checked
                OutDataRow = NewRow
        else:
            # Did not find the new data in the old data file
            OutDataRow = NewRow
        # Add OutDataRow to the updated out dataframe
        OutDataFrame = OutDataFrame.append(OutDataRow)
    return OutDataFrame
   
def WriteOutNewdataMoveOldData(UpdatedData, UpdatedDataFileName, ExistingDataFileName):
    # Move the old file 
    OldDataFolder = os.path.join(AllOutDataFolder, 'OldResultFiles')
    # if the folder for old data does not exist, then make it
    if not os.path.exists(OldDataFolder):
        os.mkdir(OldDataFolder)
    # change the name of the results file so it is not confused with current data
    MovedDataFile = os.path.join(OldDataFolder, 'X_'+os.path.basename(ExistingDataFileName))
    shutil.move(ExistingDataFileName, MovedDataFile)
    # Now that the old data is moved, write out the updated data
    UpdatedData.to_csv(UpdatedDataFileName, index = False, float_format='%.3f')    
      
#       
if __name__ == "__main__":
    main()