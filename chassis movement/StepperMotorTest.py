import Jetson.GPIO as GPIO
import time

# Define GPIO pins for DIR and STEP signals for the motor
DIR_pin = 18
STEP_pin = 17

# Define the distance to move in steps
distance_steps = 2000  # Adjust this value based on your motor's step angle and mechanical setup

# Initialize GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR_pin, GPIO.OUT)
GPIO.setup(STEP_pin, GPIO.OUT)

# Function to move motor in specified direction for specified steps
def move_motor(direction, steps):
    GPIO.output(DIR_pin, direction)
    for _ in range(steps):
        GPIO.output(STEP_pin, GPIO.HIGH)
        time.sleep(0.0005)  # Adjust this delay as needed for your motor speed
        GPIO.output(STEP_pin, GPIO.LOW)
        time.sleep(0.0005)  # Adjust this delay as needed for your motor speed

try:
    # Move motor forward
    move_motor(GPIO.HIGH, distance_steps)
    
    # Pause for 2 seconds
    time.sleep(2)
    
    # Move motor backward
    move_motor(GPIO.LOW, distance_steps)
    
    # Pause for 2 seconds
    time.sleep(2)

except KeyboardInterrupt:
    print("Program stopped by user")
    
finally:
    # Clean up GPIO
    GPIO.cleanup()
