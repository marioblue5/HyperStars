import pyrealsense2 as rs
import numpy as np
import cv2
import os
import time

# Function to create a folder if it doesn't exist
def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# Initialize camera pipeline
def initialize_camera():
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 90)
    config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 90)
    return pipeline, config

# Capture raw frames and keep them in memory
def capture_frames(pipeline, config, duration=5):
    try:
        frame_count = 0
        pipeline.start(config)
        start_time = time.time()
        raw_frames = []

        while time.time() - start_time < duration:
            frameset = pipeline.wait_for_frames()
            raw_frames.append(frameset)
            frameset.keep()
            frame_count += 1

        return raw_frames
    finally:
        print(f"Total frames in {duration} seconds: {frame_count}")
        pipeline.stop()

# Process and save frames to disk
def process_and_save_frames(raw_frames, directory):
    ensure_folder(directory)
    depth_dir = os.path.join(directory, 'Depth')
    color_dir = os.path.join(directory, 'Color')
    ensure_folder(depth_dir)
    ensure_folder(color_dir)
    
    align = rs.align(rs.stream.color)

    for i, frameset in enumerate(raw_frames):
        # Align the frames
        aligned_frames = align.process(frameset)
        depth_frame = aligned_frames.get_depth_frame()
        color_frame = aligned_frames.get_color_frame()

        # Convert images to numpy arrays
        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Save the images
        depth_path = os.path.join(depth_dir, f'depth_{i:03}.png')
        color_path = os.path.join(color_dir, f'color_{i:03}.png')
        cv2.imwrite(depth_path, depth_image)
        cv2.imwrite(color_path, color_image)

def main():
    directory = input("Enter the directory name for saving the datasets: ")
    pipeline, config = initialize_camera()
    raw_frames = capture_frames(pipeline, config)
    process_and_save_frames(raw_frames, directory)
    print("Frames have been processed and saved successfully.")

if __name__ == '__main__':
    main()
