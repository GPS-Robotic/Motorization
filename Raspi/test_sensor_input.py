import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.IN) # 13 19 26

print GPIO.input(19)
