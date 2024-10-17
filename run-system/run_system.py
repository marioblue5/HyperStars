import threading
import multiprocessing
from camera_system import record_bag
from chassis_movement import chassis_forward_backward
import time
from datetime import datetime
import pyrealsense2 as rs
import os
from bag_extractor import count_frames_and_save_rgb_depth_filtered

# Function to ensure directory creation
def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to get all connected camera serial numbers
def get_camera_serial_numbers():
    context = rs.context()
    devices = context.devices
    serial_numbers = [device.get_info(rs.camera_info.serial_number) for device in devices]
    
    if len(serial_numbers) == 0:
        raise ValueError("No cameras detected. Please check connections.")
    
    return serial_numbers

if __name__ == '__main__':
    print("Starting the system...")
    
    # Get connected camera serial numbers
    camera_serials = get_camera_serial_numbers()
    # print(camera_serials[0])
    # print(camera_serials[1])
    timestamp = datetime.now().strftime('%m%d%H%M')
    base_directory = 'dataset_prime'

    # Ensure base directory exists
    ensure_folder(base_directory)
    # Start first motor movement in a thread (backward)
    duration = 3
    motor_speed = -15 
    motor_thread = threading.Thread(target=chassis_forward_backward, args=(duration, motor_speed))
    motor_thread.start()

    # Run camera recording in parallel
    camera_process = multiprocessing.Process(target=record_bag, args=(camera_serials[0], duration, base_directory))
    camera_process.start()

    # Wait for both the motor and camera recording to finish
    motor_thread.join()
    camera_process.join()

    # Start second motor movement in a thread (forward)
    duration= 15
    motor_speed = 15 
    motor_thread = threading.Thread(target=chassis_forward_backward, args=(duration, motor_speed))
    motor_thread.start()

    # Run camera recording in parallel
    camera_process = multiprocessing.Process(target=record_bag, args=(camera_serials[1], duration, base_directory))
    camera_process.start()

        # Wait for both the motor and camera recording to finish
    motor_thread.join()
    camera_process.join(
    print("All camera scans and movements completed. System shutdown.")

