# some description of what the code does


# package imports
import serial
import Jetson.GPIO as GPIO
from timeit import default_timer

#initialization
GPIO.setmode(GPIO.BOARD)
MC1 = 32
MC2 = 33
GPIO.setup(MC1, GPIO.OUT)
GPIO.setup(MC2, GPIO.OUT)
Freq = 50
Duty_cycle = 50
MC1_pwm = GPIO.PWM(MC1, Freq)
MC2_pwm = GPIO.PWM(MC2, Freq)

# code here


# initialization
    # send signal to chassis motors
    # if signal is returned - break loop
    # if not, loop x amount of times before sending an error message

# calibration


# defining emergency stopping timer


# main loop here
start = default_timer()
    # data collection
        # move chassis forward slowly

        duration = default_timer() - start

        # if duration >= x, break loop
        pwm.stop()
        # if duration is < x, continue

    # system reset
        # reverse all motors to move the system back to starting position
        # this will be done faster than the speed at which the system scans

#cleanup?
GPIO.cleanup()
                    
