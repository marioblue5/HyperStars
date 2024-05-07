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

def main():
    # Ensure output directory exists
    if not os.path.exists('output'):
        os.mkdir('output')

    # Initialize RealSense context
    context = rs.context()
    devices = context.query_devices()
    serial_numbers = [device.get_info(rs.camera_info.serial_number) for device in devices]

    if len(serial_numbers) < 3:
        raise ValueError("Three cameras are required but only found " + str(len(serial_numbers)))

    # Set up cameras
    pipelines = [setup_camera(sn) for sn in serial_numbers]
    try:
        num_frames = 150
        for i in range(num_frames):
            for index, pipeline in enumerate(pipelines):
                frames = pipeline.wait_for_frames()
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()
                if not depth_frame or not color_frame:
                    continue

                # Save the frames
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())
                save_image(f'output/depth_{serial_numbers[index]}_{i}.png', depth_image)
                save_image(f'output/color_{serial_numbers[index]}_{i}.jpg', color_image, is_color=True)

    finally:
        for pipeline in pipelines:
            pipeline.stop()

if __name__ == "__main__":
    main()
