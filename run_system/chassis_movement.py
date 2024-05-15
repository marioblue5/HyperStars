# some description of what the code does


# Package imports
import pyrealsense2 as rs
import cv2
import os
import json
import Adafruit_PCA9685
import time
import numpy as np
import threading
# import Jetson.GPIO as GPIO
    # import serial
    # from timeit import default_timer

# Initialization

#Intializing Motor Parameters
FL = 0 
FR = 1
BL = 2
BR = 3

# Define the signal values for 100%, 0%, and -100% speed respectively
freq = 60
max_signal = 2050
stop_signal = 1550
min_signal = 1050

def ramping(percent_speed):
    # Calculate number of steps for each half of the ramp
    intervals = 5

    # Create an increasing ramp from 0 to percent_speed
    increasing_ramp = np.linspace(0, percent_speed, num=intervals, endpoint=True)


    # Create a decreasing ramp from percent_speed to 0, use less intervals since it'll be easier to slow down
    decreasing_ramp = np.linspace(percent_speed, 0, num=intervals-1, endpoint=True)

    #Remove the initial value because it's redundant
    decreasing_ramp = decreasing_ramp[1:]
    # Combine both ramps into a single array
    print(increasing_ramp)
    print(decreasing_ramp)
    return increasing_ramp, decreasing_ramp


# Mapping Percent and Signal Values
def percent_to_pwm(percent):
    np.clip(percent,-100,100)
    # Calculate the PWM signal value based on the provided percent speed
    signal_value = stop_signal + (percent / 100) * 500

    # Convert microseconds to PWM values
    pwm_value = (signal_value / 1000000.0) * freq * 4096

    return int(pwm_value)

# Motor Move Function, Time in seconds
def chassis_forward_backward(duration,percent_speed):
    pwm = initialize_motors()
    ramp_up,ramp_down = ramping(percent_speed)

    # The idea is to spend the first 10% of the duration ramping up, and the last 10% ramping down

    ramping_time = np.minimum(0.1*duration,4)

    # Starting ramp up
    for i in ramp_up:
        for j in range(4):
            pwm.set_pwm(j,0,percent_to_pwm(i))
        if i == 0:
            time.sleep(1)
        # Making each ramp interval proportional to the number of intervals
        time.sleep(ramping_time/ramp_up.size)
    pwm.set_pwm(0,0,percent_to_pwm(percent_speed))
    pwm.set_pwm(1,0,percent_to_pwm(percent_speed*0.95))
    pwm.set_pwm(2,0,percent_to_pwm(percent_speed))
    pwm.set_pwm(3,0,percent_to_pwm(percent_speed*0.95))
    time.sleep(duration*0.8)
    # Starting ramp down
    for i in ramp_down:
        for j in range(4):
            pwm.set_pwm(j,0,percent_to_pwm(i))
        time.sleep(ramping_time/ramp_down.size)

# Note! Left and right movement do not need a negative percent value, just use 
# 0-100 as a magnitude 

# def chassis_move_left(duration,percent_speed):
#     # Diagonal Pair
#     ramp_up,ramp_down = ramping(percent_speed)

#     # The idea is to spend the first 20% of the duration ramping up, and the last 20% ramping down

#     ramping_time = 0.2*duration

#     # Starting ramp up
#     for i in ramp_up:
#         pwm.set_pwm(0, 0,percent_to_pwm(-abs(i)))
#         pwm.set_pwm(3,0,percent_to_pwm(-abs(i)))
#         # Diagonal Pair
#         pwm.set_pwm(1,0,percent_to_pwm(abs(i)))
#         pwm.set_pwm(2,0,percent_to_pwm(abs(i)))
#         time.sleep(ramping_time/ramp_up.size)
#     time.sleep(duration*0.6)
#     # Starting ramp down
#     for i in ramp_down:
#         pwm.set_pwm(0, 0,percent_to_pwm(-abs(i)))
#         pwm.set_pwm(3,0,percent_to_pwm(-abs(i)))
#         # Diagonal Pair
#         pwm.set_pwm(1,0,percent_to_pwm(abs(i)))
#         pwm.set_pwm(2,0,percent_to_pwm(abs(i)))
#         time.sleep(ramping_time/ramp_down.size)
# def chassis_rotate_cw(duration,percent_speed):
#     # Diagonal Pair
#     ramp_up,ramp_down = ramping(percent_speed)

#     # The idea is to spend the first 20% of the duration ramping up, and the last 20% ramping down

#     ramping_time = 0.2*duration

#     # Starting ramp up
#     for i in ramp_up:
#         pwm.set_pwm(1, 0,percent_to_pwm(-abs(i)))
#         pwm.set_pwm(3,0,percent_to_pwm(-abs(i)))
#         # Diagonal Pair
#         pwm.set_pwm(0,0,percent_to_pwm(abs(i)))
#         pwm.set_pwm(2,0,percent_to_pwm(abs(i)))
#         time.sleep(ramping_time/ramp_up.size)
#     time.sleep(duration*0.6)
#     # Starting ramp down
#     for i in ramp_down:
#         pwm.set_pwm(1, 0,percent_to_pwm(-abs(i)))
#         pwm.set_pwm(3,0,percent_to_pwm(-abs(i)))
#         # Diagonal Pair
#         pwm.set_pwm(0,0,percent_to_pwm(abs(i)))
#         pwm.set_pwm(2,0,percent_to_pwm(abs(i)))
#         time.sleep(ramping_time/ramp_down.size)

# def chassis_rotate_ccw(duration,percent_speed):
#     # Diagonal Pair
#     ramp_up,ramp_down = ramping(percent_speed)

#     # The idea is to spend the first 20% of the duration ramping up, and the last 20% ramping down

#     ramping_time = 0.2*duration

#     # Starting ramp up
#     for i in ramp_up:
#         pwm.set_pwm(1, 0,percent_to_pwm(abs(i)))
#         pwm.set_pwm(3,0,percent_to_pwm(abs(i)))
#         # Diagonal Pair
#         pwm.set_pwm(0,0,percent_to_pwm(-abs(i)))
#         pwm.set_pwm(2,0,percent_to_pwm(-abs(i)))
#         time.sleep(ramping_time/ramp_up.size)
#     time.sleep(duration*0.6)
#     # Starting ramp down
#     for i in ramp_down:
#         pwm.set_pwm(1, 0,percent_to_pwm(abs(i)))
#         pwm.set_pwm(3,0,percent_to_pwm(abs(i)))
#         # Diagonal Pair
#         pwm.set_pwm(0,0,percent_to_pwm(-abs(i)))
#         pwm.set_pwm(2,0,percent_to_pwm(-abs(i)))
#         time.sleep(ramping_time/ramp_down.size)
    
# def chassis_move_right(duration, percent_speed):
    # Diagonal Pair
    ramp_up,ramp_down = ramping(percent_speed)

    # The idea is to spend the first 20% of the duration ramping up, and the last 20% ramping down

    ramping_time = 0.2*duration

    # Starting ramp up
    for i in ramp_up:
        pwm.set_pwm(0, 0,percent_to_pwm(abs(i)))
        pwm.set_pwm(3,0,percent_to_pwm(abs(i)))
        # Diagonal Pair
        pwm.set_pwm(1,0,percent_to_pwm(-abs(i)))
        pwm.set_pwm(2,0,percent_to_pwm(-abs(i)))
        time.sleep(ramping_time/ramp_up.size)
    time.sleep(duration*0.6)
    # Starting ramp down
    for i in ramp_down:
        pwm.set_pwm(0, 0,percent_to_pwm(abs(i)))
        pwm.set_pwm(3,0,percent_to_pwm(abs(i)))
        # Diagonal Pair
        pwm.set_pwm(1,0,percent_to_pwm(-abs(i)))
        pwm.set_pwm(2,0,percent_to_pwm(-abs(i)))
        time.sleep(ramping_time/ramp_down.size)
def initialize_motors():

    # Initialize the PCA9685 using the default address
    pwm = Adafruit_PCA9685.PCA9685(busnum=1)

    # Set the PWM frequency to 60 Hz (good for servos)
    pwm.set_pwm_freq(60)
    return pwm

        
# Stepper Motors!!!!

# def move_stepmotor(direction, steps, delay=0.001):
#     """
#     Moves the motor in the specified direction for a number of steps.
#     :param direction: Direction to rotate (True for one way, False for the reverse).
#     :param steps: Number of steps to move.
#     :param delay: Delay between steps in seconds.
#     """
#     GPIO.output(DIR_pin_L, direction)
#     GPIO.output(DIR_pin_R, not direction)
#     for _ in range(steps):
#         #if GPIO.input(LIMIT_pin_1) == GPIO.LOW || GPIO.input(LIMIT_pin_2) == GPIO.LOW: 
#          #   break
#         #else
#         GPIO.output(STEP_pin_L, GPIO.HIGH)
#         GPIO.output(STEP_pin_R, GPIO.HIGH)
#         time.sleep(delay)
#         GPIO.output(STEP_pin_L, GPIO.LOW)
#         GPIO.output(STEP_pin_R, GPIO.LOW)
#         time.sleep(delay)
# # Function to create a folder if it doesn't exist
# def ensure_folder(folder):
#     if not os.path.exists(folder):
#         os.makedirs(folder)

# Function to setup each camera HERE

# Pins
DIR_pin_L = 21  # Direction pin
STEP_pin_L = 22  # Step pin
#LIMIT_pin_1 = 22 # Limit Switch Pin

DIR_pin_R = 23
STEP_pin_R = 24
#LIMIT_pin_2 = 23

# Motor setup
steps_per_revolution = 2000


# Initialize GPIO
# GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

# GPIO.setup(DIR_pin_L, GPIO.OUT)
# GPIO.setup(DIR_pin_R, GPIO.OUT)

# GPIO.setup(STEP_pin_L, GPIO.OUT)
# GPIO.setup(STEP_pin_R, GPIO.OUT)


# if __name__ == '__main__':
#     try:
#         initialize_motors()
#         # steps = steps_per_revolution * 3  # Change "1" to adjust the number of revolutions
#         # thread1 = threading.Thread(target=chassis_forward_backward,args=(8,20))
#         thread2 = threading.Thread(target=start_capture)
#         # time.sleep(1)
#         thread2.start()
#         # time.sleep(1)
#         # thread1.start()
#         # time.sleep(1)
        
#         # thread1.join()
#         # move_stepmotor(False, steps)  # Move backward
#         print(" If motors did not stop by now then ramp down function is busted :(")
#         for j in range(4):
#              pwm.set_pwm(j,0,percent_to_pwm(0))
#         # time.sleep(1)
#         # chassis_forward_backward(10,-20)
#         for j in range(4):
#              pwm.set_pwm(j,0,percent_to_pwm(0))
#         thread2.join()
#     finally:
#         # GPIO.cleanup()
#         print("All good!")
       
