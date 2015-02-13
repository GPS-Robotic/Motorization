from RPIO import PWM
from time import sleep

servo = PWM.Servo()

GPIO_Servo=4

while True:
	i=raw_input('value (1500=stop, starts at 1550)?')
	servo.set_servo(GPIO_Servo, int(i))

