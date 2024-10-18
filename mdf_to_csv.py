#Created by Collin Brockman 7/24/2023


#Creates .csv files from raw can MF4 files

#Defines Dependent Script Files
from init import path_in,path_dbc,path_out_excel_files,Timescale
from Create_Log import log

#Defines Needed Libraries
from asammdf import MDF
import asammdf
from pathlib import Path
#Runs function to determine the input format
def run_mdf_to_cvs():
    Find_Date_Folders_IN()

#Look for named folders in the IN folder uses name for output
#If MF4 files are found they are sent to create cvs, output retains the file name
def Find_Date_Folders_IN():
    for x in path_in.glob('*'):
            if x.is_dir():
                Date = str(Path.as_posix(x)).rsplit(sep = "/")[-1]
                Find_Named_Folders_IN_Date(x,Date)
            else:
                Name = (str(Path.as_posix(x)).rsplit(sep = "/")[-1]).lstrip('0')
                if str(x).rsplit('.')[-1] == 'MF4':
                    Create_cvs(path_in,Name,'')

#Look for named folders in the named folder uses name for output
#If MF4 files are found they are sent to create cvs, output name is folder name  + file name
def Find_Named_Folders_IN_Date(x,Date):
    for y in x.glob('*'):
        if y.is_dir():
            Name = (str(Path.as_posix(y)).rsplit(sep = "/")[-1]).lstrip('0')
            Get_Files_from_Folder_IN_Date(y,Name,Date)
        else:
            Name = (str(Path.as_posix(y)).rsplit(sep = "/")[-1]).lstrip('0')
            if str(y).rsplit('.')[-1] == 'MF4':
                Create_cvs(x,Date,Name)

#Looks for files in the named folder in the named folder
#If more than one file is in this directory the files will be named: name of first folder , name of second folder , (#)
def Get_Files_from_Folder_IN_Date(y,Name,Date):
    i = 0
    for file in y.glob('*' + 'MF4'):
        if i != 0:
            Name = Name + '(' + str(i) + ')'
        Create_cvs(file,Name,Date)
        i += 1

#Creates cvs from the found MF4 files
def Create_cvs(file,Name,Date):
#Here is where the signals to be collected are defined
#The format for signals is a list of strings ['signal1','signal2']
#The list can be moved down by ending the line with a comma as shown
#Make sure the signal name is the same name as in the dbc file
#If the signal is not found it WILL NOT STOP the program and will be shown as Signal Not Found in the logs
    signals = ['']
    #interpolation set as linear interpolation
    MDF.configure(MDF,integer_interpolation = 1 ,float_interpolation = 1)
    #finds all dbc files in the dbc file folder
    dbc_files = {"CAN": [(dbc, 0) for dbc in list(path_dbc.glob("*" + ".DBC"))]}
    #Names the files first folder name, second folder name, _Before
    #Note the _Before will be removed in the Excel_Math.py call 
    cvs_name = Path(path_out_excel_files,Date+" "+Name+'_Before')
    mdf = asammdf.MDF(file)
    mdf = mdf.extract_bus_logging(dbc_files)
    #Searches to find any signals in signals that are not found after the extract bus logging and removes them from the filter
    to_remove = []
    for i in signals:
        try:
            mdf.filter([i])
        except:
            log(i + ' Not Found!' ,str(cvs_name))
            to_remove.append(i)
    for i in to_remove:
        signals.remove(i)
    #Filters the MF4 file with the signals in signal - signals not found after extracting the bus log
    mdf = mdf.filter(signals)
    #Exports the cvs file with a timescale defined in main
    mdf.export("csv", filename=cvs_name,time_from_zero=True,single_time_base=True,raster=Timescale,use_display_names = False,add_units = False)
    log('Export Success!',cvs_name)