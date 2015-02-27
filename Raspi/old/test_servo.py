import time
import os
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD) # choose PIN-numeration by board, not by GPIO-numeration
GPIO.setup(26,GPIO.OUT) # choose output on PIN 26
# GPIO.setup(12,GPIO.OUT) # same for LED

while True:
    Servo = GPIO.PWM(26,50) # initialize PWM on PIN 26 with 50Hz frequenzy
#    LED = GPIO.PWM(12,50) # initialize PWM on PIN 12 with 50Hz frequenzy (for LED)
    Eingabe = raw_input("Wahl: l / r / m / q ")
    
    if(Eingabe == "r"):
        Schritte = raw_input("Schrittweite? ")
        print Schritte, " Schritte nach rechts"
        Servo.start(10) # start PWM with duty-cylce 10% of 20ms = 2ms
#	LED.start(10) #10

        for Counter in range(int(Schritte)):
            time.sleep(0.1)

        Servo.stop() # stop duty-cycle
#	LED.stop()

    elif(Eingabe == "m"):
        Servo.start(7)
#	LED.start(7) #7
        print "Drehung in Mittel"

        time.sleep(1)
        Servo.stop()
#	LED.stop()

    elif(Eingabe == "l"):
        Schritte = raw_input("Schrittweite? ")
        print Schritte, " Schritte nach links"
        Servo.start(5) #5
#	LED.start(5)
        
        for Counter in range(int(Schritte)):
            time.sleep(0.1)

        Servo.stop()
#	LED.stop()

    elif(Eingabe == "q"):
        print "Programm wird beendet"
        os._exit(1)
        Servo.stop()
#	LED.stop()
        GPIO.cleanup()

    else:
        print "Ungueltige Eingabe!!"

servo.stop()
GPIO.cleanup()
