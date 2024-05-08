import pyrealsense2 as rs
import cv2
import os
import json
import Adafruit_PCA9685
import time
import numpy as np
import threading
import Jetson.GPIO as GPIO

# Initialization

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
    initial_time = time.time()
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
    total_time = time.time() - initial_time
    print(f"Total time spent for this frame is: {total_time}")
    return True

# Thread target function to handle camera capture
def handle_camera(serial_number, directory):
    pipeline = setup_camera(serial_number)
    try:
        for i in range(100):  # Adjust number of frames as needed
            capture_frame(pipeline, directory, i)
    finally:
        pipeline.stop()

def start_capture():
    try:
        # Find connected devices
        context = rs.context()
        devices = context.query_devices()
        serial_numbers = [device.get_info(rs.camera_info.serial_number) for device in devices]

        if len(serial_numbers) < 3:
            raise ValueError("Three D405 cameras are not connected")

        # Directory names for each camera
        directories = ["ABC_Camera_1", "ABC_Camera_2", "ABC_Camera_3"]

        # Creating threads for each camera
        threads = []
        for sn, directory in zip(serial_numbers, directories):
            thread = threading.Thread(target=handle_camera, args=(sn, directory))
            threads.append(thread)
            thread.start()

        # Wait for all threads to complete
        for thread in threads:
            thread.join()

    finally:
        print("Image capture and intrinsics saving completed for all cameras.")

if __name__ == '__main__':
    start_capture()
