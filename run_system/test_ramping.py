import numpy as np
intervals = 5
percent_speed = input("Enter percent speed: ")
percent_speed = int(percent_speed)
# Create an increasing ramp from 0 to percent_speed
increasing_ramp = np.linspace(0, percent_speed, num=intervals, endpoint=True)
# Create a decreasing ramp from percent_speed to 0, use less intervals since it'll be easier to slow down
decreasing_ramp = np.linspace(percent_speed, 0, num=intervals-2, endpoint=True)

# Remove the initial value because it's redundant
decreasing_ramp = decreasing_ramp[1:]
# Combine both ramps into a single array
print(increasing_ramp)
print(decreasing_ramp)