import pyrealsense2 as rs
import numpy as np
import cv2
import threading
import os
import json

def save_image(filename, image, is_color=False):
    """Save a color or depth image."""
    if is_color:
        cv2.imwrite(filename, image)  # Save color image directly
    else:
        # Convert depth image to color map for better visualization
        depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(image, alpha=0.09), cv2.COLORMAP_JET)
        cv2.imwrite(filename, depth_colormap)

def save_intrinsics_as_json(path, profile):
    """Save the intrinsics of the camera to a JSON file."""
    intrinsics = profile.as_video_stream_profile().get_intrinsics()
    data = {
        "width": intrinsics.width,
        "height": intrinsics.height,
        "intrinsic_matrix": [intrinsics.fx, 0, 0, 0, intrinsics.fy, 0, intrinsics.ppx, intrinsics.ppy, 1]
    }
    with open(path, 'w') as file:
        json.dump(data, file, indent=4)

def setup_camera(serial_number):
    """Set up and return a RealSense pipeline for a given serial number."""
    pipeline = rs.pipeline()
    config = rs.config()
    config.enable_device(serial_number)
    config.enable_stream(rs.stream.depth, 848, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 848, 480, rs.format.bgr8, 30)
    pipeline.start(config)
    return pipeline

def camera_pipeline(pipeline, directory):
    """Capture, process, and save images from a single camera."""
    frame_counter = 0
    try:
        while True:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            depth_frame = frames.get_depth_frame()
            color_frame = frames.get_color_frame()
            if not depth_frame or not color_frame:
                continue

            # Convert frames to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())

            depth_file_name = os.path.join(directory, f'pre_depth_{frame_counter}.png')
            color_file_name = os.path.join(directory, f'pre_color_{frame_counter}.jpg')

            # Save pre-processed images
            save_image(depth_file_name, depth_image)
            save_image(color_file_name, color_image, is_color=True)

            # Apply filters
            processed_depth = depth_to_disparity.process(depth_frame)
            processed_depth = spatial.process(processed_depth)
            processed_depth = temporal.process(processed_depth)
            processed_depth = disparity_to_depth.process(processed_depth)

            # Convert processed depth frame to numpy array for saving
            processed_depth_image = np.asanyarray(processed_depth.get_data())
            post_depth_file_name = os.path.join(directory, f'post_depth_{frame_counter}.png')
            save_image(post_depth_file_name, processed_depth_image)

            # Increment frame counter
            frame_counter += 1
    finally:
        pipeline.stop()

def main():
    # Ensure the output directory exists
    if not os.path.exists('output'):
        os.mkdir('output')
    os.chdir('output')

    # Initialize RealSense context
    context = rs.context()
    devices = context.query_devices()
    serial_numbers = [device.get_info(rs.camera_info.serial_number) for device in devices]

    if len(serial_numbers) < 3:
        raise ValueError("Three D405 cameras are not connected")

    # Setup pipelines and directories for each camera
    pipelines = [setup_camera(sn) for sn in serial_numbers]
    directories = [f"Camera_{i+1}" for i in range(len(pipelines))]

    # Start threads for each camera
    threads = []
    for pipeline, directory in zip(pipelines, directories):
        thread = threading.Thread(target=camera_pipeline, args=(pipeline, directory))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete (they won't, as the script runs until manually stopped)
    for thread in threads:
        thread.join()

if __name__ == "__main__":
    main()
