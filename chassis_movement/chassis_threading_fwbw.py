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
    # import serial
import Jetson.GPIO as GPIO
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
    intervals = 3

    # Create an increasing ramp from 0 to percent_speed
    increasing_ramp = np.linspace(0, percent_speed, num=intervals, endpoint=True)


    # Create a decreasing ramp from percent_speed to 0, use less intervals since it'll be easier to slow down
    decreasing_ramp = np.linspace(percent_speed, 0, num=intervals-2, endpoint=True)

    #Remove the initial value because it's redundant
    decreasing_ramp = decreasing_ramp[1:]
    # Combine both ramps into a single array

    return increasing_ramp, decreasing_ramp


# Mapping Percent and Signal Values
def percent_to_pwm(percent):
    if percent > 100: 
        percent = 100
    elif percent < -100:
        percent = -100

    # Calculate the PWM signal value based on the provided percent speed
    signal_value = stop_signal + (percent / 100) * 500

    # Convert microseconds to PWM values
    pwm_value = (signal_value / 1000000.0) * freq * 4096

    return int(pwm_value)

# Motor Move Function, Time in seconds
def chassis_forward_backward(duration,percent_speed):

    ramp_up,ramp_down = ramping(percent_speed)

    # The idea is to spend the first 20% of the duration ramping up, and the last 20% ramping down

    ramping_time = 0.2*duration

    # Starting ramp up
    # for i in ramp_up:
    #     for j in range(4):
    #         pwm.set_pwm(j,0,percent_to_pwm(i))
    #     if i == 0:
    #         time.sleep(1)
    #     time.sleep(ramping_time/ramp_up.size)
    for j in range(4):
             pwm.set_pwm(j,0,percent_to_pwm(percent_speed))
    time.sleep(duration*0.6)
    # Starting ramp down
    for i in ramp_down:
        for j in range(4):
            pwm.set_pwm(j,0,percent_to_pwm(i))
        time.sleep(ramping_time/ramp_down.size)

# Note! Left and right movement do not need a negative percent value, just use 
# 0-100 as a magnitude 

def chassis_move_left(duration,percent_speed):
    # Diagonal Pair
    ramp_up,ramp_down = ramping(percent_speed)

    # The idea is to spend the first 20% of the duration ramping up, and the last 20% ramping down

    ramping_time = 0.2*duration

    # Starting ramp up
    for i in ramp_up:
        pwm.set_pwm(0, 0,percent_to_pwm(-abs(i)))
        pwm.set_pwm(3,0,percent_to_pwm(-abs(i)))
        # Diagonal Pair
        pwm.set_pwm(1,0,percent_to_pwm(abs(i)))
        pwm.set_pwm(2,0,percent_to_pwm(abs(i)))
        time.sleep(ramping_time/ramp_up.size)
    time.sleep(duration*0.6)
    # Starting ramp down
    for i in ramp_down:
        pwm.set_pwm(0, 0,percent_to_pwm(-abs(i)))
        pwm.set_pwm(3,0,percent_to_pwm(-abs(i)))
        # Diagonal Pair
        pwm.set_pwm(1,0,percent_to_pwm(abs(i)))
        pwm.set_pwm(2,0,percent_to_pwm(abs(i)))
        time.sleep(ramping_time/ramp_down.size)
def chassis_rotate_cw(duration,percent_speed):
    # Diagonal Pair
    ramp_up,ramp_down = ramping(percent_speed)

    # The idea is to spend the first 20% of the duration ramping up, and the last 20% ramping down

    ramping_time = 0.2*duration

    # Starting ramp up
    for i in ramp_up:
        pwm.set_pwm(1, 0,percent_to_pwm(-abs(i)))
        pwm.set_pwm(3,0,percent_to_pwm(-abs(i)))
        # Diagonal Pair
        pwm.set_pwm(0,0,percent_to_pwm(abs(i)))
        pwm.set_pwm(2,0,percent_to_pwm(abs(i)))
        time.sleep(ramping_time/ramp_up.size)
    time.sleep(duration*0.6)
    # Starting ramp down
    for i in ramp_down:
        pwm.set_pwm(1, 0,percent_to_pwm(-abs(i)))
        pwm.set_pwm(3,0,percent_to_pwm(-abs(i)))
        # Diagonal Pair
        pwm.set_pwm(0,0,percent_to_pwm(abs(i)))
        pwm.set_pwm(2,0,percent_to_pwm(abs(i)))
        time.sleep(ramping_time/ramp_down.size)

def chassis_rotate_ccw(duration,percent_speed):
    # Diagonal Pair
    ramp_up,ramp_down = ramping(percent_speed)

    # The idea is to spend the first 20% of the duration ramping up, and the last 20% ramping down

    ramping_time = 0.2*duration

    # Starting ramp up
    for i in ramp_up:
        pwm.set_pwm(1, 0,percent_to_pwm(abs(i)))
        pwm.set_pwm(3,0,percent_to_pwm(abs(i)))
        # Diagonal Pair
        pwm.set_pwm(0,0,percent_to_pwm(-abs(i)))
        pwm.set_pwm(2,0,percent_to_pwm(-abs(i)))
        time.sleep(ramping_time/ramp_up.size)
    time.sleep(duration*0.6)
    # Starting ramp down
    for i in ramp_down:
        pwm.set_pwm(1, 0,percent_to_pwm(abs(i)))
        pwm.set_pwm(3,0,percent_to_pwm(abs(i)))
        # Diagonal Pair
        pwm.set_pwm(0,0,percent_to_pwm(-abs(i)))
        pwm.set_pwm(2,0,percent_to_pwm(-abs(i)))
        time.sleep(ramping_time/ramp_down.size)
    
def chassis_move_right(duration, percent_speed):
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
# Stepper Motors!!!!

def move_stepmotor(direction, steps, delay=0.001):
    """
    Moves the motor in the specified direction for a number of steps.
    :param direction: Direction to rotate (True for one way, False for the reverse).
    :param steps: Number of steps to move.
    :param delay: Delay between steps in seconds.
    """
    GPIO.output(DIR_pin_L, direction)
    GPIO.output(DIR_pin_R, not direction)
    for _ in range(steps):
        #if GPIO.input(LIMIT_pin_1) == GPIO.LOW || GPIO.input(LIMIT_pin_2) == GPIO.LOW: 
         #   break
        #else
        GPIO.output(STEP_pin_L, GPIO.HIGH)
        GPIO.output(STEP_pin_R, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP_pin_L, GPIO.LOW)
        GPIO.output(STEP_pin_R, GPIO.LOW)
        time.sleep(delay)
# Function to create a folder if it doesn't exist
def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to setup each camera
def setup_camera(serial_number):
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_device(serial_number)
    config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
    pipeline.start(config)
    return pipeline

# Function to save camera intrinsics to a JSON file
def save_intrinsic_as_json(filename, frame):
    intrinsics = frame.profile.as_video_stream_profile().intrinsics
    with open(filename, 'w') as outfile:
        json.dump(
            {
                'width': intrinsics.width,
                'height': intrinsics.height,
                'intrinsic_matrix': [
                    intrinsics.fx, 0, 0,
                    0, intrinsics.fy, 0,
                    intrinsics.ppx, intrinsics.ppy, 1
                ]
            },
            outfile,
            indent=4
        )

# Function to capture and save a frame from each camera
def capture_frame(pipeline, folder_name, frame_number):
    ensure_folder(folder_name)
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()
    if not depth_frame or not color_frame:
        return False
    
    # Save intrinsics
    save_intrinsic_as_json(f"{folder_name}/intrinsics.json", color_frame)
    
    # Save images
    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    cv2.imwrite(f"{folder_name}/depth-{frame_number}.png", depth_image)
    cv2.imwrite(f"{folder_name}/color-{frame_number}.jpg", color_image)
    return True

def start_capture():
    try:
        # Find connected devices
        context = rs.context()
        devices = context.query_devices()
        serial_numbers = [device.get_info(rs.camera_info.serial_number) for device in devices]

        if len(serial_numbers) < 3:
            raise ValueError("Three D405 cameras are not connected")

        # Setup pipelines for each camera
        pipelines = [setup_camera(sn) for sn in serial_numbers]

        # Directory names for each camera
        directories = ["Camera_1", "Camera_2", "Camera_3"]

        # Capture 100 frames from each camera
        for i in range(90):
            for pipeline, directory in zip(pipelines, directories):
                capture_frame(pipeline, directory, i)

    finally:
        # Stop all pipelines
        for pipeline in pipelines:
            pipeline.stop()

    print("Image capture and intrinsics saving completed for all cameras.")
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
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

GPIO.setup(DIR_pin_L, GPIO.OUT)
GPIO.setup(DIR_pin_R, GPIO.OUT)

GPIO.setup(STEP_pin_L, GPIO.OUT)
GPIO.setup(STEP_pin_R, GPIO.OUT)

# Initialize the PCA9685 using the default address
pwm = Adafruit_PCA9685.PCA9685(busnum=1)

# Set the PWM frequency to 60 Hz (good for servos)
pwm.set_pwm_freq(60)

if __name__ == '__main__':
    try:
        steps = steps_per_revolution * 3  # Change "1" to adjust the number of revolutions
        thread1 = threading.Thread(target=chassis_forward_backward,args=(15,15))
        # thread2 = threading.Thread(target=start_capture)
        thread1.start()
        # thread2.start()
        
        thread1.join()
        # thread2.join()
        time.sleep(2)
        # move_stepmotor(False, steps)  # Move backward
        
    finally:
        GPIO.cleanup()

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
                    
