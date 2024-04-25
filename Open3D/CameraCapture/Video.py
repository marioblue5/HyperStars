import pyrealsense2 as rs
import numpy as np
import cv2
import os

# Function to create folder if it doesn't exist
def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

# Setting up each camera
def setup_camera(serial_number):
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_device(serial_number)
    config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
    pipeline.start(config)
    return pipeline

# Capture and save a frame from each camera
def capture_frame(pipeline, folder_name, frame_number):
    ensure_folder(folder_name)
    frames = pipeline.wait_for_frames()
    color_frame = frames.get_color_frame()
    if not color_frame:
        return False
    color_image = np.asanyarray(color_frame.get_data())
    cv2.imwrite(f"{folder_name}/frame-{frame_number}.jpg", color_image)
    return True

try:
    # Find connected devices
    context = rs.context()
    devices = context.query_devices()
    serial_numbers = [device.get_info(rs.camera_info.serial_number) for device in devices]

    if len(serial_numbers) < 3:
        raise ValueError("Three D405 cameras are not connected")

    # Setup pipelines for each camera
    pipelines = [setup_camera(sn) for sn in serial_numbers]

    # Directory names for each camera
    directories = ["Camera_1", "Camera_2", "Camera_3"]

    # Capture 100 frames from each camera
    for i in range(100):
        for pipeline, directory in zip(pipelines, directories):
            capture_frame(pipeline, directory, i)

finally:
    # Stop all pipelines
    for pipeline in pipelines:
        pipeline.stop()

print("Image capture completed for all cameras.")
