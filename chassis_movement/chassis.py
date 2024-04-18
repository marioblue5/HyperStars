# some description of what the code does


# Package imports
import Adafruit_PCA9685
import time
import numpy as np
    # import serial
    # import Jetson.GPIO as GPIO
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
    intervals = 10

    # Create an increasing ramp from 0 to percent_speed
    increasing_ramp = np.linspace(0, percent_speed, num=intervals, endpoint=True)

    #Remove the initial value becaue it's redundant
    increasing_ramp = increasing_ramp[1:]

    # Create a decreasing ramp from percent_speed to 0, use less intervals since it'll be easier to slow down
    decreasing_ramp = np.linspace(percent_speed, 0, num=intervals-2, endpoint=True)

    #Remove the initial value because it's redundant
    decreasing_ramp = decreasing_ramp[1:]
    # Combine both ramps into a single array

    return increasing_ramp, decreasing_ramp


# Mapping Percent and Signal Values
def percent_to_pwm(percent):
    # float [-1, 1]
    k = np.clip(-100, 100, percent) / 100.0
    # Calculate the PWM signal value based on the provided percent speed
    signal_value = stop_signal + k * 500
    # Convert microseconds to PWM values
    pwm_value = (signal_value / 1000000.0) * freq * 4096
    return int(pwm_value)


def apply_speed(velocity: np.ndarray):
    velocity = velocity.reshape(-1)
    for i, v in enumurate(velocity):
        pwm.set_pwm(i, 0, percent_to_pwm(v))



# Motor Move Function, Time in seconds
def chassis_forward_backward(velocity: np.ndarray, duration):

    ramp_up, ramp_down = ramping(1.0)

    # The idea is to spend the first 20% of the duration ramping up, and the last 20% ramping down

    ramping_time = min(0.2 * duration, 5)

    # Starting ramp up
    for i in ramp_up:
        apply_speed(velocity * i)
        ddl = time.time() + ramping_time/ramp_up.size
        while time.time() < ddl:
            yield "ramp up"
    ddl = time.time() + time.sleep(duration*0.6)
    while time.time() < ddl:
        yield "linear"
    # Starting ramp down
    for i in ramp_down:
        apply_speed(velocity * i)
        ddl = time.time() + ramping_time / ramp_down.size
        while time.time() < ddl:
            yield "ramp down"
    # Idle
    while True:
        yield None

def ctrl():
    for states in zip(
        move_stepmotor(direction, 10000, pin_stepper_1, pin_switch_1),
        move_stepmotor(direction, 10000, pin_stepper_2, pin_switch_2),
        chassis_forward_backward(
            # velocity matrix
            np.array([
                [100.0, 100.0],
                [100.0, 100.0]
            ]),
            # dutation, seconds
            10.0
        )
    ):
        for s in states:
            if s is not None:
                continue
        break

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



# Initialize the PCA9685 using the default address
pwm = Adafruit_PCA9685.PCA9685(busnum=1)

# Set the PWM frequency to 60 Hz (good for servos)
pwm.set_pwm_freq(60)

if __name__ == '__main__':
      chassis_forward_backward(5,25)


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
                    
