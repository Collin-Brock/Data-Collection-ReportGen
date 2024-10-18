#Created by Collin Brockman 7/24/2023


#Defines Dependent Script Files
from init import path_out,path_resources,path_out_graphs,WidthP,HeightP,Graphs_per_page,Page_header_height,Graph_height
from Create_Log import log
from Excel_Math import Info_Card

#Defines Needed Libraries
from fpdf import FPDF
from pathlib import Path

#Defines Files Global Varibles
HeightP = HeightP*25.4
WidthP = WidthP*25.4
Page_header_height = Page_header_height*25.4
Graph_height = Graph_height*25.4

#This funtion loads a pdf file into memory and puts a title page with the Billy Goat Logo
#This function also sets some basic parameters like page size and font
def PDF_Report_Start():
    pdf = FPDF('P','mm','Letter')
    pdf.set_font('Arial','B',16)
    pdf.add_page()
    pdf.ln(10)
    pdf.cell(0,0, 'PDF CAN Data Report',0,0,'C')
    pdf.ln(10)
    pdf.set_font('Arial','B',10)
    pdf.cell(0,0, 'Created by Collin Brockman',0,0,'C')
    pdf.ln(7)
    return pdf

#Called for each set of data a page is retuned in the PDF with each graph along with warnings for battery and controller temp in red as well as SOC used and kWh used
def PDF_Add_Page(pdf,csvfile):
    #Calls the Excel_Math.py to return the SOC and Warnings information
    SOC_Used,Warn_Controller,Warn_Battery,Battery_kwh_Used = Info_Card(csvfile)
    csvfile_name = str((Path.as_posix(csvfile)).rsplit(sep = "/")[-1]).rsplit(sep = ".")[-2]
    #Main setup code formats texta and formats each of the graphs
    #FPDF's page creation tools are awkward at best the pdf.ln() call drops the line of the "Cursor" to input "Cells" or text box on the empty page
    pdf.add_page()
    #Titles the page with the name of the excel file usally (date name)
    pdf.cell(0,0,csvfile_name,0,0,'C')
    #Sets color to red
    pdf.set_text_color(255,50,50)
    pdf.ln(1)
    pdf.cell(0,0, Warn_Battery + ' ' + Warn_Controller,0,0,'L')
    #Sets color back to black
    pdf.set_text_color(0,0,0)
    pdf.ln(5)
    #Creates SOC and kWh used data cell
    pdf.cell(0,0,Battery_kwh_Used + ' kWh used' + '    State of Charge Used: ' + str(SOC_Used))
    #Start of Image Addition
    #Called as pdf.image(name.png,starting x location,y location (postive = down),Graph Width,Graph Height)
    pdf.image(str(path_out_graphs) + '/' + csvfile_name  + ' ' + 'Temperature'+ '.png',0,Page_header_height,WidthP,Graph_height)
    pdf.image(str(path_out_graphs) + '/' + csvfile_name  + ' ' + 'RPM'+ '.png',0,Page_header_height+Graph_height,WidthP,Graph_height)
    pdf.image(str(path_out_graphs) + '/' + csvfile_name  + ' ' + 'Cell Voltages'+ '.png',0,Page_header_height+2*Graph_height,WidthP,Graph_height)
    pdf.image(str(path_out_graphs) + '/' + csvfile_name  + ' ' + 'Power'+ '.png',0,Page_header_height+3*Graph_height,WidthP,Graph_height)
    #Adds a new page with more graphs
    pdf.add_page()
    pdf.cell(0,0,csvfile_name,0,0,'C')
    pdf.ln(1)
    pdf.image(str(path_out_graphs) + '/' + csvfile_name  + ' ' + 'Battery Temperature'+ '.png',0,Page_header_height,WidthP,Graph_height)
    pdf.image(str(path_out_graphs) + '/' + csvfile_name  + ' ' + 'Motor and Controller Temperature'+ '.png',0,Page_header_height+Graph_height,WidthP,Graph_height)
    pdf.image(str(path_out_graphs) + '/' + csvfile_name  + ' ' + 'Current'+ '.png',0,Page_header_height+2*Graph_height,WidthP,Graph_height)

#Final Call Saves the pdf to the disk in the Out folder
def PDF_Finish(pdf):
    log('PDF Save Started....')
    pdf_save_path = str(path_out)  + '/Report.pdf'
    pdf.output(pdf_save_path, 'F' )
    log('PDF Saved', pdf_save_path)