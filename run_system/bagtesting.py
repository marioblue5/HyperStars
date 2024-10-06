import pyrealsense2 as rs
import os
import time

# Function to create a folder if it doesn't exist
def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# Initialize camera pipeline with the highest resolution for the D405
def initialize_camera(serial_number, output_path):
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_device(serial_number)

    # Enable the highest resolution (1280x720) at 30 FPS
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    # Enable recording to a .bag file
    config.enable_record_to_file(output_path)

    return pipeline, config

# Capture and record .bag file
def capture_bag(pipeline, config, duration=15):
    frame_count = 0
    pipeline.start(config)

    # Timer for diagnostics
    start_time = time.time()

    while time.time() - start_time < duration:
        frameset = pipeline.wait_for_frames()
        frame_count += 1

    pipeline.stop()

    end_time = time.time()
    return frame_count, start_time, end_time

# Function to handle each camera sequentially
def handle_camera(serial_number, directory):
    print(f"Starting capture for camera {serial_number}...")

    # Set the file path for saving the .bag file
    bag_file_path = os.path.join(directory, f"camera_{serial_number}.bag")
    pipeline, config = initialize_camera(serial_number, bag_file_path)

    # Timer diagnostics
    start_timer = time.time()
    
    # Capture frames and get diagnostics
    frame_count, capture_start, capture_end = capture_bag(pipeline, config)
    
    end_timer = time.time()
    total_time = end_timer - start_timer
    capture_duration = capture_end - capture_start

    print(f"Total frames captured by camera {serial_number}: {frame_count}")
    print(f"Capture duration: {capture_duration:.2f} seconds")
    print(f"Total time including setup: {total_time:.2f} seconds")
    print(f"Average frame rate: {frame_count / capture_duration:.2f} FPS")
    print(f"Bag file saved to {bag_file_path}")

def start_capture():
    context = rs.context()
    if len(context.devices) < 1:
        raise ValueError("No D405 camera detected")

    base_directory = input("Enter the directory name for saving the datasets: ")
    ensure_folder(os.path.join("datasets", base_directory))

    # Loop through each camera sequentially
    for device in context.devices:
        serial_number = device.get_info(rs.camera_info.serial_number)
        directory = os.path.join("datasets", base_directory, f"Camera_{serial_number}")
        ensure_folder(directory)
        handle_camera(serial_number, directory)

    print("All camera captures and saves have completed.")

if __name__ == '__main__':
    start_capture()
