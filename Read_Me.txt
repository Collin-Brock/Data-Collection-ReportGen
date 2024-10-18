Created by Collin Brockman 7/24/2023

Notes:
init creates all path information in case folder names are changed
init Detects Current Directory
Do not change innner folders directory only change MAIN folder location
The contents of the #_OUT_ folder are regenerating
The Input can be:
A MF4 file
A MF4 file in a folder
A MF4 file in a folder in a folder (common with the canedge)
The ouput names will be based on the file/folder combination

How to use:
First Install an IDE such as VSCode
For VSCODE go to https://code.visualstudio.com/
Scroll down to user installer and click the x64 download
If using VSCode Open MAIN as a workspace
Open Main.py
VSCode will prompt you to install a python extension
Once the extension is installed make sure to download python of the correct version (3.11.4) either throught the windows store or online
VSCode will automatically try to install it with the windows store if you try to set an interpreter (Bottom Right Hand after Python{})
Then you will need to change MAIN>.venv>pyvenv.cfg to have the correct Paths to the python folder for home and .exe file for the other two paths
If the interpreter is not automatically selcted, select the interpreter as the Python 3.11.4 (.venv)
This will open the virtual enviorment used to run the script
Click the Run Icon in the upper right corner
The script will automatically start updating the terminal with the log

In order to learn more about a specific code file open it and read the comments