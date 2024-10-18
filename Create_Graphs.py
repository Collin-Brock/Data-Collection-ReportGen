#Created by Collin Brockman 7/24/2023


#Defines Dependent Script Files
from init import path_out_graphs,WidthP,HeightP,Graphs_per_page,Page_header_height,Graph_height
from Create_Log import log

#Defines Needed Libraries
import matplotlib.pyplot as plt
import csv
import datetime
from pathlib import Path
import numpy as np

#Defines the needed defined values for the sheet
X_tick_spacing = 900 #In seconds determines how often the x tick marks are located


#This function is used to create graphs of the same format with diffrent data sets and labels
#Each call to the graph function is in a specific format
def CreateGraphs(csvfile):
#The plot definitions are the first thing that need to be set
#For each graphed plot set an arbitrary value (will need later) equal to an array of the format ['signal','Label','color',Average]
#Note signal must be the same as the excel column to be refrenced for more colors lookup matplotlib colors
#Note if Average = 1 an average line will be calculated and plotted
    TLTemp= ['','Ambient','tab:blue',1]
    motor_temp= ['','Motor','tab:orange',1]
    controller_temp= ['','Controller','tab:green',1]
    battery_temp= ['','Battery','tab:purple',1]
    electronics_temp= ['','Electronics','tab:cyan',1]
#Some line definitions don't refrence values and are lines used to show a graph value
#First set an arbitrary value (will need later) equal to an array of the format [value,'Label','color']
    C_Foldback= [1,'Controller Foldback','tab:red']
    B_Foldback= [1,'Battery Foldback','tab:olive']
#Now to call a graph to be made which will output as a png in the graphs folder
#Call Graph_Make() with the following parameters(csvfile,'signal',range,'unit',plot,a=line)
#Note csvfile come from main.py
#Note range can either be a range(minvalue,maxvalue,step) if either are ommited from the call it will default to min value = 0 and step = 1 call
#A np.arrage() call can be helpful if decimal point numbers are needed however it can only handle single decimal spaces in the current configuration
#Note a is completly arbitrary
    Graph_Make(csvfile,'', range(101),10,'°C',TLTemp,motor_temp,controller_temp,battery_temp,electronics_temp,a= C_Foldback,b= B_Foldback)
    Graph_Make(csvfile,'', range(71),10,'°C',TLTemp,battery_temp,electronics_temp,b= B_Foldback)
    Graph_Make(csvfile,'', range(101),10,'°C',TLTemp,motor_temp,controller_temp,a= C_Foldback)
    motor_speed = ['' , 'Motor rpm' , 'tab:blue' ,1]
    Target = [ 3600,'Target rpm','tab:olive' ]
    Graph_Make(csvfile,'', range(5001),500,'rpm',motor_speed,a =Target)
    HcellV = ['','Highest','tab:red',0]
    LcellV = ['','Lowest','tab:blue',0]
    MaxV = [4.2 , 'Max Voltage','tab:green']
    MinV = [3 , 'Min Voltage','tab:olive']
    Graph_Make(csvfile,'Cell Voltages',np.arange(2.8,4.5,.1),.2,'V',LcellV,HcellV,a=MaxV,b=MinV)
    motor_power = ['','Motor','tab:red',1]
    battery_power = ['','Battery','tab:blue',1]
    controller_power = ['','Controller','tab:green',1]
    Graph_Make(csvfile,'Power',range(-1000,4001),500,'W',motor_power,controller_power,battery_power)
    motor_current = ['','Motor','tab:red',1]
    battery_current = ['','Battery','tab:blue',1]
    controller_current = ['','Controller','tab:green',1]
    Graph_Make(csvfile,'Current',range(-24,101),10,'A',motor_current,controller_current,battery_current)

#This function is called with the above format and will create a graph with the same format and save the graph as a .png
def Graph_Make(csvfile,Title,Range_Y,Scale_Y,Units_Y,*args,**kwargs):
    #This section sets up the file as well as the other common figure formatting options for every graph
    Units_Y = ' ' + Units_Y
    csvfile_name = str((Path.as_posix(csvfile)).rsplit(sep = "/")[-1]).rsplit(sep = ".")[-2]
    Graph_Name = str(path_out_graphs) + '/' + csvfile_name  + ' ' + Title + '.png'
    fig, Plot = plt.subplots(figsize=(WidthP,Graph_height))
    Plot.grid('major',color = 'whitesmoke')
    Plot.set_title(Title, fontsize=14)
    Plot.margins(x=0)
    Plot.margins(y=0)
    time_stamps=trytofinddata('timestamps',csvfile)
    #This loop interates through every input in addition to the formatting inputs required
    #This will look for the data and if it is found add it to the figure with a plot
    #It also look uses the format of the call for each input including the label name of signal color and if a average plot is called
    for arg in args:
        Data = trytofinddata(arg[0],csvfile)
        if Data != 'N/A':
            M,=Plot.plot(time_stamps,Data,color=arg[2],label=arg[1],linewidth = 1)
            #The line before the average sets up the data by removing any zeros from the data and replacing them with a nan value which is not plotted
            Data[Data == 0] = np.nan
            average = np.nanmean(Data)
            #This is a call for setting up the average line with the label so that the average value is displayed
            if arg[3] == 1:
                A=Plot.axhline(average,color=arg[2],linestyle =':',label=(arg[1] + ' Average: ' + str(round(average,1)) +  Units_Y),linewidth = 0.5)
    #This function looks for any arguments inputted into the funtion which is why all of the special data uses a variable = call
    #It will create a horizontal line with the format given in the call for each argument
    for a in kwargs:
        CF=Plot.axhline(kwargs[a][0],color=kwargs[a][2],linestyle =':',label=(kwargs[a][1] + ' ' + str(kwargs[a][0]) + Units_Y),linewidth = 1.5)
    #In order to make the data more readable and customizably readable the tick marks and labels are created manually with the x and y ticks functions
    Plot.set_ylim(min(Range_Y),max(Range_Y))
    Plot.set_yticks(Create_Y_Ticks(Range_Y,Scale_Y,Units_Y)[0])
    Plot.set_yticklabels(Create_Y_Ticks(Range_Y,Scale_Y,Units_Y)[1])
    Plot.set_xticks(Create_X_Ticks(time_stamps)[0])
    Plot.set_xticklabels(Create_X_Ticks(time_stamps)[1])
    #This sets the labels for the plots to the labels from the manual creation function to an angle in the center of the tick mark
    for label in Plot.get_xticklabels(which='major'):
        label.set(rotation=45, horizontalalignment='center')
    #This function creates the legend in the bottom left corner
    #Legend Placement information in the matplotlib cheatsheets
    Plot.legend(loc='lower left',bbox_to_anchor = (1.1,0.1),fontsize = 'small')
    #Finally the figure is saved as a .png and logged
    plt.savefig(Graph_Name,bbox_inches ='tight')
    plt.close()
    log('Created Graph', Graph_Name)

#This function defines the location and label for each of the X ticks
def Create_X_Ticks(time_stamps):
    xtickloc = []
    xticklab = []       
    #Finds the x ticks where the the value of the time_stamp divided by the X_tick_spacing has a remainder of zero ie is a multiple of
    for y in time_stamps:
        if round(y)%X_tick_spacing == 0:
            #Sets the location and label value
            xtickloc.append(y)
            xticklab.append(str(datetime.timedelta(seconds = y)))
    #This function determines if the last tick mark would interfere with the tick mark at the last point in the data
    #If the tick mark would interfere with a tick mark at the last point in the data it is ommitted
    #This interference check is set at 300 seconds or 10 minutes
    #If the only other timestamp is at 0 then the interference check is skipped and both ticks are used
    if (time_stamps[-1] < xtickloc[-1] + 300) and (time_stamps[0] != xtickloc[-1]):
        xtickloc[-1] = (time_stamps[-1])
        xticklab[-1] = (str(datetime.timedelta(seconds = time_stamps[-1])))
    else:
        xtickloc.append(time_stamps[-1])
        xticklab.append(str(datetime.timedelta(seconds = time_stamps[-1])))
    return xtickloc,xticklab

#This function defines the location and label for each of the Y ticks
def Create_Y_Ticks(Range_Y,Scale_Y,Unit):  
    ytickloc = []
    yticklab = []
    #Finds the tick marks for the range and scale from the given input in the original call
    #10 multiplier creates functionality for ranges with a tenths place to avoid floating point number issues
    for y in Range_Y:
        #Makes sure the range is only to the tenths place
        if y is not int:  
            y = round(y,1)
        if round(y*10)%round(Scale_Y*10) == 0:
            ytickloc.append(y)
            yticklab.append(str(y) + Unit)
    return ytickloc,yticklab

#This function tries to find the indexed data within the finished excel sheet
#If the indexed data is not found a 'N/A' is returned
def trytofinddata(signal_name,csvfile):
    with open(csvfile) as sheet:
        x = []
        Read_Sheet = csv.DictReader(sheet, delimiter=',')
        try:
            for row in Read_Sheet:
                x.append(round(float(row[signal_name]),2))
        except:
            x = 'N/A'
        return x