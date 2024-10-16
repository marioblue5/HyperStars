# this script takes in an RGB segmented and aligned point cloud and uses the height of the points to detect wilting, a sign of water stress

import os
import re
import open3d as o3d
import numpy as np

def detect_water_stress(directory):

    #directory = where RGB segmented and aligned point clouds are stored, with timestamps according to below

    # Regex pattern to detect datetime in the format "YYYY-MM-DD_HH-MM-SS"
    datetime_pattern = re.compile(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}')

    # Get a list of .ply files that contain a valid datetime in their filename
    point_cloud_files = [
        f for f in os.listdir(directory)
        if f.endswith('.ply') and datetime_pattern.search(f)
    ]

    # Sort the files by modification time (newest first)
    point_cloud_files = sorted(point_cloud_files, key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)

    # Check if there are any valid files
    if point_cloud_files:
        # Load the most recent file
        most_recent_file = point_cloud_files[0]
        print(f"Most recent file with datetime: {most_recent_file}")
        pcd_path_curr = os.path.join(directory, most_recent_file)
        pcd_curr = o3d.io.read_point_cloud(pcd_path_curr)

        # Load the second most recent file or the same one if there's only one
        if len(point_cloud_files) > 1:
            second_most_recent_file = point_cloud_files[1]
            print(f"Second most recent file with datetime: {second_most_recent_file}")
            pcd_path_prev = os.path.join(directory, second_most_recent_file)
        else:
            # If only one file is available, load it twice
            print("Only one valid point cloud file found. Loading it twice.")
            pcd_path_prev = pcd_path_curr

        pcd_prev = o3d.io.read_point_cloud(pcd_path_prev)

        print(f"Loaded point clouds from: {pcd_path_curr} and {pcd_path_prev}")
    else:
        print("No valid point cloud files with datetime found.")
        return -1

    # Access the points from both point clouds
    points_curr = np.asarray(pcd_curr.points)
    points_prev = np.asarray(pcd_prev.points)

    # Calculate the average height (z-coordinate is the third column)
    avg_height_curr = np.mean(points_curr[:, 2])  # Average of z-coordinates from pcd_curr
    avg_height_prev = np.mean(points_prev[:, 2])  # Average of z-coordinates from pcd_prev

    # Compare average heights
    if avg_height_curr < 0.7 * avg_height_prev:
        return 1
    else:
        return 0

if __name__ == '__main__':
    detected = detect_water_stress(directory="C:/Users/slantin/Desktop/Code/HyperStars/software")
    print(detected)