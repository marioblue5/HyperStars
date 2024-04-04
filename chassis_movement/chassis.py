# some description of what the code does
"""
Movement of chassis Motors. 
M1 = motor controller 1 --> left front wheels
M2 = motor controller 2 --> right front wheels
M3 = motor controller 3 --> left back wheels
M4 = motor controller 4 --> right back wheels
"""

# package imports
import Adafruit_PCA9685
import time
    # import serial
    # import Jetson.GPIO as GPIO
    # from timeit import default_timer

# Initialization
# Function to convert microseconds to PWM value
def microseconds_to_pwm(value, freq=60):
    return int((value / 1000000.0) * freq * 4096)

# Initialize the PCA9685 using the default address
pwm = Adafruit_PCA9685.PCA9685(busnum=1)

# Set the PWM frequency to 60 Hz (good for servos)
pwm.set_pwm_freq(60)

#Intializing Motor Parameters
min_signal = 1050  # Minimum pulse length out of 4096
max_signal = 2050  # Maximum pulse length out of 4096
MC1 = 0 
MC2 = 1
MC3 = 2
MC4 = 3

# Convert microseconds to PWM values
min_pwm = microseconds_to_pwm(min_signal, 60)
max_pwm = microseconds_to_pwm(max_signal, 60)
print(min_pwm)
print(max_pwm)

"""
Old code, left in case we need...
GPIO.setmode(GPIO.BOARD)
MC1 = 32
MC2 = 33
GPIO.setup(MC1, GPIO.OUT)
GPIO.setup(MC2, GPIO.OUT)
Freq = 50
Duty_cycle = 50
MC1_pwm = GPIO.PWM(MC1, Freq)
MC2_pwm = GPIO.PWM(MC2, Freq)
""" 

# Motor Move Function
def motormove(controller, 0, speed)
pwm.set_pwm(controller, 0, speed)

""" 
Need to think about: 
    * how to define speed
""" 

# Chassis Forward Function
def chassisforward(speed)
motormove(MC1, 0, speed)
motormove(MC2, 0, speed)
motormove(MC3, 0, speed)
motormove(MC4, 0, speed)

# Chassis Backward Function 
def chassisbackward(speed)
motormove(MC1, 0, speed)
motormove(MC2, 0, speed)
motormove(MC3, 0, speed)
motormove(MC4, 0, speed)

# Chassis Stop Function
"""
Look into how to stop all controllers at once
def motorstop(controller, 0);
    neutral_signal = 1550  # Neutral position for many servos and ESCs
    neutral_pwm = microseconds_to_pwm(neutral_signal, 60)
    print("Setting motor to neutral")
    pwm.set_pwm(controller, 0, neutral_pwm)
    time.sleep(2)
"""


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
                    
