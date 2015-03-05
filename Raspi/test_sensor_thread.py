import sensors
import time

sens = sensors.sensors(mode=1, start=False)

raw_input("Press enter to start")
sens.start()

time.sleep(1)

while True:
	out = str(sens.running) + ": " + str(sens.measurements[0][0]) + ", ("
	for entry in sens.measurements[1]:
		out = out + str(entry[0]) + ", "
	out = out + "), "  + str(sens.measurements[2][0])
	f=open("test.txt", "w")
	print out + "\n"
	f.write(out + "\n")
	f.close()
	time.sleep(.5)
