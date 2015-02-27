from RPIO import PWM 
import time

PWM.setup(pulse_incr_us=5)
PWM.init_channel(0,subcycle_time_us=20000)
PWM.add_channel_pulse(0,7,0,300)
while(True):
    eingabe = raw_input('Wert eingeben')
    PWM.add_channel_pulse(0,7,0,int(eingabe))
#time.sleep(2)
#PWM.add_channel_pulse(0,7,0,300)
#time.sleep(2)
#PWM.clear_channel(0)
#time.sleep(2)
#PWM.add_channel_pulse(0,7,0,285)
#time.sleep(2)
#for i in range(300,350,1):
#    PWM.add_channel_pulse(0,7,0,i)
#    time.sleep(1)
#PWM.clear_channel_gpio(0,7)
#PWM.cleanup()
#motor = PWM.Servo()
#print PWM.get_pulse_incr_us()
#motor.set_servo(7,1500)
#time.sleep(2)
#while(True):
#    eingabe = raw_input('Wert eingebe:')
#    if(eingabe=='v'):
#        for i in range(1500,2000,10):
#            print i
#            motor.set_servo(7,i)
#            time.sleep(0.5)
#    else:
#	motor.set_servo(7,int(eingabe))
#for i in range (600,700,20):
#    motor.set_servo(7,i)
#    time.sleep(2)

#    motor.set_servo(7,1500)
#time.sleep(20)
#motor.stop_servo(7)
#motor.stop_servo(7)


