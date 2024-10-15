import open3d as o3d
import numpy as np
import cv2
import matplotlib.pyplot as plt

# Load your mesh
mesh_path = "C:/Users/molina.mario/Desktop/mario/datasets/20241014_Data/Right/PreviousAttempts/Attempt2/output_slac_mesh.ply"  # Replace with the path to your mesh file
mesh = o3d.io.read_triangle_mesh(mesh_path)

# Convert the mesh to a point cloud (sample points from the surface)
pcd = mesh.sample_points_uniformly(number_of_points=1000000)  # Adjust points as needed

# Save the intermediate point cloud (converted from the mesh)
o3d.io.write_point_cloud("C:/Users/molina.mario/Desktop/mario/datasets/20241014_Data/Right/PreviousAttempts/Attempt2/intermediate_point_cloud.ply", pcd)

# Get color information from point cloud
colors = np.asarray(pcd.colors)  # Extract colors (in RGB format)
print(colors[1])
print(colors[235])
print(colors[4232])
# Check if there are colors available
if colors.size == 0:
    raise ValueError("No color information found in the point cloud!")
# Define RGB thresholds for green and red plants
# Adjust these values based on your specific plant color
# Define RGB thresholds for white (high values of R, G, and B)
# Typically, white will have RGB values close to 1.0 in normalized space
lower_white = np.array([0.2, 0.2, 0.2])  # Lower bound for white [R, G, B]
upper_white = np.array([1.0, 1.0, 1.0])  # Upper bound for white [R, G, B]

# Create a mask for non-white points (everything that is NOT white)
mask_non_white = ~np.all((colors >= lower_white) & (colors <= upper_white), axis=1)

# Apply the mask to the point cloud to keep only non-white points
non_white_points = np.asarray(pcd.points)[mask_non_white]
non_white_colors = colors[mask_non_white]

# Create a new point cloud with the non-white points
pcd_non_white = o3d.geometry.PointCloud()
pcd_non_white.points = o3d.utility.Vector3dVector(non_white_points)
pcd_non_white.colors = o3d.utility.Vector3dVector(non_white_colors)

o3d.io.write_point_cloud("C:/Users/molina.mario/Desktop/mario/datasets/20241014_Data/Right/PreviousAttempts/Attempt2/segmented_plants.ply", pcd_non_white)

# Visualize the segmented plant point cloud
o3d.visualization.draw_geometries([pcd_non_white],
                                  zoom=0.8,
                                  front=[-0.4999, -0.1659, -0.8499],
                                  lookat=[2.1813, 2.0619, 2.0999],
                                  up=[0.1204, -0.9852, 0.1215])
