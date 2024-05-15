import pyrealsense2 as rs
import numpy as np
import cv2
import os
import time
import multiprocessing

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
    frame_count = 0
    pipeline.start(config)
    start_time = time.time()
    raw_frames = []

    while time.time() - start_time < duration:
        frameset = pipeline.wait_for_frames()
        raw_frames.append(frameset)
        frameset.keep()
        frame_count += 1

    pipeline.stop()
    return raw_frames, frame_count

# Process and save frames to disk
def process_and_save_frames(raw_frames, directory):
    ensure_folder(directory)
    depth_dir = os.path.join(directory, 'Depth')
    color_dir = os.path.join(directory, 'Color')
    ensure_folder(depth_dir)
    ensure_folder(color_dir)
    
    align = rs.align(rs.stream.color)

    for i, frameset in enumerate(raw_frames):
        aligned_frames = align.process(frameset)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        depth_path = os.path.join(depth_dir, f'depth_{i:03}.png')
        color_path = os.path.join(color_dir, f'color_{i:03}.png')
        cv2.imwrite(depth_path, depth_image)
        cv2.imwrite(color_path, color_image)

# Function to handle each camera in a separate process
def handle_camera(serial_number, directory):
    print(f"Starting capture for camera {serial_number}...")
    pipeline, config = initialize_camera(serial_number)
    raw_frames, frame_count = capture_frames(pipeline, config)
    print(f"Total frames captured by camera {serial_number}: {frame_count}")
    process_and_save_frames(raw_frames, directory)
    print(f"Frames processed and saved successfully for camera {serial_number}")

def start_capture():
    context = rs.context()
    if len(context.devices) < 2:
        raise ValueError("Three D405 cameras are not connected")

    base_directory = input("Enter the directory name for saving the datasets: ")
    directories = [os.path.join("datasets", base_directory, f"Camera_{i+1}") for i in range(3)]
    serial_numbers = [device.get_info(rs.camera_info.serial_number) for device in context.devices]

    processes = []
    for sn, directory in zip(serial_numbers, directories):
        ensure_folder(directory)  # Ensure each camera's directory is created before starting process
        process = multiprocessing.Process(target=handle_camera, args=(sn, directory))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    print("All camera captures and saves have completed.")

if __name__ == '__main__':
    start_capture()
