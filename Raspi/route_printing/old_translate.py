from os import listdir
from os.path import isfile, join
import math
import time

mypath = 'old_log/' # 'log/'
new_path = 'log/' #'new_log/'
prefix = 'RC_log'
suffix = '.txt'
data_format = ['time', 'year', 'month', 'day', 'hour', 'minute', 'second', 'latitude', 'longitude', 'altitude', 'track', 'satellites', 'GPS_time', 'steering_direction', 'steering_velocity', 'steering_position']
data_seperator = "\t"

prefix_length = len(prefix)
suffix_length = len(suffix)

all_files = [ f for f in listdir(mypath) if isfile(join(mypath,f)) ]

number_of_files = len(all_files)

for c_file in all_files:
	log_file=open(mypath + c_file, 'r')
	save_file = open (new_path + c_file, 'w')

	i = 0
	data = []
	for line in log_file:
		i = i + 1
		w_line = line[0:len(line)-1]

		parts = []
		parts.append((w_line.split('['))[0])
		parts.append((((w_line.split('['))[1]).split(']'))[0])
		parts.append(w_line.split(']')[1])

		w_line = ""
	
		for e in parts[0].split(' '):
			if e != '':
				w_line = w_line + e + data_seperator
		w_line = w_line + "[" + parts[1] + "]"
		for e in parts[2].split(' '):
			w_line = w_line + e + data_seperator

		data.append(w_line)


	for entry in data:
		save_file.write(entry + "\n")
	
	log_file.close()
	save_file.close()
	
	raw_input("In file " + c_file + ": " + str(i) + " lines read & translated; continue? ")
