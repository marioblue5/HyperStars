# some description of what the code does
"""
Movement of chassis Motors. 
M1 = motor controller 1 --> left front wheels
M2 = motor controller 2 --> right front wheels
M3 = motor controller 3 --> left back wheels
M4 = motor controller 4 --> right back wheels
"""

# Package imports
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
MC1 = 0 
MC2 = 1
MC3 = 2
MC4 = 3

# Define the signal values for 100%, 0%, and -100% speed respectively
max_signal = 2050
stop_signal = 1550
min_signal = 1050

# Mapping Percent and Signal Values
def percent_to_pwm(percent):
    if percent > 100: 
        percent = 100
    elif percent < -100:
        percent = -100

    # Calculate the PWM signal value based on the provided percent speed
    signal_value = stop_signal + (percent / 100) * (max_signal - stop_signal)

    # Convert microseconds to PWM values
    pwm_value = microseconds_to_pwm(signal_value, 60)

    return int(pwm_value)

# Motor Move Function
def motor_move(controller, 0, speed):
    pwm.set_pwm(controller, 0, speed)

# Move Chassis Function
def chassis_move(speed):    #speed percent value
    percent_to_pwm(speed)
    motormove(MC1, 0, pwm_value)
    motormove(MC2, 0, pwm_value)
    motormove(MC3, 0, pwm_value)
    motormove(MC4, 0, pwm_value)

"""
Left here in case we need
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
""" 
                    
