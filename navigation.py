

#constants
obstacle = .5 #meter?						#obstacle distance
c_1 = .7 									#constants for cost function from paper to experiment with
c_2 = .3
segment_width = 10 #degree					#angle width of one scanning segment

target = [a,b,c]				#target coords
GPS = [a_gps,b_gps,c_gps]		#current coords
ref = [a_ref,b_ref,c_ref]		#reference position / direction to target?
#Scan = [liste containing information from scanning sensor]

desired_direction				#direction for steering could also be break and turn around
reference_direction				#direction to target

								#list for narrow, medium and wide gaps
wide = []
medium = []
narrow = []

def gap_finding(Scan,obstacle,narrow, medium, wide):	#take sensor data, obstacle distance and list for gaps
	N_free = 0											#and give back the indices for free gaps ordered as wide, medium, narrow
	for i in range(len(Scan)):
		if Scan[i] <= obstacle:
			if N_free > 3:
				for j in range(N_free-1, -1, -1):
					wide.extend([(i-1-j)])
			elif N_free == 3:
				medium.extend([i-1,i-2,i-3])
			else N_free < 3 and N_free != 0:
				for j in range(N_free-1, -1, -1):
				narrow.extend([(i-1-j)])
			N_free = 0
		else:
			N_free += 1

def cost(ref_direction,segment):									#calculate costs for a steering direction
	return c_1 * (ref_direction - segment*segment_width) + c_2 segment*segment_width

def minimum_cost(gap_list,ref_direction):
	cost_list = [cost(ref_direction,x) for x in gap_list]
	return cost_list.index(min(cost_list))

def calc_direction(reference_direction,narrow,medium,wide,segment_width):		#calculate steering direction from gaps and desired direction
	if (reference_direction % 10 in wide) or (reference_direction % 10 in medium) or (reference_direction % 10 in narrow):
		return reference_direction
	else
		if wide != []:
			return minimum_cost(wide,reference_direction)*segment_width
		elif medium != []:
			return minimum_cost(medium,reference_direction)*segment_width
		elif narrow != []:
			return minimum_cost(narrow,reference_direction)*segment_width
		else:
			return -1 						#-1 for turn around/ go backwards.



