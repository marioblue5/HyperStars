import pyrealsense2 as rs
import numpy as np
import cv2
import os

# Setup directories for each camera's images
folders = ['Camera1', 'Camera2', 'Camera3']
for folder in folders:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Configure depth and color streams for each camera
pipeline1 = rs.pipeline()
pipeline2 = rs.pipeline()
pipeline3 = rs.pipeline()
config1 = rs.config()
config2 = rs.config()
config3 = rs.config()

# Enable all connected devices
config1.enable_all_streams()
config2.enable_all_streams()
config3.enable_all_streams()

# Start the configured pipelines
pipeline1.start(config1)
pipeline2.start(config2)
pipeline3.start(config3)

try:
    # Capture 100 images from each camera
    for i in range(100):
        # Wait for a coherent pair of frames: depth and color
        frames1 = pipeline1.wait_for_frames()
        frames2 = pipeline2.wait_for_frames()
        frames3 = pipeline3.wait_for_frames()

        color_frame1 = frames1.get_color_frame()
        color_frame2 = frames2.get_color_frame()
        color_frame3 = frames3.get_color_frame()

        # Convert images to numpy arrays
        color_image1 = np.asanyarray(color_frame1.get_data())
        color_image2 = np.asanyarray(color_frame2.get_data())
        color_image3 = np.asanyarray(color_frame3.get_data())

        # Save images to respective folders
        cv2.imwrite(f'Camera1/img_{i}.png', color_image1)
        cv2.imwrite(f'Camera2/img_{i}.png', color_image2)
        cv2.imwrite(f'Camera3/img_{i}.png', color_image3)

finally:
    # Stop streaming
    pipeline1.stop()
    pipeline2.stop()
    pipeline3.stop()