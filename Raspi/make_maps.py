# This script shall convert old log-files into new ones and creat GPS-route-maps in html-format (google-maps).
#
# to start:
#	sudo python make_maps.py		--> converts all files and opens all maps in browser
#	sudo python make_maps.py -o		--> converts all files, but doesn't open maps in browser
#	sudo python make_maps.py filename	--> converts only ./log/filename and opens map in browser
#	sudo python make_maps.py filename -o	--> converts only ./log/filename, but doesn't open map in browser
#
# NOTE: It is important to keep the file __init__.py in the directory route_printing

import sys
from route_printing.create_route_log import *
from route_printing.create_map import *

file_name = ""

# first option above:
if (len(sys.argv) == 1):
	open_at_finish=True

# second & third option above:
elif (len(sys.argv) == 2):
	if(sys.argv[1]=="-o"):
		open_at_finish=False
	else:
		file_name=sys.argv[1]
		open_at_finish=True

# fourth option above:
elif ( (len(sys.argv)==3) and (sys.argv[2]=="-o") ):
	file_name = sys.argv[1]
	open_at_finish=False

else:
	print "wrong number or type of arguments. Quit."
	quit ()

# Do the work:

if(file_name==""):
	make_route_LOG(input_path="./log", output_path="./route_printing/GPS_route_log")
else:
	make_route_LOG(file_name, input_path="./log", output_path="./route_printing/GPS_route_log")

print "GPS-data-log(s) created.\n"

if(file_name==""):
	mypath = "log"
	for file_name in [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]:
		make_route_HTML(input_file_name=file_name, open_at_finish=open_at_finish, input_path="./route_printing/GPS_route_log", output_path="./route_htmls")
else:
	make_route_HTML(input_file_name=file_name, open_at_finish=open_at_finish, input_path="./route_printing/GPS_route_log", output_path="./route_htmls")

print "Done."

#make_route_LOG(input_file="", input_path="../log", output_path="./GPS_route_log", output_file="", data_seperator="\t", new_data_seperator=",", auto_all=True, data_format=['time', 'year', 'month', 'day', 'hour', 'minute', 'second', 'latitude', 'longitude', 'altitude', 'track', 'satellites', 'GPS_time', 'steering_direction', 'steering_velocity', 'steering_position'], prefix = 'RC_log', suffix = '.txt')

#make_route_HTML(input_file_name, output_file_name="", input_path="./GPS_route_log", output_path="../route_htmls", data_seperator=",", open_at_finish=False)
