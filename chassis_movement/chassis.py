# some description of what the code does


# package imports
import serial
from timeit import default_timer

# code here


# initialization
    # send signal to chassis motors
    # if signal is returned - break loop
    # if not, loop x amount of times before sending an error message

# calibration


# defining emergency stopping timer


# main loop here
start = default_timer()
    # data collection
        # move chassis forward slowly

        duration = default_timer() - start

        # if duration >= x, break loop
        # if duration is < x, continue

    # system reset
        # reverse all motors to move the system back to starting position
        # this will be done faster than the speed at which the system scans
                    
