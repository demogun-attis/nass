# External module imports
import RPi.GPIO as GPIO
import time

# Pin Definitons:
pwmPin = 14 # Broadcom pin 18 (P1 pin 12)
ledPin = 23 # Broadcom pin 23 (P1 pin 16)

pin = ['9', '14', '5', '23', '12', '3', '2', '17']
dc = 95 # duty cycle (0-100) for PWM pin

GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
# Pin Setup:
GPIO.setup(pwmPin, GPIO.OUT) # LED pin set as output
pwm = GPIO.PWM(pwmPin, 50)  # Initialize PWM on pwmPin 100Hz frequency

# Initial state for LEDs:
# GPIO.output(ledPin, GPIO.LOW)
pwm.start(dc)

print("Here we go! Press CTRL+C to exit")
try:
    for i in pin:
        stat = "0"
        print("STATUS OF: %s", i)
        GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
        GPIO.setup(int(i), GPIO.IN) # PWM pin set as output
        stat = GPIO.input(int(i))
        print("STATUS IS: %s", stat)
    #for i in pin:
    #    GPIO.setmode(GPIO.BCM) # Broadcom pin-numbering scheme
    #    GPIO.setup(int(i), GPIO.OUT) # PWM pin set as output
    #    print("cleaning up: %s", i)
    #    GPIO.cleanup()
    while 1:
        time.sleep(1)
        pwm.ChangeDutyCycle(100-dc)
        GPIO.setup(pwmPin, GPIO.OUT) # PWM pin set as output
        print("setting to high")
        GPIO.output(pwmPin, GPIO.HIGH)
        time.sleep(0.075) 
        print("setting to low")
        GPIO.output(pwmPin, GPIO.LOW)
        time.sleep(0.075)
    print("stop")
except KeyboardInterrupt: # If CTRL+C is pressed, exit cleanly:
    #pwm.stop() # stop PWM
    GPIO.cleanup() # cleanup all GPIO

