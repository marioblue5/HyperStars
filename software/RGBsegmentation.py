import open3d as o3d
import numpy as np
import matplotlib.pyplot as plt
import copy

# Load your mesh
#mesh_path = "C:/Users/molina.mario/Desktop/mario/datasets/20241014_Data/Right/PreviousAttempts/Attempt2/output_slac_mesh.ply"  # Replace with the path to your mesh file
mesh_path = "C:/Users/slantin/Desktop/Code/HyperStars/software/right_slac_mesh.ply"
mesh = o3d.io.read_triangle_mesh(mesh_path)

# Convert the mesh to a point cloud (sample points from the surface)
pcd = mesh.sample_points_uniformly(number_of_points=1000000)  # Adjust points as needed

# Access the point cloud's points as a NumPy array
points = np.asarray(pcd.points)

# Define the rotation matrix (180-degree flip around Z-axis)
#R = np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]])
R = np.array([[ 1, 0, 0], [0,  -1, 0], [0, 0, -1]])

# Rotate the points
rotated_points = np.dot(points, R.T)

# Update the point cloud with the rotated points
pcd.points = o3d.utility.Vector3dVector(rotated_points)

# The rotated point cloud is still tilted, so now we segment out the white NFT channels, create a flat plane using plane segmentation
# and tilt the point cloud again such that this plane is now 0 degrees

# Save the intermediate point cloud (converted from the mesh)
#o3d.io.write_point_cloud("C:/Users/molina.mario/Desktop/mario/datasets/20241014_Data/Right/PreviousAttempts/Attempt2/intermediate_point_cloud.ply", pcd)
#o3d.io.write_point_cloud("C:/Users/slantin/Desktop/Code/HyperStars/software/right_rotated.ply", pcd)

# Get color information from point cloud
colors = np.asarray(pcd.colors)  # Extract colors (in RGB format)
# Check if there are colors available
if colors.size == 0:
    raise ValueError("No color information found in the point cloud!")
# Define RGB thresholds for green and red plants
# Adjust these values based on your specific plant color
# Define RGB thresholds for white (high values of R, G, and B)
# Typically, white will have RGB values close to 1.0 in normalized space
lower_white = np.array([0.4, 0.4, 0.4])  # Lower bound for white [R, G, B]
upper_white = np.array([1.0, 1.0, 1.0])  # Upper bound for white [R, G, B]

upper_black = np.array([0.2, 0.2, 0.2])
upper_green = np.array([0.0,0.95,0.0])
upper_red = np.array([0.95,0.0,0.0])

red_green_condition = (colors[:, 0] > colors[:, 2]) & (colors[:, 1] > colors[:, 2])
white_condition = np.all((colors >= lower_white) & (colors <= upper_white), axis=1)
black_condition = np.all(colors <= upper_black, axis=1)

# Create a mask for white points (everything that is white)
mask_white = np.all((colors >= lower_white) & (colors <= upper_white), axis=1)

# Apply the mask to the point cloud to keep only white points
white_points = np.asarray(pcd.points)[mask_white]
white_colors = colors[mask_white]

# Create a new point cloud with the non-white points
pcd_white = o3d.geometry.PointCloud()
pcd_white.points = o3d.utility.Vector3dVector(white_points)
pcd_white.colors = o3d.utility.Vector3dVector(white_colors)

# Visualize the rotated point cloud
#o3d.visualization.draw_geometries([pcd_white]) # shows that the majority of points left are in the NFT channel plane--use this to establish the zero height and angle

#-----
plane_model, inliers = pcd.segment_plane(distance_threshold=0.01,
                                         ransac_n=3,
                                         num_iterations=1000)
[a, b, c, d] = plane_model
print(f"Plane equation: {a:.2f}x + {b:.2f}y + {c:.2f}z + {d:.2f} = 0")

# Given plane normal from the plane equation
plane_normal = np.array([a, b, c], dtype=np.float64)

# Desired alignment (align plane to be parallel to the XY plane, meaning its normal should align with the Z-axis)
target_normal = np.array([0, 0, 1], dtype=np.float64)

# Step 1: Normalize both vectors
plane_normal = plane_normal / np.linalg.norm(plane_normal)
target_normal = target_normal / np.linalg.norm(target_normal)

# Step 2: Compute the cross product (rotation axis) and the angle (in radians)
rotation_axis = np.cross(plane_normal, target_normal)
sin_angle = np.linalg.norm(rotation_axis)  # The sine of the angle is the magnitude of the cross product
cos_angle = np.dot(plane_normal, target_normal)  # The cosine of the angle is the dot product

# Step 3: Handle the case where the plane normal is already aligned (no need to rotate)
if sin_angle < 1e-6:
    rotation_matrix = np.eye(3)  # Identity matrix, no rotation needed
else:
    # Normalize the rotation axis
    rotation_axis = rotation_axis / sin_angle

    # Step 4: Compute the rotation matrix using the axis-angle formula
    ux, uy, uz = rotation_axis
    tilt_rotation_matrix = np.array([
        [cos_angle + ux**2 * (1 - cos_angle),      ux*uy*(1 - cos_angle) - uz*sin_angle, ux*uz*(1 - cos_angle) + uy*sin_angle],
        [uy*ux*(1 - cos_angle) + uz*sin_angle, cos_angle + uy**2 * (1 - cos_angle),      uy*uz*(1 - cos_angle) - ux*sin_angle],
        [uz*ux*(1 - cos_angle) - uy*sin_angle, uz*uy*(1 - cos_angle) + ux*sin_angle, cos_angle + uz**2 * (1 - cos_angle)]
    ])

flipped_points = np.asarray(pcd.points)

# Step 6: Apply the combined rotation to the points
tilted_points = np.dot(flipped_points, tilt_rotation_matrix.T)

# Update the point cloud with the rotated points
pcd.points = o3d.utility.Vector3dVector(tilted_points)

# Visualize the rotated point cloud
#o3d.visualization.draw_geometries([pcd]) # see that the point cloud is now rotated as we expect

# ------

# Create a mask for non-white points (everything that is NOT white)
#mask_non_white = ~np.all((colors >= lower_white) & (colors <= upper_white) & (colors >= upper_black) & ( red_condition | green_condition ), axis=1)
mask_non_white = ~(white_condition | black_condition) & (red_green_condition)


# Apply the mask to the point cloud to keep only non-white points
non_white_points = np.asarray(pcd.points)[mask_non_white]
non_white_colors = colors[mask_non_white]

# Create a new point cloud with the non-white points
pcd_non_white = o3d.geometry.PointCloud()
pcd_non_white.points = o3d.utility.Vector3dVector(non_white_points)
pcd_non_white.colors = o3d.utility.Vector3dVector(non_white_colors)

# DBSCAN to remove small clusters

labels = np.array(pcd_non_white.cluster_dbscan(eps=0.02, min_points=850, print_progress=True))

# Identify the number of clusters and noise (label = -1 is considered noise)
max_label = labels.max()
print(f"Found {max_label + 1} clusters and noise")

min_cluster_size = 50
filtered_points = np.where(labels >= 0)[0]  # Exclude noise points (label = -1)

# For each cluster, filter out the clusters that are too small
for cluster_label in range(max_label + 1):
    cluster_indices = np.where(labels == cluster_label)[0]
    if len(cluster_indices) < min_cluster_size:
        filtered_points = np.setdiff1d(filtered_points, cluster_indices)

# Extract the remaining points from the point cloud
filtered_pcd = pcd_non_white.select_by_index(filtered_points)


# do another plane segmentation to only get lettuce layer and assign the bottom of this to be zero

# Step 1: Perform plane segmentation with a larger distance threshold of 0.3
plane_model, inliers = filtered_pcd.segment_plane(distance_threshold=0.05,
                                                  ransac_n=3,
                                                  num_iterations=1000)

# Plane equation: ax + by + cz + d = 0
a_thresh, b_thresh, c_thresh, d_thresh = plane_model
print(f"Plane equation: {a_thresh:.2f}x + {b_thresh:.2f}y + {c_thresh:.2f}z + {d_thresh:.2f} = 0")

plane_points = filtered_pcd.select_by_index(inliers)

plane_points_np = np.asarray(plane_points.points)
min_z = plane_points_np[:, 2].min()  # Find the minimum Z value

plane_points_np[:, 2] -= min_z
plane_points.points = o3d.utility.Vector3dVector(plane_points_np)

o3d.visualization.draw_geometries([plane_points])

#o3d.io.write_point_cloud("C:/Users/molina.mario/Desktop/mario/datasets/20241014_Data/Right/PreviousAttempts/Attempt2/segmented_plants.ply", pcd_non_white)
o3d.io.write_point_cloud("C:/Users/slantin/Desktop/Code/HyperStars/software/right_segmented_aligned_plants.ply", plane_points)

