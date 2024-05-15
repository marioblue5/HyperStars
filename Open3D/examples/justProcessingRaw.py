import pyrealsense2 as rs
import numpy as np
import cv2
import os

# Configuration constants
DEPTH_WIDTH = 848
DEPTH_HEIGHT = 480
DEPTH_DTYPE = np.uint16  # 16-bit depth values

# Function to read a binary depth file
def read_depth_file(filepath):
    # Read the binary data and reshape based on how it was saved
    depth_data = np.fromfile(filepath, dtype=DEPTH_DTYPE)
    depth_data = depth_data.reshape((DEPTH_HEIGHT, DEPTH_WIDTH))
    return depth_data

# Apply RealSense filters to a numpy array representing depth data
def apply_filters(depth_array):
    # Create a pyrealsense2 depth frame from the numpy array
    depth_frame = rs.frame_from_data(rs.format.z16, rs.stream.depth, depth_array)
    
    # Initialize filters
    decimation = rs.decimation_filter()
    spatial = rs.spatial_filter()
    temporal = rs.temporal_filter()
    hole_filling = rs.hole_filling_filter()

    # Apply filters
    depth_frame = decimation.process(depth_frame)
    depth_frame = spatial.process(depth_frame)
    depth_frame = temporal.process(depth_frame)
    depth_frame = hole_filling.process(depth_frame)

    # Convert processed frame back to numpy array
    filtered_depth_array = np.asanyarray(depth_frame.get_data())
    return filtered_depth_array

# Save a depth image as a PNG file using a color map
def save_depth_image(depth_array, filepath):
    # Apply a colormap for visualization
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_array, alpha=0.03), cv2.COLORMAP_JET)
    cv2.imwrite(filepath, depth_colormap)

def process_and_save_depth_images(input_dir, output_dir):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for filename in os.listdir(input_dir):
        if filename.endswith(".bin"):
            file_path = os.path.join(input_dir, filename)
            depth_array = read_depth_file(file_path)
            filtered_depth_array = apply_filters(depth_array)
            output_filepath = os.path.join(output_dir, filename.replace('.bin', '.png'))
            save_depth_image(filtered_depth_array, output_filepath)
            print(f"Processed and saved: {output_filepath}")

def main():
    input_dir = input("Enter the directory containing the depth .bin files: ")
    output_dir = input("Enter the directory to save processed images: ")
    process_and_save_depth_images(input_dir, output_dir)
    print("All depth images have been processed and saved.")

if __name__ == '__main__':
    main()
