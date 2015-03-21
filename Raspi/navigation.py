#constants
c_1 = .7 		#constants for cost function from paper to experiment with
c_2 = .3

#desired_direction				#direction for steering could also be break and turn around
#reference_direction			#direction to target

def gap_finding(Scan,obstacle,narrow, medium, wide):	#take sensor data, obstacle distance and list for gaps
	N_free = 0											#and give back the indices for free gaps ordered as wide, medium, narrow
	for i in range(len(Scan)):
		if Scan[i] <= obstacle:
			if N_free > 3:
				for j in range(N_free-1, -1, -1):
					wide.extend([(i-1-j)])
			elif N_free == 3:
				medium.extend([i-1,i-2,i-3])
			elif N_free < 3 and N_free != 0:
				for j in range(N_free-1, -1, -1):
					narrow.extend([(i-1-j)])
			else:
				print 'error in gap finding!'
			N_free = 0
		else:
			N_free += 1

def cost(ref_direction,segment,segment_number,gap_width):		#calculate costs for a steering direction reference_direction in degree, segment in index
	'blabla bla Beschreibung'
	return c_1 * abs(ref_direction - (segment-segment_number/2.)*segment_width) + c_2 * gap_width #gap width!!!!

def minimum_cost(gap_list,ref_direction,segment_number,gap_width): #gap:list: narrow, medium, wide!
	cost_list = [cost(ref_direction,x,segment_number,gap_width) for x in gap_list]
	return cost_list.index(min(cost_list))

def calc_direction(reference_direction,narrow,medium,wide,segment_width,segment_number):		#calculate steering direction from gaps and desired direction
	#check for integer division
	index = int(round(reference_direction / segment_width) + segment_number/2.) 
	if (index in wide) or (index in medium) or (index in narrow):
		return reference_direction
	else:
		if wide != []:
			return (minimum_cost(wide,reference_direction,segment_number,0)-segment_number/2.)*segment_width	#returns an angle
		elif medium != []:
			return (minimum_cost(medium,reference_direction,segment_number,1)-segment_number/2.)*segment_width
		elif narrow != []:
			return (minimum_cost(narrow,reference_direction,segment_number,2)-segment_number/2.)*segment_width
		else:
			return -1 						#-1 for turn around/ go backwards.

def navigate(Scan,obstacle=100.,reference_direction,segment_width=18.,segment_number=10):
	#list for narrow, medium and wide gaps
	wide = []
	medium = []
	narrow = []
	scan = [x[0] for x in Scan] #from sensors you get a list [[measurement,time],[measurement,time],....]

	gap_finding(scan,obstacle,narrow,medium,wide)
	steering_direction = calc_direction(reference_direction,narrow,medium,wide,segment_width,segment_number)
	return steering_direction #index of segment to go through

#def steering_radius():
	#do something

#def get_reference_direction():
