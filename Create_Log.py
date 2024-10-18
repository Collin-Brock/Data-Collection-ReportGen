#Created by Collin Brockman 7/24/2023

#Creates Logs writes to log.txt file and terminal window

#Defines Dependent Script Files
from init import path_out_log,path
from datetime import datetime as now

#Defines Needed Libraries
import os

#Create a new log file or overwrites the current log file
def first_log():
    log = open(path_out_log,'w')
    log_file_begin = ('Script Launched at ' + str(now.now()).rsplit('.')[0] + ' from ' + str(path))
    log.write(log_file_begin)
    print(log_file_begin)
    log.close

#Creates a log entry
#Called as log('string','string2',....) which are concatonated into a group of lines in the form
#'string'
#' string2'.....
#' Time'
def log(Log,*args): 
    os.system('cls')
    log = open(path_out_log,'a')
    log.write('\n' + '\n' + str(Log) + '\n' )
    print(Log)
    for arg in args:
        log.write(' ' + str(arg) + '\n')
        print(' ' + str(arg))
    log.write(' ' + str(now.now()).rsplit('.')[0])
    print(' ' + str(now.now()).rsplit('.')[0])
    log.close