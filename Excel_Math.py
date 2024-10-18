#Created by Collin Brockman 7/24/2023


#Reads the xxxx_Before file then creates a xxxx file with appended power data also called by PDF_Creator.py to find critical values

#Defines Dependent Script Files
from Create_Log import log
from init import Timescale

#Defines Needed Libraries
import csv
import os

#First the labels are appended then as marked the file rewrites each line with appended data 
#This File Inputs the File Name and New File Name from main.py
def Append_Labels(csvfile,csvfile_new):
    read = open(csvfile,'r')
    write = open(csvfile_new,'w')
    reader = csv.reader(read)
    writer = csv.writer(write,delimiter=',',lineterminator = '\n')
    Labels = next(reader)
    #Here add a Labels.append to add a column with the given header
    #Ex. timestamps|...|Battery Power|Controller Power|SOC_Used.
    Labels.append('Battery Power')
    Labels.append('Controller Power')
    writer.writerow(Labels)
    read.close()
    return write,writer

def Do_Math(csvfile,csvfile_new):
    write,writer = Append_Labels(csvfile,csvfile_new)
    read = open(csvfile,'r')
    dict = csv.DictReader(read)
    row = []
    #This loop will iterate over every line of the xxx_Before file and write it into the new file along with adding data
    #The data added is the Power for the Battery and Controller
    #If any of the data needed to collect for power is missing it will fail and not output data
    try:
        for rdict in dict:
            rdict[''] = float(rdict['']) *-1
            row = list(rdict.values())
            row.append(float(rdict['']) * float(rdict['']))
            row.append(float(rdict['']) * float(rdict['']))
            writer.writerow(row)
        write.close()
        read.close()
        os.remove(csvfile)
    except:
        log('Power Column Creation Failed','Excel_Math.py>Do_Math')
        write.close()
        read.close()
        os.remove(csvfile_new)
        os.rename(csvfile,csvfile_new)

#Called by PDF_Creator.py finds nessisary critical values in finished excel file
def Info_Card(csvfile):
    #SOC Data to add to Title Block if 0 or Missing = N/A
    SOC_Data = trytofinddata('',csvfile)
    if SOC_Data != 'N/A' and round(max(SOC_Data)) != 0:
        SOC_Used = round(max(SOC_Data)-min(SOC_Data))
    else:
        SOC_Used = 'N/A'
    #Battery Used Calculation to add to the Title Block if Missing = N/A
    Battery_kwh_Used = []
    Battery_Power_Data = trytofinddata('Battery Power',csvfile)
    if Battery_Power_Data != 'N/A':
        for x in Battery_Power_Data:
            Battery_kwh_Used.append(x * Timescale/3600)
        Battery_kwh_Used = sum(Battery_kwh_Used)/1000
        Battery_kwh_Used = str(round(Battery_kwh_Used,3))
    else:
        Battery_kwh_Used = 'N/A'
    #Controller Over Temp Warning to add to Title Block if Missing = N/A if foldback not reached = blank
    Controller_Temp_Data = trytofinddata('',csvfile)
    if Controller_Temp_Data != 'N/A':
        Controller_Max  = max(Controller_Temp_Data)
        if Controller_Max >= 80.0:
            warn_controller_overtemp = 'Controller Overtemp'
        else:
            warn_controller_overtemp = ''
    else:
        warn_controller_overtemp = 'N/A'
    #Battery Over Temp Warning to add to Title Block if Missing = N/A if foldback not reached = blank
    Battery_Temp_Data = trytofinddata('',csvfile)
    if Battery_Temp_Data != 'N/A':
        Battery_Max = max(Battery_Temp_Data)
        if Battery_Max >= 55.0:
            warn_battery_overtemp = 'Battery Overtemp'
        else:
            warn_battery_overtemp = ''
    else:
        warn_battery_overtemp = 'N/A'
    return SOC_Used,warn_controller_overtemp,warn_battery_overtemp,Battery_kwh_Used

#This function is called to attempt to find data from the excel file
#If no data is found a 'N/A' is returned 
#Otherwise returns x where x is an array of every data value in column
def trytofinddata(signal_name,csvfile):
    with open(csvfile) as sheet:
        x = []
        Read_Sheet = csv.DictReader(sheet, delimiter=',')
        try:
            for row in Read_Sheet:
                x.append(round(float(row[signal_name]),1))
        except:
            x = 'N/A'
        return x