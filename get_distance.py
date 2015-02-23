# Needs these initializations

# import RPIO
# import time
# RPIO.setmode(RPIO.BCM)          # RPIO-Numbering

# We have different sensors. So the function takes a list "sensor = [Trig, Echo]"
# which has trigger and echo pins initialized for each.
# e.g.
# Sensor1 = [16, 17]
# Sensor2 = [18, 19]

# Then initialize IN and OUT
# RPIO.setup(Trig,RPIO.OUT)
# RPIO.setup(Echo,RPIO.IN)
# RPIO.output(Trig, False) 


#----------------------------------------------------

def get_distance(sensor):

    Trig = sensor[0]                     # Set RPIO-Pins
    Echo = sensor[1]


    RPIO.output(Trig, True)         # Send Trigger
    time.sleep(0.00001)
    RPIO.output(Trig, False)

    while RPIO.input(Echo)==0:      # Receive Signal
        pulse_start = time.time()

    while RPIO.input(Echo)==1:
        pulse_end = time.time()

    pulse_duration = pulse_end - pulse_start    # Calculate Distance

    distance = pulse_duration * 17150

    distance = round(distance, 2)

    return distance         # Distance in cm
