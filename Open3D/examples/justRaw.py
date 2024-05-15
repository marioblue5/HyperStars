import pyrealsense2 as rs
import numpy as np
import os
import time

# Function to create a folder if it doesn't exist
def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# Initialize camera pipeline
def initialize_camera(serial_number):
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_device(serial_number)
    config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
    return pipeline, config

# Capture raw frames and keep them in memory
def capture_frames(pipeline, config, duration=5):
    try:
        pipeline.start(config)
        start_time = time.time()
        raw_depth_frames = []

        while time.time() - start_time < duration:
            frameset = pipeline.wait_for_frames()
            depth_frame = frameset.get_depth_frame()
            if not depth_frame:
                continue
            # Convert frame to numpy array and store it
            depth_data = np.asanyarray(depth_frame.get_data())
            raw_depth_frames.append(depth_data)
            frameset.keep()

        return raw_depth_frames
    finally:
        pipeline.stop()

# Save raw depth data to binary files
def save_raw_data(raw_depth_frames, directory):
    ensure_folder(directory)
    depth_dir = os.path.join(directory, 'Depth')
    ensure_folder(depth_dir)

    for i, depth_data in enumerate(raw_depth_frames):
        depth_path = os.path.join(depth_dir, f'raw_depth_{i:03}.bin')
        # Save depth data as binary
        depth_data.tofile(depth_path)

def handle_camera(serial_number, directory):
    print(f"Starting capture for camera {serial_number}...")
    pipeline, config = initialize_camera(serial_number)
    raw_depth_frames = capture_frames(pipeline, config)
    save_raw_data(raw_depth_frames, directory)
    print(f"Raw depth frames saved for camera {serial_number}")

def start_capture():
    context = rs.context()
    if len(context.devices) < 1:
        raise ValueError("Not enough cameras connected")

    base_directory = input("Enter the directory name for saving the datasets: ")
    directories = [os.path.join("datasets", base_directory, "Camera_1")]
    serial_numbers = [device.get_info(rs.camera_info.serial_number) for device in context.devices]

    handle_camera(serial_numbers[0], directories[0])
    print("All camera captures and saves have completed.")

if __name__ == '__main__':
    start_capture()
