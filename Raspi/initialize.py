# This script/functions shall initialize everything, meaning:
#	get_config: loading parameters from a config-file and returning them as a dictionary
#	set_init_pos: setting the mechanics on the car, such as: set wheels straight in the beginning, as well as the sensor-servo...
#
### get_config
#
# CAUTION: The parameters in the main must be updated manually! Best way to do:
#
# parameters.update(init())
# 
# Parameters: (all optional & with default value)
#
#	config_file_name="./Robotic.config"
#		gives the path & name of the config file with the used configuration
#
#	only_lower=False
#		if True: all parameter-names (not parameter-values!) will be translated into lower-case, 
#		example: SERVO_NULL = 1500 --> servo_null=1500
#
#	output=False
#		if False: no output will be print onto console
#
#
# In the configuration file parameters are set acording to
# parameter_name = parameter_value
# Example: SERVO_NULL = 1500
#
# comments can be put by a hash: # 
#	(Example: SERVO_NULL = 1500 # Straight-Position of Servo)
# 	everything in a line, after the # will be ignored
#
# Empty lines, lines which only contain spaces or comments will be ignored
#
# spaces and tabs ('\t') are ignored on the left-hand-side of the equal-sign only (parameter-name), but not on the right-hand-side
#
# DATA-TYPES FOR THE PARAMETER-VALUE:
#
# if on the right-hand-side of the equal-sign (parameter-value) 'None' is remaining
#	after removing all quotation-marks ('"', '''), spaces and tabs ('\t'), None is used as type
# else if on the right-hand-side of the equal-sign (parameter-value) a number (int, float, long) is remaining 
#	after removing all quotation-marks ('"', '''), spaces and tabs ('\t'), this number will be used,
#	the same accounts for booleon
#	(Example: SERVO_NULL = 		"1500" --> SERVO_NULL=1500)
#	NOTE: 'nan' is also a float-number, but 'NaN' not!
# else if the first symbol on the right-hand-side of the equal-sign (parameter-value) is ''' or '"' respectively 
#	after removing all spaces and tabs, AND the last symbol is ''' or '"'
#	the type will be interpreted as a string (within the quotation-marks)
# else if the first symbol on the right-hand-side of the equal-sign (parameter-value) is '[', '(' or '{' respectively 
#	after removing all quotation-marks (''', '"'), spaces and tabs, AND the last symbol is ']', ')' or '}'
#	the type will be interpreted as list, tuple or dictionary
# else if the parameter-value is no number, nor a list, tuple or dictionary, nor a string in quotation-marks,
#	it is interpreted as string and only tabs & spaces in front of it and at the end are cut before returned.
#
# HINT: to avoid errors & mistakes, use quotation-marks for any strings!
# NOTE: '\"' and '\'' are output-quotation-marks, thus not for structure.
# CAUTION: for floating-numbers use exponential-form for numbers smaller than and equal to 1e-5:
#	   0.00001 = 1e-05   (The 0 is important! wrong: 1e-5)
#	   for bigger numbers use the other form: 0.001
# CAUTION: There may be more problems! Also for long-numbers...
#
# Boolean-Types must be written as 'True' or 'False', not 'true' or 'false'
# Lists must be like [..., ..., ...], Tuples like (..., ..., ...) and dictionaries like {...:..., ...:..., ...)
# 	the structure of these must be stringent

from os.path import isfile

# for conversion to correct data type:
def convert_const(c,output=False):

	try:

		# remove all spaces, tabs and quotation-marks for testing
		temp = (((c.replace(' ','')).replace('\'','')).replace('\"','')).replace('\t','')	

		# checking for None

		if (temp == "None"):
			return None

		# checking for number

		for c_type in [int, float, long, bool]: # types to be tested

			# try type:
			try:
				if str(c_type(temp)) == temp:
					return c_type(temp)
			except ValueError:
				pass


		# Checking for string in quotation-marks

		temp2 = (c.replace(' ','')).replace('\t','')	
		if (temp2[0] == "\'" and temp2[len(temp2)-1] == "\'" and temp2[len(temp2)-2:]!="\\\'"):
			return c[c.find("\'")+1:(c.rfind("\'"))]
		elif (temp2[0] == "\"" and temp2[len(temp2)-1] == "\"" and temp2[len(temp2)-2:]!="\\\""):
			return c[c.find("\"")+1:(c.rfind("\""))]


		# Checking for list, tuple and dictionary:

		elif (temp[0] == "[" and temp[len(temp)-1]=="]"): # it's a list!

			# now split into parts
			temp = c[c.find("[")+1:c.rfind("]")]
			new_list = []
			pos = 0
			last_sep = -1
			structure = []

			for letter in temp: # check every letter to get structure...
				if (letter == "\"" and temp[pos-1:pos+1]!="\\\""): 
					if len(structure) == 0:
						structure.append("\"")
					else:
						if structure[len(structure)-1] != "\'":
							if structure[len(structure)-1] == "\"":
								structure = structure[0:len(structure)-1]
							else:
								structure.append("\"")
				elif (letter == "\'" and temp[pos-1:pos+1]!="\\\'"): 
					if len(structure) == 0:
						structure.append("\'")
					else:
						if structure[len(structure)-1] != "\"":
							if structure[len(structure)-1] == "\'":
								structure = structure[0:len(structure)-1]
							else:
								structure.append("\'")
				elif (letter == "["):
					if len(structure) == 0:
						structure.append("[")
					else:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							structure.append("[")
				elif (letter == "]"):
					if len(structure) != 0:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							if structure[len(structure)-1] == "[":
								structure = structure[0:len(structure)-1]
				elif (letter == "("):
					if len(structure) == 0:
						structure.append("(")
					else:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							structure.append("(")
				elif (letter == ")"):
					if len(structure) != 0:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							if structure[len(structure)-1] == "(":
								structure = structure[0:len(structure)-1]
				elif (letter == "{"):
					if len(structure) == 0:
						structure.append("{")
					else:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							structure.append("{")
				elif (letter == "}"):
					if len(structure) != 0:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							if structure[len(structure)-1] == "{":
								structure = structure[0:len(structure)-1]
				elif (letter == ","):
					if len(structure) == 0:
						new_list.append(convert_const(temp[last_sep+1:pos],output=output))
						last_sep=pos
				else:
					pass
				pos = pos + 1
			if last_sep != len(temp)-1:
				new_list.append(convert_const(temp[last_sep+1:],output=output))
		
			return new_list


		elif (temp[0] == "(" and temp[len(temp)-1]==")"): # it's a tuple!

			# now split into parts
			temp = c[c.find("(")+1:c.rfind(")")]
			new_tuple = ()
			pos = 0
			last_sep = -1
			structure = []

			for letter in temp: # check every letter to get structure...
				if (letter == "\"" and temp[pos-1:pos+1]!="\\\""): 
					if len(structure) == 0:
						structure.append("\"")
					else:
						if structure[len(structure)-1] != "\'":
							if structure[len(structure)-1] == "\"":
								structure = structure[0:len(structure)-1]
							else:
								structure.append("\"")
				elif (letter == "\'" and temp[pos-1:pos+1]!="\\\'"): 
					if len(structure) == 0:
						structure.append("\'")
					else:
						if structure[len(structure)-1] != "\"":
							if structure[len(structure)-1] == "\'":
								structure = structure[0:len(structure)-1]
							else:
								structure.append("\'")
				elif (letter == "["):
					if len(structure) == 0:
						structure.append("[")
					else:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							structure.append("[")
				elif (letter == "]"):
					if len(structure) != 0:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							if structure[len(structure)-1] == "[":
								structure = structure[0:len(structure)-1]
				elif (letter == "("):
					if len(structure) == 0:
						structure.append("(")
					else:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							structure.append("(")
				elif (letter == ")"):
					if len(structure) != 0:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							if structure[len(structure)-1] == "(":
								structure = structure[0:len(structure)-1]
				elif (letter == "{"):
					if len(structure) == 0:
						structure.append("{")
					else:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							structure.append("{")
				elif (letter == "}"):
					if len(structure) != 0:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							if structure[len(structure)-1] == "{":
								structure = structure[0:len(structure)-1]
				elif (letter == ","):
					if len(structure) == 0:
						new_tuple = new_tuple + (convert_const(temp[last_sep+1:pos],output=output),)
						last_sep=pos
				else:
					pass
				pos = pos + 1
			if last_sep != len(temp)-1:
				new_tuple = new_tuple + (convert_const(temp[last_sep+1:],output=output), )
			return new_tuple


		elif (temp[0] == "{" and temp[len(temp)-1]=="}"): # it's a dictionary!

			# now split into parts
			temp = c[c.find("{")+1:c.rfind("}")]
			new_dict = {}
			pos = 0
			last_sep = -1
			structure = []
			doppel_p = -1

			for letter in temp: # check every letter to get structure...
				if (letter == "\"" and temp[pos-1:pos+1]!="\\\""): 
					if len(structure) == 0:
						structure.append("\"")
					else:
						if structure[len(structure)-1] != "\'":
							if structure[len(structure)-1] == "\"":
								structure = structure[0:len(structure)-1]
							else:
								structure.append("\"")
				elif (letter == "\'" and temp[pos-1:pos+1]!="\\\'"): 
					if len(structure) == 0:
						structure.append("\'")
					else:
						if structure[len(structure)-1] != "\"":
							if structure[len(structure)-1] == "\'":
								structure = structure[0:len(structure)-1]
							else:
								structure.append("\'")
				elif (letter == "["):
					if len(structure) == 0:
						structure.append("[")
					else:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							structure.append("[")
				elif (letter == "]"):
					if len(structure) != 0:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							if structure[len(structure)-1] == "[":
								structure = structure[0:len(structure)-1]
				elif (letter == "("):
					if len(structure) == 0:
						structure.append("(")
					else:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							structure.append("(")
				elif (letter == ")"):
					if len(structure) != 0:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							if structure[len(structure)-1] == "(":
								structure = structure[0:len(structure)-1]
				elif (letter == "{"):
					if len(structure) == 0:
						structure.append("{")
					else:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							structure.append("{")
				elif (letter == "}"):
					if len(structure) != 0:
						if (structure[len(structure)-1] != "\"" and structure[len(structure)-1] != "\'"):
							if structure[len(structure)-1] == "{":
								structure = structure[0:len(structure)-1]
				elif (letter == ":"):
					if len(structure) == 0:
						doppel_p = pos
				elif (letter == ","):
					if (len(structure) == 0 and doppel_p>-1):
						new_dict[conver_const(temp[last_sep+1,doppel_p], output=output)] = convert_const(temp[doppel_p+1:pos], output=output)
						last_sep=pos
						doppel_p=-1
				else:
					pass
				pos = pos + 1
			if (last_sep != len(temp)-1 and doppel_p>-1):
				new_dict[conver_const(temp[last_sep+1,doppel_p],output=output)] = convert_const(temp[doppel_p+1:],output=output)
			return new_dict


		else: # so it's just a string...
			while (c[0] == " " or c[0] == "\t"):
				c = c[1:]
			while (c[len(c)-1] == " " or c[len(c)-1] == "\t"):
				c = c[0:len(c)-1]
			return c

	except: # On error: return string
		if output:
			print "Some error occured converting \'" + c + "\'. Returning as string."
		return c


# imports parameters from config-file
def get_config(config_file_name="./robotic.config", only_lower=False, output=False):

	parameters = {} # initialize empty dictionary

	if (not isfile(config_file_name)): # Check if file exists
		if output:
			print "File " + str(config_file_name) + " does not exist. Stop importing parameters."
		return parameters # and quit returning parameters (empty)

	if output:
		print "Start initialization: Open file " + config_file_name
	
	config_file=open(config_file_name, 'r')

	i = 0 # valid-parameter-counter
	j = 0 # ignored lines-counter (empty, comments, wrong type, ...)
	k = 0 # count number of parameters that were overwritten (double-definition)
	over = "" # string with all parameters that were overwritten (double-definition)

	if output:
		print "File opened, read all lines and get parameters."

	for line in config_file: # read complete file, line by line
		new_line_data = (line.replace("\n", "")).split("#")[0] # remove comments and end-of-line-escape-symbol
		parameter = new_line_data.split("=") # seperate parameter-name and -value
		
		if (len(parameter) == 2): # check if syntax is correct & line not empty (2 entries: name and value)

			name = (parameter[0].replace(' ','')).replace('\t','') # remove spaces and tabs in parameter-name
			if (name != ""): # check if parameter-name is not empty
				parameter[0] = name

				i = i + 1 # count the valid parameters

				if only_lower==True: # Translate to lower-case-letters
					parameter[0] = parameter[0].lower()

				if parameter[0] in parameters: # check if current parameter is already set
					k = k + 1
					over = over + str(parameter[0]) + "=" + str(parameters[parameter[0]]) + ", "

				parameters[convert_const(parameter[0],output=output)] = convert_const(parameter[1],output=output) # add valid parameter to dictionary

			else: # parameter-name is empty ("")
				j = j + 1 # count invalid / ignored parameters & lines

		else: # syntax is wrong or line is empty / a comment
			j = j + 1 # count invalid / ignored parameters & lines

	config_file.close()

	if output: # print output
		print "All lines read & file closed:"
		print "Invalid or empty lines and comments: " + str(j)
		print "Overwritten parameters (double-definition): " + str(k)
		if k>0:
			print "Overwritten parameters & values: "
			print over
		print "Valid parameters: " + str(i-k)
		print "Valid parameters & values:"
		print parameters

	if i-k == 0: # quit if config file contains no parameters
		if output:
			print "No valid parameters. Stop initialization."

	if output:
		print "Finished initialization: Returning new parameters."
	get_config.parameters = parameters
	return parameters # return parameters


# sets mechanics, like servos, to starting-positions
def set_init_pos(parameters, only_lower=True, output=False):
	if output:
		print "Setting Servos etc."
	print parameters



# DEFAULT CONFIGURATION OF robotic.conf:
