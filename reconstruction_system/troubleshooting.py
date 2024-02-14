import open3d as o3d
import numpy as np

pcd = o3d.geometry.PointCloud()
# Assuming you have some points to add to pcd
pcd.points = o3d.utility.Vector3dVector(np.random.rand(100, 3))

pcd_name = "test.ply"
result = o3d.io.write_point_cloud(pcd_name, pcd,'auto', False, False, True)
print("Write result:", result)
