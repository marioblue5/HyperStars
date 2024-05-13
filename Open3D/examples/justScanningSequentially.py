import pyrealsense2 as rs
import os
import json
import time

# Initialization

# Function to create a folder if it doesn't exist
def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to setup each camera
def setup_camera(serial_number):
    print(serial_number)
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_device(serial_number)
    config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
    return pipeline, config

# Function to save camera intrinsics to a JSON file
def save_intrinsic_as_json(directory, pipeline):
    ensure_folder(directory)
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    intrinsics = color_frame.profile.as_video_stream_profile().intrinsics
    filename = os.path.join(directory, "intrinsics.json")
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

# Function to record data into a ROS bag file
def record_to_rosbag(config, directory, duration, pipeline):
    ensure_folder(directory)
    bag_filename = os.path.join(directory, "realsense.bag")
    config.enable_record_to_file(bag_filename)
    pipeline.start(config)
    frame = 0
    try:
        print(f"Recording to {bag_filename} for {duration} seconds...")
        start_time = time.time()
        while time.time() - start_time < duration:
            pipeline.wait_for_frames()
            frame += 1
    finally:
        pipeline.stop()
        print(f"Number of frames in this {duration} second interval: {frame}")
        print(f"Finished recording to {bag_filename}")

def start_capture():
    try:
        # Prompt user for directory name
        user_input = input("Enter the directory name for saving the datasets: ")
        base_directory = os.path.join("datasets", user_input)
        ensure_folder(base_directory)
        # Find connected devices
        context = rs.context()
        devices = context.query_devices()
        serial_numbers = [device.get_info(rs.camera_info.serial_number) for device in devices]

        if len(serial_numbers) < 3:
            raise ValueError("Three D405 cameras are not connected")

        # Directory names for each camera
        directories = [os.path.join(base_directory,f"Camera_{i+1}") for i in range(len(serial_numbers))]

        # Process each camera sequentially
        for sn, directory in zip(serial_numbers, directories):
            pipeline, config = setup_camera(sn)
            handle_camera(sn, directory, pipeline, config)

    finally:
        print("ROS bag capture and intrinsics saving completed for all cameras.")

def handle_camera(serial_number, directory, pipeline, config):
    duration = 10  # Record for 10 seconds; adjust as needed
    record_to_rosbag(config, directory, duration, pipeline)
    save_intrinsic_as_json(directory, pipeline)

if __name__ == '__main__':
    start_capture()
