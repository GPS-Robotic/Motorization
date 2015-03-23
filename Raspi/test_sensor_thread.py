import sensors
import time

mod = int(raw_input("Modus? 0, 1 oder 2? "))

sens = sensors.sensors(mode=mod, start=False)

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
