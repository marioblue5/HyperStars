import Jetson.GPIO as GPIO
import time

# Use 'BOARD' pin numbering
GPIO.setmode(GPIO.BOARD)

# PWM pin - Choose between pin 32 and 33
PWM_PIN = 32

# Initialize PWM pin
GPIO.setup(PWM_PIN, GPIO.OUT, initial=GPIO.LOW)
pwm = GPIO.PWM(PWM_PIN, 50)  # Set frequency to 50Hz

def microseconds_to_duty_cycle(microseconds):
    """
    Convert microseconds to a duty cycle percentage for the PWM signal.
    PWM frequency for GPIO library is 50Hz, or 20,000 microseconds per period.
    """
    return (microseconds / 20000) * 100

def start_motor():
    """Start the motor by initializing PWM."""
    pwm.start(microseconds_to_duty_cycle(1050))  # Start with the lowest signal

def change_motor_speed(microseconds):
    """Change the motor speed to a specific value in microseconds."""
    if 1050 <= microseconds <= 1950:
        duty_cycle = microseconds_to_duty_cycle(microseconds)
        pwm.ChangeDutyCycle(duty_cycle)
    else:
        print("Microsecond value out of range. Must be between 1050 and 1950.")

def stop_motor():
    """Stop the motor."""
    pwm.stop()

# Example usage
if __name__ == "__main__":
    try:
        start_motor()
        time.sleep(2)  # Wait for 2 seconds
        print('Starting Test')
        # Example: Set motor speed to mid-range
        change_motor_speed(1500)
        time.sleep(5)  # Wait for 2 seconds
        
        # Stop the motor
        stop_motor()
        
    except KeyboardInterrupt:
        print("Program stopped by User")
    finally:
        pwm.stop()
        GPIO.cleanup()  # Clean up all GPIO
