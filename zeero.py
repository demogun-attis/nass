#!/usr/bin/python
import RPi.GPIO as GPIO
import time, sys

print("SETMODE")
GPIO.setmode(GPIO.BCM)

# init list with pin numbers

pinList = [14, 5, 23, 12, 3, 2, 17, 9]

# loop through pins and set mode and state to 'low'

print("FIRST SLEEP")
SleepTimeL = 3
#while 1:
for i in pinList:
    print("BCM %s", i)
    GPIO.setmode(GPIO.BCM)
    print("OUT")
    GPIO.setup(i, GPIO.OUT)
    print("LOW")
    GPIO.output(i, GPIO.LOW)
   
    # time to sleep between operations in the main loop
    
    print("SECOND SLEEP")
    time.sleep(SleepTimeL);    
    # main loop
    
    try:
      print("HIGH")
      GPIO.output(i, GPIO.HIGH)
      print("THIRD SLEEP")
      time.sleep(SleepTimeL);
      GPIO.cleanup()
        
    
    # End program cleanly with keyboard
    except KeyboardInterrupt:
        print ("Quit")
   
        # Reset GPIO settings
        GPIO.cleanup()
        sys.exit()
print("Good bye!")
# find more information on this script at
# http://youtu.be/oaf_zQcrg7g
