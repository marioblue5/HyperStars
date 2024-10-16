import open3d as o3d
import numpy as np

# Create a simple point cloud and rotate it
pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(np.random.rand(10, 3))

rotation = np.array([0, 0, np.pi/2], dtype=np.float64)
R = o3d.geometry.get_rotation_matrix_from_xyz(rotation)

pcd.rotate(R)

# Visualize the point cloud
o3d.visualization.draw_geometries([pcd])
