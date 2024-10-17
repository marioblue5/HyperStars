import pyrealsense2 as rs
import multiprocessing
import os
import time

# Function to ensure directory creation
def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to handle recording from one camera
def record_bag(serial_number, duration, output_directory):
    print(f"Starting recording for camera {serial_number}...")
    
    # Create pipeline and configuration for each camera
    pipeline = rs.pipeline()
    config = rs.config()
    
    # Set the camera by serial number
    config.enable_device(serial_number)
    
    # Enable streams for depth and color
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 15)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 15)
    
    # Set the output file path for the .bag file
    bag_file = os.path.join(output_directory, f"camera_{serial_number}.bag")
    config.enable_record_to_file(bag_file)
    
    # Start the pipeline
    time.sleep(2)
    pipeline.start(config)
    
    try:
        frame_count = 0
        start_time = time.time()
        
        # Capture frames for the specified duration
        while time.time() - start_time < duration:
            frames = pipeline.wait_for_frames()
            frame_count += 1
    
    except Exception as e:
        print(f"Error with camera {serial_number}: {e}")
    
    finally:
        pipeline.stop()
        print(f"Recording for camera {serial_number} finished. Total frames: {frame_count}")

# Multiprocessing function to handle multiple cameras simultaneously
def record_multiple_cameras(duration, output_directory):
    context = rs.context()
    devices = context.devices
    
    if len(devices) < 1:
        raise ValueError("No cameras found.")
    
    ensure_folder(output_directory)
    
    # Create a process for each camera
    processes = []
    for device in devices:
        serial_number = device.get_info(rs.camera_info.serial_number)
        process = multiprocessing.Process(target=record_bag, args=(serial_number, duration, output_directory))
        processes.append(process)
        process.start()
    
    # Wait for all processes to finish
    for process in processes:
        process.join()
    
    print("All camera recordings have completed.")

if __name__ == '__main__':
    duration = int(input("Enter the recording duration in seconds: "))
    output_directory = input("Enter the output directory to save the .bag files: ")
    record_multiple_cameras(duration, output_directory)

