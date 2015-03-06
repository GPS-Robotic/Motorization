# This function (make_route_LOG()) shall convert the normal log-files to GPS-data-log-files
# Thereby it will only write all valid (lat,long) values in the new file (nan will be ignored) (each pair in a new line)
# format & file/path-settings can be set (see parameters)
# 
# NOTE: Do not use function write_log() alone!
#
# parameters:	there are no obligatory parameters
#
#	OPTIONAL PARAMETERS WITH DEFAULT VALUES:
#
#		input_file=""
#			filename to convert
#			if not specified ("") AND auto_all = False: gives list to choose, which file will be converted
#			if not specified ("") AND auto_all = True: will convert all files 
#			if specified AND auto_all = True: will convert all files
#			if specified AND auto_all = False: will only convert this given file
#
#		input_path="."
#			path of input-log-files
#			default: current directory!
#
#		output_path="./GPS_route_log"
#			path of output-GPS-data-log-files
#
#		output_file=""
#			filename of output-file, only important, if single file is converted (auto_all = False)
#
#		data_seperator="\t"
#			data-seperator in old log-file
#
#		new_data_seperator=","
#			data-seperator in new GPS-data-log-file
#
#		auto_all=True
#			if True, will convert automatically ALL files in given directory
#
#		data_format=['time', 'year', 'month', 'day', 'hour', 'minute', 'second', 'latitude', 'longitude', 'altitude', 'track', 'satellites', 'GPS_time', 'steering_direction', 'steering_velocity', 'steering_position']
#			format of data in old log-file, only important: position of 'longitude' and 'latitude', 
#				i.e. ['',7,'','crab','longitude','latitude',''] would be valid
#
#		prefix = 'RC_log'
#			prefix of old log-files, only important for selecting files if auto_all = False AND input_file = ""
#
#		suffix = '.txt'
#			suffix of old log-files, only important for selecting files if auto_all = False AND input_file = ""
#


from os import listdir
from os.path import isfile, join
import os
import math
import time

def make_route_LOG(input_file="", input_path=".", output_path="./GPS_route_log", output_file="", data_seperator="\t", new_data_seperator=",", auto_all=True, data_format=['time', 'year', 'month', 'day', 'hour', 'minute', 'second', 'latitude', 'longitude', 'altitude', 'track', 'satellites', 'GPS_time', 'steering_direction', 'steering_velocity', 'steering_position'], prefix = 'RC_log', suffix = '.txt'):

	def write_log(input_file_nmb):
		log_file_name = all_files[input_file_nmb]
		print ""

		print "[01] Opening file " + mypath + log_file_name
		log_file=open(mypath + log_file_name, 'r')

		print "[02] Reading lines"
		i = 0
		data = []
		for line in log_file:
			i = i + 1
			data.append(line)

		print "[03] " + str(i) + " lines read; Closing log-file"
		log_file.close()

		print "[04] File closed; Working with data"

		entry_number = 0
		lat_number = -1
		long_number = -1

		for entry in data_format:
			if entry ==  'latitude':
				if lat_number != -1:
					print "Error: Two times latitude in data format given in this script. Quit."
					quit()
				lat_number = entry_number
			if entry == 'longitude':
				if long_number != -1:
					print "Error: Two times longitude in data format given in this script. Quit."
					quit()
				long_number = entry_number
			entry_number = entry_number + 1

		if ((lat_number == -1) or (long_number == -1)):
			print "Error: no valid data format given in this python script. Quit."
			quit()

		new_data = []
		k = 0 # valid entries
		l = 0 # nan-entries
		for entry in data:
			current_entry = entry.split(data_seperator)
			if ( (math.isnan(float(current_entry[long_number]))) or (math.isnan(float(current_entry[lat_number]))) ):
				l = l + 1
			else:
				k = k + 1
				new_data.append([current_entry[lat_number], current_entry[long_number]])

		if ( (output_file != "") and (auto_all == False) ):
			log_file_name = ouput_file

		print "[05] Data worked: " + str(k) + " valid entries & " + str(l) + " unvalid entries (nan); Opening file " +  track_path + log_file_name + " to save GPS-data"
		track_file = open(track_path + log_file_name, 'w')

		print "[06] File opened; Writting GPS-data"
		for entry in new_data:
			track_file.write(entry[0] + new_data_seperator + entry[1] + "\n")

		print "[07] GPS-data saved; Closing file"
		track_file.close()

		print "[08] File closed"


	mypath = input_path + "/"
	track_path = output_path + "/"

	prefix_length = len(prefix)
	suffix_length = len(suffix)

	all_files = [ f for f in listdir(mypath) if (isfile(join(mypath,f)) and ( ( (f[len(f)-3:] != ".py") and (f[len(f)-4:] != ".py~") ) and (f[len(f)-4:] != ".pyc") ) ) ]

	number_of_files = len(all_files)

	if number_of_files == 0:
		print "No files found in " + mypath
		print "Exit."
		quit()

	if (not (os.path.isdir(output_path))):
		os.system('mkdir ' + output_path)

# no file is specified and auto_all is false --> give list to choose

	if ( (auto_all==False) and (input_file=="") ):

		new_list = []
		for current_file in all_files:
			new_name = current_file
			if prefix_length > 0:
				if current_file[0:prefix_length] == prefix:
					new_name = current_file[prefix_length:]
					if suffix_length > 0:
						if new_name[(len(new_name)-suffix_length):] == suffix:
							new_name = new_name[0:(len(new_name)-suffix_length)]

			if current_file != new_name:
				new_name = time.strftime("%Y %m %d %H %M %S", time.localtime(float(new_name)))
			else:
				new_name = ''
			new_list.append(new_name)

		print ""
		print str(number_of_files) + " files found in " + mypath + ":"
		print ""
		print "number\tdate & time\t\tfilename"
		print "\tyyyy mm dd hh mm ss"
		print ""
		i = 0

		for current_file in all_files:
			if new_list[i] != '':
				print str(i) + "\t" + new_list[i] + "\t" + current_file
			else:
				print str(i) + "\t\t\t\t" + current_file
			i=i+1
			if (i%20) == 0:
				print ""
				raw_input ("displayed 20 files, press enter to continue.")
				print ""
		print ""

		check = 0

		while (check == 0):
			input_file_nmb = raw_input("Input file number to convert (0.." + str(number_of_files-1) + ") and press enter (a for all; q to quit): ")

			check = 1

			if input_file_nmb == 'q':
				quit()

			if input_file_nmb == 'a':
				print "all files will be worked:"
				for input_file_nmb in range(0, number_of_files, 1):
					print ""
					print "FILE " + str(input_file_nmb+1) + " of " + str(number_of_files) + ":"
					print ""
					write_log(input_file_nmb)

			else:

				try:
					input_file_nmb = int(input_file_nmb)
					if ((input_file_nmb<0) or (input_file_nmb>number_of_files-1)):
						print "Error: No entry for " + str(input_file_nmb) + " (number to small/big). Try again..."
						check = 0
				except:
					print "Error: Input is not an integer. Try again..."
					check = 0

				write_log(input_file_nmb)



# file is specified and auto_all is false --> convert only one file

	elif ( (auto_all==False) and (input_file!="") ):
		found = 0
		for input_file_nmb in range(0, number_of_files, 1):
			if (all_files[input_file_nmb] == input_file):
				input_file = temp_input_file
				print "DEB: " + str(input_file_nmb)
				found = 1
		if (found == 1):
			write_log(input_file_nmb)
		else:
			print "Error: file " + mypath + input_file + " not found. Quit."
			quit()

# auto_all is true --> convert all files

	elif (auto_all==True):
		print "all files will be worked:"
		for input_file in range(0, number_of_files, 1):
			print ""
			print "FILE " + str(input_file+1) + " of " + str(number_of_files-1) + ":"
			print ""
			write_log(input_file)

	print ""
	print "Finished. Quit program..."
	print ""
