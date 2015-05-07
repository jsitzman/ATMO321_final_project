from IPython.html.widgets import interact, fixed
from IPython.html import widgets
from IPython.display import display # Used to display widgets in the notebook
from mpl_toolkits.basemap import Basemap
import numpy as np
import netCDF4
%pylab inline

#global variables
the_file = ""

#creates the file name
def getfile(year, month, day, time):
    global the_file
    
    #this line will use the globally shared shared1/sarava/ERAINTERIM folder
    #the_file = "/shared1/sarava/ERAINTERIM/" + str(year) + "%02d" % (month, ) + "/" + str(year) + "%02d" % (month, ) + str(day) + "T" + "%02d" % (time, ) + "0000Z.ncd" 
    
    
    #this line is used if the data files are used in the same folder as the notebook.
    #     folders should be named 201411 and 201412
    the_file = str(year) + "%02d" % (month, ) + "/" + str(year) + "%02d" % (month, ) + str(day) + "T" + "%02d" % (time, ) + "0000Z.ncd"
    
    return the_file
    

#this method is needed to create the widgets and make the program interactive
def show_file(year, month, day, time):
    return getfile(year, month, day, time)


# returns the data from the specified file at a specified pressure level for a particular variable type (such as temperature)
def getdict(ncfile, variable_name, level_index):
    dictionary = {}
    extract = ncfile.variables[variable_name]
    dictionary["data"] = extract[level_index,:,:]
    dictionary["units"] = str(extract.units)
    dictionary["latitudes"] = ncfile.variables["Latitude"][:]
    dictionary["longitudes"] = ncfile.variables["Longitude"][:]
    return dictionary

    
#plots the variables specified
#the first variable will be plotted as a contour fill color map
#the second variable will be plotted on top of the first variable as contour lines
def plotpanel(variable1_dict, variable2_dict):
    my_map = Basemap(projection='lcc', resolution = 'l', area_thresh = 1000.0, lat_0 = 35, lon_0 = 275,
                                                                 llcrnrlon=240, llcrnrlat=18, urcrnrlon=310, urcrnrlat=52)
    my_map.drawcoastlines()
    my_map.drawcountries()
    my_map.drawmapboundary()
    my_map.drawmeridians(np.arange(0, 360, 30), labels=[0,0,0,1])
    my_map.drawparallels(np.arange(-90, 90, 15), labels=[1,0,0,0])
    
    values1 = variable1_dict.values()
    keys1 = variable1_dict.keys()
    lon1_data = values1[1]
    lat1_data = values1[2]
    lonall1, latall1 = np.meshgrid(lon1_data, lat1_data)
    lonproj1, latproj1 = my_map(lonall1, latall1)
    if(variable2_dict != 0):
        values2 = variable2_dict.values()
        keys2 = variable2_dict.keys()
        lon2_data = values2[1]
        lat2_data = values2[2]
        lonall2, latall2 = np.meshgrid(lon2_data, lat2_data)
        lonproj2, latproj2 = my_map(lonall2, latall2)
        contours = pylab.contour(lonproj2, latproj2, values2[3], 17, colors='k')
        contours.clabel(fontsize=9, inline=1)
    pylab.contourf(lonproj1, latproj1, values1[3], 10, cmap=cm.jet)
    if(variable2_dict == 0):
        colorbar(orientation='horizontal', shrink=.7, pad = 0.05)
    else:
        colorbar(orientation='horizontal', shrink=.7, pad = 0.05)
    
    #['units', 'longitudes', 'latitudes', 'data']
    print "plotting data..."
    

#this function is called whenever the "plot data" button is pressed
#note: this function is called 1 time per click, but nothing graphically will change if the sliders are not changed
def on_button_clicked(b):
    success = False;
    
    try: #file might not exist, must check for it
        ncf = netCDF4.Dataset(the_file)
        success = True;
        print the_file
    except Exception, excp:
        #print the_file
        print "ERROR: failed to open file."
        print "File could not be found or does not exist."
        
    if(success):
        geo_height_data300 = getdict(ncf, "Z", 19)
        u_wind_data = getdict(ncf, "u", 19)
        
        geo_height_data500 = getdict(ncf, "Z", 15)
        r_vorticity_data = getdict(ncf, "vor", 15)
        
        humidity_data = getdict(ncf, "RH", 11)
        velocity_data = getdict(ncf, "w", 11)
        
        temp_data = getdict(ncf, "T", 0)
        #print temp_data.values()[3]
        
        #plot stuff
        pylab.rcParams['figure.figsize'] = (20.0, 10.0)
        pylab.subplot(221)
        plotpanel(u_wind_data, geo_height_data300)
        pylab.title("GH and wind speed at upper trop")
        
        pylab.subplot(222)
        plotpanel(r_vorticity_data, geo_height_data500)
        pylab.title("GH and relative vorticity at mid trop")
        
        pylab.subplot(223)
        plotpanel(humidity_data, velocity_data,)
        pylab.title("Relative humidity and vertical velocity at lower trop")
        
        pylab.subplot(224)
        plotpanel(temp_data, 0)
        pylab.title("Air Temperature near surface")
    
    
# main program
interact(show_file, year=(1880, 2014), month=(1,12), day=(1, 31), time=(0, 18, 6))
button = widgets.ButtonWidget(description="Plot Data")
display(button)
button.on_click(on_button_clicked)
