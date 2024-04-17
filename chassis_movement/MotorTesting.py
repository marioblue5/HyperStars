import Adafruit_PCA9685
import time

# Function to convert microseconds to PWM value
def microseconds_to_pwm(value, freq=60):
    return int((value / 1000000.0) * freq * 4096)

# Initialize the PCA9685 using the default address
pwm = Adafruit_PCA9685.PCA9685(busnum=1)

# Set the PWM frequency to 60 Hz (good for servos)
pwm.set_pwm_freq(60)

# Motor control parameters
channel = 0  # Adjust based on your connection
min_signal = 1050  # Minimum pulse length out of 4096
max_signal = 2050  # Maximum pulse length out of 4096

# Convert microseconds to PWM values
min_pwm = microseconds_to_pwm(min_signal, 60)
max_pwm = microseconds_to_pwm(max_signal, 60)
print(min_pwm)
print(max_pwm)

neutral_signal = 1550  # Neutral position for many servos and ESCs
neutral_pwm = microseconds_to_pwm(neutral_signal, 60)
print("Setting motor to neutral")
for i in range(4):
        pwm.set_pwm(i, 0, neutral_pwm)

time.sleep(1)

# Example of setting motor to minimum position/speed
print("Setting motor to minimum")
for i in range(4):
        pwm.set_pwm(i, 0, min_pwm)
time.sleep(4)

# Setting motor to neutral position (if applicable)
neutral_signal = 1550  # Neutral position for many servos and ESCs
neutral_pwm = microseconds_to_pwm(neutral_signal, 60)
print("Setting motor to neutral")
for i in range(4):
        pwm.set_pwm(i, 0, neutral_pwm)

time.sleep(4)


# Example of setting motor to maximum position/speed
print("Setting motor to maximum")
for i in range(4):
        pwm.set_pwm(i, 0, max_pwm)
time.sleep(4)

# Setting motor to neutral position (if applicable)
neutral_signal = 1550 # Neutral position for many servos and ESCs
neutral_pwm = microseconds_to_pwm(neutral_signal, 60)
print(neutral_pwm)
print("Setting motor to neutral")
for i in range(4):
        pwm.set_pwm(i, 0, neutral_pwm)
time.sleep(1)
