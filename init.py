#Created by Collin Brockman 7/24/2023

#Defines Universally Globally needed information such as paths and varibles

#Defines Needed Libraries
from pathlib import Path
import os

#Sets all Universal Global Variables
Timescale = 1.0
WidthP = 8.5
HeightP = 11
Graphs_per_page = 4
Page_header_height = 20/25.4
Graph_height = (HeightP-Page_header_height)/Graphs_per_page

#Sets the File Names for the Input and Output Folder
input_folder = "!_IN_"
output_folder = "#_OUT_"
resources_folder = "ZZ Resources"
graphs_folder = 'Graphs'
excel_files_folder = 'Excel Files'
dbc_folder = "DBC"
log = ' Log File.txt'

#Sets Paths for Input and Output Folders
path = Path(os.path.dirname(os.path.dirname(__file__)))
path_in = Path(path, input_folder)
path_resources = Path(path,resources_folder)
path_out = Path(path, output_folder)
path_dbc = Path(path, dbc_folder)
path_out_excel_files = Path(path,output_folder,excel_files_folder)
path_out_log = Path(path_out,log)
path_out_graphs = Path(path,output_folder,graphs_folder)