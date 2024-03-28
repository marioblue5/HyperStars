import Jetson.GPIO as GPIO
import time

# GPIO pin setup
DIR_pin = 18  # Direction pin
STEP_pin = 32  # Step pin
ENABLE_pin = 16  # Enable pin for the TMC2209
LIMIT_pin = 22 # Limit Switch Pin

# Motor setup
steps_per_revolution = 2000  # Adjust this based on your motor's specification

# Initialize GPIO
GPIO.setmode(GPIO.BOARD)  # Use physical pin numbering
GPIO.setup(DIR_pin, GPIO.OUT)
GPIO.setup(STEP_pin, GPIO.OUT)
GPIO.setup(ENABLE_pin, GPIO.OUT)
GPIO.setup(LIMIT_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Function to enable/disable the motor driver
def enable_motor(enable=True):
    """
    Enables or disables the motor driver.
    :param enable: True to enable, False to disable.
    """
    # Assuming the TMC2209's Enable pin is active-low
    GPIO.output(ENABLE_pin, GPIO.LOW if enable else GPIO.HIGH)

def move_motor(direction, steps, delay=0.0005):
    """
    Moves the motor in the specified direction for a number of steps.
    :param direction: Direction to rotate (True for one way, False for the reverse).
    :param steps: Number of steps to move.
    :param delay: Delay between steps in seconds.
    """
    GPIO.output(DIR_pin, direction)
    for _ in range(steps):
        if GPIO.input(LIMIT_pin) == GPIO.LOW: 
            break
        GPIO.output(STEP_pin, GPIO.HIGH)
        time.sleep(delay)
        GPIO.output(STEP_pin, GPIO.LOW)
        time.sleep(delay)

try:
    enable_motor(enable=True)  # Enable the motor before moving
    steps = steps_per_revolution * 2  # Change "2" to adjust the number of revolutions
    move_motor(True, steps)  # Move forward
    time.sleep(2)  # Wait for 2 seconds
    move_motor(False, steps)  # Move backward
    enable_motor(enable=False)  # Optionally, disable the motor after operations

except KeyboardInterrupt:
    print("Program stopped by user")

finally:
    enable_motor(enable=False)  # Ensure motor is disabled when cleaning up
    GPIO.cleanup()  # Clean up GPIO to ensure a clean exit
