import open3d as o3d

# Load a PLY file as a point cloud
point_cloud = o3d.io.read_point_cloud('/home/stella/open3d_data/extract/LoungeRGBDImages/slac/0.006/fragment_pcd_010.ply')

# Check the loaded point cloud
print(point_cloud)
# Visualize the point cloud
o3d.visualization.draw_geometries([point_cloud])
