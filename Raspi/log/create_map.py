# This function shall deliver a .html - file, opening google-maps and displaying the route, given by the GPS-data from the input-file
#
# Starting-Point on map is red, End-Point is white
# Map is centered around Starting-Point
#
# input-parameters:
#		input_file_name: file-name of GPS-data (i.e. log.txt)
#				 data in file must be: "lat,long\nlat,long\n....",
#				 with ',' being the data-separator (can be adjusted) (NOTE: '\n' = new line)
#		OPTIONAL:
#		output_file_name:	file-name of output-HTML (i.e. "log.html"),
#				  	if not set or set to "" --> output file-name will be input filename + '.html'
#		input_path:		path of input file (i.e. "./track"),
#					if not set, will be "./GPS_route_log"
#		output_path:		path of output file (i.e. "./route_htmls"),
#					if not set, will be "./htmls",
#					output-path will be created, if not existent!
#		data_separator:		tells, by which symbol the data in the input file is seperated,
#					if not set, will be ','
#		open_at_finish:		shall the created html-file be opened at the end of the process? (True / False),
#					if not set, will be 'False'

import pygmaps
import webbrowser
import os

def make_route_HTML(input_file_name, output_file_name="", input_path="./GPS_route_log", output_path="./htmls", data_separator=",", open_at_finish=False):

	track_file = open(input_path + "/" + input_file_name, 'r')

	GPS_data = []
	for line in track_file:
		data = (line.split("\n")[0]).split(data_separator)
		GPS_data.append((float(data[0]), float(data[1])))

	start = [(GPS_data[0])[0], (GPS_data[0])[1]]
	stop = [(GPS_data[len(GPS_data)-1])[0], (GPS_data[len(GPS_data)-1])[1]]

	mymap = pygmaps.maps(start[0], start[1], 16)
	mymap.addpoint(start[0], start[1]) #, "#0000FF")
	mymap.addpoint(stop[0], stop[1], "#FFFFFF") #, "#0000FF")
	mymap.addpath(GPS_data,"#0000FF")

	if output_file_name == "":
		output_file_name = input_file_name + ".html"

	if (not (os.path.isdir(output_path))):
		os.system('mkdir ' + output_path)
	mymap.draw(output_path + "/" + output_file_name)

	if open_at_finish:
		webbrowser.open(output_path + "/" + output_file_name,2)



# ORIGINAL EXPLANATION:

########## CONSTRUCTOR: pygmaps.maps(latitude, longitude, zoom) ##############################
# DESC:         initialize a map  with latitude and longitude of center point  
#               and map zoom level "15"
# PARAMETER1:   latitude (float) latittude of map center point
# PARAMETER2:   longitude (float) latittude of map center point
# PARAMETER3:   zoom (int)  map zoom level 0~20
# RETURN:       the instant of pygmaps
#========================================================================================
#mymap = pygmaps.maps(37.428, -122.145, 16)


########## FUNCTION: setgrids(start-Lat, end-Lat, Lat-interval, start-Lng, end-Lng, Lng-interval) ######
# DESC:         set grids on map  
# PARAMETER1:   start-Lat (float), start (minimum) latittude of the grids
# PARAMETER2:   end-Lat (float), end (maximum) latittude of the grids
# PARAMETER3:   Lat-interval (float)  grid size in latitude 
# PARAMETER4:   start-Lng (float), start (minimum) longitude of the grids
# PARAMETER5:   end-Lng (float), end (maximum) longitude of the grids
# PARAMETER6:   Lng-interval (float)  grid size in longitude 
# RETURN:       no returns
#========================================================================================
#mymap.setgrids(37.42, 37.43, 0.001, -122.15, -122.14, 0.001)


########## FUNCTION:  addpoint(latitude, longitude, [color])#############################
# DESC:         add a point into a map and dispaly it, color is optional default is red
# PARAMETER1:   latitude (float) latitude of the point
# PARAMETER2:   longitude (float) longitude of the point
# PARAMETER3:   color (string) color of the point showed in map, using HTML color code
#               HTML COLOR CODE:  http://www.computerhope.com/htmcolor.htm
#               e.g. red "#FF0000", Blue "#0000FF", Green "#00FF00"
# RETURN:       no return
#========================================================================================
#mymap.addpoint(37.427, -122.145, "#0000FF")


########## FUNCTION:  addradpoint(latitude, longitude, radius, [color], title)##################
# DESC:         add a point with a radius (Meter) - Draw cycle
# PARAMETER1:   latitude (float) latitude of the point
# PARAMETER2:   longitude (float) longitude of the point
# PARAMETER3:   radius (float), radius  in meter 
# PARAMETER4:   color (string) color of the point showed in map, using HTML color code
#               HTML COLOR CODE:  http://www.computerhope.com/htmcolor.htm
#               e.g. red "#FF0000", Blue "#0000FF", Green "#00FF00"
# PARAMETER5:   title (string), label for the point
# RETURN:       no return 
#========================================================================================
#mymap.addradpoint(37.429, -122.145, 95, "#FF0000")


########## FUNCTION:  addpath(path,[color])##############################################
# DESC:         add a path into map, the data struceture of Path is a list of points
# PARAMETER1:   path (list of coordinates) e.g. [(lat1,lng1),(lat2,lng2),...]
# PARAMETER2:   color (string) color of the point showed in map, using HTML color code
#               HTML COLOR CODE:  http://www.computerhope.com/htmcolor.htm
#               e.g. red "#FF0000", Blue "#0000FF", Green "#00FF00"
# RETURN:       no return
#========================================================================================
#path = [(37.429, -122.145),(37.428, -122.145),(37.427, -122.145),(37.427, -122.146),(37.427, -122.146)]
#mymap.addpath(path,"#00FF00")

########## FUNCTION:  draw(file)######################################################
# DESC:         create the html map file (.html)
# PARAMETER1:   file (string) the map path and file
# RETURN:       no return, generate html file in specified directory
#========================================================================================
#mymap.draw('./mymap.html')

