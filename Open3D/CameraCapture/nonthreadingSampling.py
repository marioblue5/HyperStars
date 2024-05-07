import pyrealsense2 as rs
import numpy as np
import cv2
import os

def save_image(filename, image, is_color=False):
    """Save a color or depth image."""
    if is_color:
        cv2.imwrite(filename, image)  # Save color image directly
    else:
        # Convert depth image to color map for better visualization
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(image, alpha=0.09), cv2.COLORMAP_JET)
        cv2.imwrite(filename, depth_colormap)

def setup_camera(serial_number):
    """Set up and return a RealSense pipeline for a given serial number."""
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_device(serial_number)
    config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
    pipeline.start(config)
    return pipeline

def capture_frames(pipeline, device_id, output_folder, num_frames=150):
    """Capture a number of frames from a camera and save them to disk."""
    for i in range(num_frames):
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()
        color_frame = frames.get_color_frame()
        if not depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())
        save_image(os.path.join(output_folder, f'depth_{i}.png'), depth_image)
        save_image(os.path.join(output_folder, f'color_{i}.jpg'), color_image, is_color=True)

def main():
    # Ensure the output directories exist
    base_dir = 'output'
    if not os.path.exists(base_dir):
        os.mkdir(base_dir)

    directories = ['1', '2', '3']  # Folder names for each camera
    for d in directories:
        if not os.path.exists(os.path.join(base_dir, d)):
            os.mkdir(os.path.join(base_dir, d))

    # Initialize RealSense context
    context = rs.context()
    devices = context.query_devices()
    if len(devices) < 3:
        raise ValueError("Three cameras are required but only found " + str(len(devices)))

    # Set up cameras and capture frames
    for index, device in enumerate(devices):
        serial_number = device.get_info(rs.camera_info.serial_number)
        pipeline = setup_camera(serial_number)
        capture_frames(pipeline, serial_number, os.path.join(base_dir, directories[index]))

        # Stop the pipeline after capturing the frames
        pipeline.stop()

if __name__ == "__main__":
    main()
