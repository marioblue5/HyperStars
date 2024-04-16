# some description of what the code does


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

#Intializing Motor Parameters
FL = 0 
FR = 1
BL = 2
BR = 3

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

# Motor Move Function, Time in seconds
def chassis_forward_backward(time,percent_speed):
    for i in range(4):
        pwm.set_pwm(i,0,percent_to_pwm(percent_speed))
    time.sleep(time)
    for i in range(4):
        pwm.set_pwm(i,0,percent_to_pwm(stop_signal))

# Note! Left and right movement do not need a negative percent value, just use 
# 0-100 as a magnitude 

def chassis_move_left(duration,percent_speed):
    # Diagonal Pair
    pwm.set_pwm(0, 0,percent_to_pwm(abs(percent_speed)))
    pwm.set_pwm(3,0,percent_to_pwm(abs(percent_speed)))
    # Diagonal Pair
    pwm.set_pwm(2,0,percent_to_pwm(abs(-percent_speed)))
    pwm.set_pwm(4,0,percent_to_pwm(abs(-percent_speed)))
    #Timer and Stop
    time.sleep(duration)
    for i in range(4):
        pwm.set_pwm(i,0,percent_to_pwm(stop_signal))


def chassis_move_right(duration, percent_speed):
    percent_speed = abs(percent_speed)  # Ensuring non-negative speed

    # Diagonal Pair
    pwm.set_pwm(0, 0, percent_to_pwm(abs(-percent_speed)))
    pwm.set_pwm(3, 0, percent_to_pwm(abs(-percent_speed)))
    # Diagonal Pair
    pwm.set_pwm(2, 0, percent_to_pwm(abs(percent_speed)))
    pwm.set_pwm(4, 0, percent_to_pwm(abs(percent_speed)))
    # Timer and Stop
    time.sleep(duration)
    for i in range(4):
        pwm.set_pwm(i, 0, percent_to_pwm(stop_signal))



# Initialize the PCA9685 using the default address
pwm = Adafruit_PCA9685.PCA9685(busnum=1)

# Set the PWM frequency to 60 Hz (good for servos)
pwm.set_pwm_freq(60)



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
                    
