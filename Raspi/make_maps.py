# This script shall convert old GPS-log-files into new ones and creat GPS-route-maps in html-format (google-maps).
#
# to start:
#	sudo python make_maps.py		--> converts all files, but doesn't open all maps in browser
#	sudo python make_maps.py -o		--> converts all files and opens all maps in browser
#	sudo python make_maps.py filename	--> converts only ./log/filename, but doesn't open map in browser
#	sudo python make_maps.py filename -o	--> converts only ./log/filename and opens map in browser
#
# NOTE: It is important to keep the file __init__.py in the directory log
# NOTE: This script is designed for a specific log/path-configuration:
#		create_route_log.py & create_map.py & __init__.py & the old log-files must be in the log-directory
#		the new log-files will be saved in the log/GPS_route_log -directory
#		and the final html-files will be saved in log/htmls

import sys
from log.create_route_log import *
from log.create_map import *

file_name = ""

# first option above:
if (len(sys.argv) == 1):
	open_at_finish=False

# second & third option above:
elif (len(sys.argv) == 2):
	if(sys.argv[1]=="-o"):
		open_at_finish=True
	else:
		file_name=sys.argv[1]
		open_at_finish=False

# fourth option above:
elif ( (len(sys.argv)==3) and (sys.argv[2]=="-o") ):
	file_name = sys.argv[1]
	open_at_finish=True

else:
	print "wrong number or type of arguments. Quit."
	quit ()

# Do the work:

if(file_name==""):
	pass
	make_route_LOG(input_path="./log", output_path="./log/GPS_route_log")
else:
	make_route_LOG(file_name, input_path="./log", output_path="./log/GPS_route_log")

print "GPS-data-log(s) created.\n"

if(file_name==""):
	mypath = "log"
	# exclude the python files:
	for file_name in [ f for f in listdir(mypath) if (isfile(join(mypath,f)) and ( ( (f[len(f)-3:] != ".py") and (f[len(f)-4:] != ".py~") ) and (f[len(f)-4:] != ".pyc") ) ) ]:
		try:
			pass
			make_route_HTML(input_file_name=file_name, open_at_finish=open_at_finish, input_path="./log/GPS_route_log", output_path="./log/htmls")
		except:
			print "ERROR at file " + file_name
else:
	try:
		make_route_HTML(input_file_name=file_name, open_at_finish=open_at_finish, input_path="./log/GPS_route_log", output_path="./log/htmls")
	except:
		print "ERROR at file " + file_name

print "Done."
