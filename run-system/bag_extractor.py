import pyrealsense2 as rs
import numpy as np
import cv2
import os
import json

def ensure_folder(folder):
    if not os.path.exists(folder):
        os.makedirs(folder)

def save_intrinsic_as_json(filename, frame):
    intrinsics = frame.profile.as_video_stream_profile().intrinsics
    with open(filename, 'w') as outfile:
        json.dump(
            {
                'width': intrinsics.width,
                'height': intrinsics.height,
                'intrinsic_matrix': [
                    intrinsics.fx, 0, 0, 0, intrinsics.fy, 0, intrinsics.ppx,
                    intrinsics.ppy, 1
                ]
            },
            outfile,
            indent=4
        )

def count_frames_and_save_rgb_depth_filtered(bag_file, output_folder):
    # Create separate folders for color and filtered depth images
    color_folder = os.path.join(output_folder, "color")
    depth_folder = os.path.join(output_folder, "depth")
    
    ensure_folder(color_folder)
    ensure_folder(depth_folder)

    # Initialize the pipeline for playback
    pipeline = rs.pipeline()
    config = rs.config()
    
    # Configure the pipeline to read from the provided .bag file
    config.enable_device_from_file(bag_file, repeat_playback=False)
    
    # Enable both color and depth streams
    config.enable_stream(rs.stream.color)
    config.enable_stream(rs.stream.depth)
    
    # Start the pipeline
    pipeline.start(config)
    
    # Get the playback device
    playback = pipeline.get_active_profile().get_device().as_playback()
    playback.set_real_time(False)  # Disable real-time playback to read faster
    
    # Initialize filters
    align = rs.align(rs.stream.color)
    depth_to_disparity = rs.disparity_transform(True)
    disparity_to_depth = rs.disparity_transform(False)
    spatial = rs.spatial_filter()
    temporal = rs.temporal_filter()

    # Set filter options
    spatial.set_option(rs.option.filter_magnitude, 2)
    spatial.set_option(rs.option.filter_smooth_alpha, 0.6)
    spatial.set_option(rs.option.filter_smooth_delta, 50)
    spatial.set_option(rs.option.holes_fill, 0)  # Disable hole filling
    temporal.set_option(rs.option.filter_smooth_alpha, 1)
    temporal.set_option(rs.option.filter_smooth_delta, 20)
    temporal.set_option(rs.option.holes_fill, 2)
    
    frame_count = 1  # Start counting frames from 1 (for 000001.png)
    last_timestamp = None  # Track the timestamp of the last frame
    intrinsic_saved = False  # Ensure we only save intrinsics once

    try:
        while True:
            # Wait for the next set of frames (blocking call)
            frames = pipeline.wait_for_frames()

            # Align frames to the color stream
            aligned_frames = align.process(frames)
            color_frame = aligned_frames.get_color_frame()
            depth_frame = aligned_frames.get_depth_frame()

            # If no color or depth frame is available, skip
            if not color_frame or not depth_frame:
                continue

            # Save intrinsics on the first valid color frame
            if not intrinsic_saved:
                intrinsic_file_path = os.path.join(output_folder, 'camera_intrinsics.json')
                save_intrinsic_as_json(intrinsic_file_path, color_frame)
                print(f"Intrinsics saved to {intrinsic_file_path}")
                intrinsic_saved = True

            # Get the timestamp of the current frame
            current_timestamp = color_frame.get_timestamp()

            # Check if the current frame is a duplicate by comparing timestamps
            if last_timestamp is not None and current_timestamp == last_timestamp:
                print(f"Duplicate frame at timestamp {current_timestamp}, skipping...")
                continue  # Skip this frame if it's a duplicate

            # Apply filters to the depth frame
            disparity_frame = depth_to_disparity.process(depth_frame)
            filtered_disparity_frame = spatial.process(disparity_frame)
            filtered_disparity_frame = temporal.process(filtered_disparity_frame)
            filtered_depth_frame = disparity_to_depth.process(filtered_disparity_frame)

            # Convert images to numpy arrays
            color_image = np.asanyarray(color_frame.get_data())
            filtered_depth_image = np.asanyarray(filtered_depth_frame.get_data())

            # Save the RGB and filtered depth images
            color_image_path = os.path.join(color_folder, f"{frame_count:06}.png")
            filtered_depth_image_path = os.path.join(depth_folder, f"{frame_count:06}.png")
            cv2.imwrite(color_image_path, color_image)
            cv2.imwrite(filtered_depth_image_path, filtered_depth_image)

            # Update the last processed timestamp
            last_timestamp = current_timestamp

            # Increment the frame counter
            frame_count += 1
            print(f"Frame {frame_count - 1} processed and saved as {color_image_path} and {filtered_depth_image_path}")

    except RuntimeError as e:
        # If no more frames are available, stop the pipeline
        print("End of .bag file reached or error occurred:", e)
    
    finally:
        # Stop the pipeline
        pipeline.stop()
    
    print(f"Total frames processed and saved: {frame_count - 1}")

if __name__ == "__main__":
    bag_file_path = input("Enter the path to the .bag file: ")
    output_folder = input("Enter the output folder to save the images: ")
    
    count_frames_and_save_rgb_depth_filtered(bag_file_path, output_folder)
