#Created by Collin Brockman 7/24/2023

#Main file used to call all other script files functions

#Defines Dependent Script Files
from init import path_out_excel_files,path_out_graphs

#Defines Dependent Script Files
from mdf_to_csv import run_mdf_to_cvs
from PDF_Creator import PDF_Report_Start,PDF_Add_Page, PDF_Finish
from Create_Graphs import CreateGraphs
from Excel_Math import Do_Math
from Create_Log import first_log
from Create_Log import log

#Defines Needed Libraries 
from pathlib import Path
import os


#Function to Run the script turning any .MF4 files into a pdf report 
#Naming convention of the files outputs are Folder>Folder or Folder>File or File depending on what is input
def run():
    #Starts the log file located in the outfolder in order to log actions of the Script for debugging Create_Log.py
    #Log calls are log('string','string2',.....) it will concatenate each input and add the time logged
    first_log()
    #Creates an folder for the excel files and graphs if they are not there
    try:
        os.makedirs(path_out_excel_files)
    except:
        log('Excel Files Folder Already Exists!')
    try:
        os.makedirs(path_out_graphs)
    except:
        log('Graphs Folder Already Exists!')
    #Starts the PDF report PDF_Creator.py
    #Note PDFs are held in MEMORY until the PDF Finish is called not a problem unless PDF size in the gigabytes
    #Note2 all PDF operations are increadbly slow compared to all other functions and calls (Thanks FPDF)
    pdf = PDF_Report_Start()
    #Creates cvs files from MF4 files
    #Houses the names for all signals it will search for    
    run_mdf_to_cvs()
    #Runs for each _Before.cvs file in the excel folder
    for csvfile in list(path_out_excel_files.glob('*')):
        if '.csv' in csvfile.suffix and (str(csvfile)).rsplit(sep = "_",maxsplit=1)[1] == 'Before.csv':
            new_csvfile = Path(str((Path.as_posix(csvfile)).rsplit(sep = "_",maxsplit=1)[0])+'.csv')
            #Creates columns for power information Excel_Math.py
            #Also called by PDF_Creator.py to find Max Values and State of Charge Value
            Do_Math(csvfile,new_csvfile)
            #Creates .png graphs as called in the CreateGraphs function Create_Graphs.py
            CreateGraphs(new_csvfile)
            #Adds 2 Pages of graphs and information for each input file
            PDF_Add_Page(pdf,new_csvfile)
    #Finishes PDF and Saves it to Output file
    #Note Extremely Slow 30s +
    PDF_Finish(pdf)

#Debugging Functions
def runpdf():
    pdf = PDF_Report_Start()
    for csvfile in list(path_out_excel_files.glob('*')):
            PDF_Add_Page(pdf,csvfile)
    PDF_Finish(pdf)
def rungraph():
    for csvfile in list(path_out_excel_files.glob('*')):
            CreateGraphs(csvfile)


run()