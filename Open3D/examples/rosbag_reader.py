import pyrealsense2 as rs
import numpy as np
import cv2
import os

def extract_frames(bag_file_path, output_dir):
    # Configure the pipeline to stream from a .bag file
    config = rs.config()
    config.enable_device_from_file(bag_file_path, repeat_playback=False)

    # Start the pipeline
    pipeline = rs.pipeline()
    profile = pipeline.start(config)

    # Needed so frames don't get dropped during processing
    profile.get_device().as_playback().set_real_time(False)

    try:
        frame_number = 0
        while True:
            # Wait for the next set of frames from the bag file
            frames = pipeline.wait_for_frames()

            # Get color and depth frames
            color_frame = frames.get_color_frame()
            depth_frame = frames.get_depth_frame()

            # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())
            depth_image = np.asanyarray(depth_frame.get_data())

            # Ensure output directory exists
            os.makedirs(output_dir, exist_ok=True)

            # Save images
            color_img_path = os.path.join(output_dir, f"{frame_number}_color.png")
            depth_img_path = os.path.join(output_dir, f"{frame_number}_depth.png")
            cv2.imwrite(color_img_path, color_image)
            cv2.imwrite(depth_img_path, depth_image)

            frame_number += 1

    except RuntimeError as e:
        print(f'No more frames to read: {str(e)}')

    finally:
        # Stop the pipeline
        pipeline.stop()

if __name__ == '__main__':
    # Prompt user for directory name
    base_directory = input("Please make sure to have the directory inside the dataset folders. Enter the directory name: ")
    dataset_base_dir = os.path.join('datasets', base_directory)

    # Process each camera's bag file
    for i in range(1, 4):  # For cameras 1 to 3
        camera_dir = os.path.join(dataset_base_dir, f"Camera_{i}")
        bag_file_path = os.path.join(camera_dir, 'realsense.bag')
        output_dir = os.path.join(camera_dir, 'extracted_frames')

        # Check if the .bag file exists before attempting to extract frames
        if os.path.isfile(bag_file_path):
            print(f"Extracting frames from {bag_file_path} to {output_dir}")
            extract_frames(bag_file_path, output_dir)
        else:
            print(f"No .bag file found at {bag_file_path}. Please check the directory.")
