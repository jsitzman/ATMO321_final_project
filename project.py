from IPython.html.widgets import interact, fixed
from IPython.html import widgets
from IPython.display import display # Used to display widgets in the notebook
import mpl_toolkits.basemap as bm
import numpy as np
import netCDF4
%pylab inline
#the following is the pressure levels available to be used: [ 1000.   925.   850.   700.   600.   500.   400.   300.   250.   200.
#                                                                                        150.   100.    70.    50.    30.    20.    10.]

the_file = ""
#creates the file name
def getfile(year, month, day, time):
    the_file = "ERAINTERIM/" + str(year) + "%02d" % (month, ) + "/" + str(year) + "%02d" % (month, ) + str(day) + "T" + "%02d" % (time, ) + "0000Z.ncd"
    print the_file
    

#this method is needed to create the widgets and make the program interactive
def show_file(year, month, day, time):
    return getfile(year, month, day, time)


# returns the data from the specified file at a specified pressure level for a particular variable type (such as temperature)
def getdict(ncfile, variable_name, level_index):
    #write code here!!!
    print "not done" #delete this line once the function is complete

    
#plots the variables specified
#the first variable will be plotted as a contour fill color map
#the second variable will be plotted on top of the first variable as contour lines
def plotpanel(variable1_dict, variable2_dict):
    #write code here!!!
    print "not done" #delete this line once the function is complete
    

#this function is called whenever the "plot data" button is pressed
#note: this function is called 1 time per click, but nothing graphically will change if the sliders are not changed
def on_button_clicked(b):
    try: #file might not exist, must check for it
        ncf = netCDF4.Dataset(the_file) 
        #getdict(1, 2) #uncomment this line when the function is complete, change "1" and "2" to real values
        #plotpanel(1, 2, 3) #uncomment this line when the function is complete, change "1", "2", and "3" to real values
    except Exception, excp:
        print "ERROR: failed to open file."
        print "File could not be found or does not exist."
    
    
# main program
interact(show_file, year=(1880, 2014), month=(1,12), day=(1, 31), time=(0, 18, 6))
button = widgets.ButtonWidget(description="Plot Data")
display(button)
button.on_click(on_button_clicked)
