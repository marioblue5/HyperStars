""" 
Someone check this for errors
I edited it so that both controllers were moving
IDK if it works though
"""

import Jetson.GPIO as GPIO
import time

# GPIO pin setup
DIR_pin_1 = 18  # Direction pin
STEP_pin_1 = 32  # Step pin
ENABLE_pin_1 = 16  # Enable pin for the TMC2209
LIMIT_pin_1 = 22 # Limit Switch Pin

DIR_pin_2 = 19
STEP_pin_2 = 33
ENABLE_pin_2 = 17
LIMIT_pin_2 = 23

# Motor setup
steps_per_revolution = 2000  # Adjust this based on your motor's specification

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering

GPIO.setup(DIR_pin_1, GPIO.OUT)
GPIO.setup(DIR_pin_2, GPIO.OUT)

GPIO.setup(STEP_pin_1, GPIO.OUT)
GPIO.setup(STEP_pin_2, GPIO.OUT)

GPIO.setup(ENABLE_pin_1, GPIO.OUT)
GPIO.setup(ENABLE_pin_2, GPIO.OUT)

GPIO.setup(LIMIT_pin_1, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(LIMIT_pin_2, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to enable/disable the motor driver
def enable_stepmotor(enable=True):
    """
    Enables or disables the motor driver.
    :param enable: True to enable, False to disable.
    """
    # Assuming the TMC2209's Enable pin is active-low
    GPIO.output(ENABLE_pin, GPIO.LOW if enable else GPIO.HIGH)

def move_stepmotor(direction, steps, stepper_pin, switch_pin, delay=0.0005):
    """
    Moves the motor in the specified direction for a number of steps.
    :param direction: Direction to rotate (True for one way, False for the reverse).
    :param steps: Number of steps to move.
    :param delay: Delay between steps in seconds.
    """
    GPIO.output(DIR_pin, direction)
    # Initialize the state
    state = 1
    GPIO.output(stepper_pin, GPIO.HIGH)
    last_filp: float = time.time() # seconds
    while True:
        if GPIO.input(LIMIT_pin_1) == GPIO.LOW and GPIO.input(LIMIT_pin_2) == GPIO.LOW:
            # position limit pin activated
            yield None
        elif steps <= 0:
            # no steps left
            yield None
        else:
            # check the previous state and flip pin upon next ddl
            if time.time() - last_filp >= delay:
                last_flip = time.time()
                state = 0 if state else 1
                steps -= state
                if steps <= 0:
                    continue
                GPIO.output(stepper_pin, GPIO.HIGH if state else GPIO.LOW)
            yield steps # The steps left

try:
    enable_stepmotor(enable=True)  # Enable the motor before moving
    steps = steps_per_revolution * 2  # Change "2" to adjust the number of revolutions
    move_stepmotor(True, steps)  # Move forward
    time.sleep(2)  # Wait for 2 seconds
    move_stepmotor(False, steps)  # Move backward
    enable_stepmotor(enable=False)  # Optionally, disable the motor after operations

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    enable_stepmotor(enable=False)  # Ensure motor is disabled when cleaning up
    GPIO.cleanup()  # Clean up GPIO to ensure a clean exit
