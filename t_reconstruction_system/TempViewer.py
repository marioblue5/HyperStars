
import numpy as np
import open3d as o3d

# Load your mesh or point cloud
# For mesh:
mesh_or_point_cloud = o3d.io.read_triangle_mesh('/home/stella/open3d_data/extract/LoungeRGBDImages/fragments/unified_scene.ply')  # Replace 'your_file.ply' with your mesh file path
# For point cloud:
# mesh_or_point_cloud = o3d.io.read_point_cloud('your_file.pcd')  # Replace 'your_file.pcd' with your point cloud file path

# If it's a mesh, compute normals to enhance lighting
if isinstance(mesh_or_point_cloud, o3d.geometry.TriangleMesh):
    mesh_or_point_cloud.compute_vertex_normals()

# Initialize the visualizer
vis = o3d.visualization.Visualizer()
vis.create_window()

# Add the geometry to the visualizer
vis.add_geometry(mesh_or_point_cloud)

# Example: Set the background color to light gray (values between 0 and 1 for RGB)
vis.get_render_option().background_color = np.asarray([0.8, 0.8, 0.8])
view_control = vis.get_view_control()
cam_params = view_control.convert_to_pinhole_camera_parameters()
cam_params.extrinsic = np.array([[1, 0, 0, 0],  # You might need to adjust this matrix
                                 [0, 1, 0, 0],  # This row flips the Y axis
                                 [0, 0, -1, 0],  # This row flips the Z axis (assuming the camera is upside-down)
                                 [0, 0, 0, 1]])
# You can adjust more settings here, like lighting or camera view
# ...

# Run the visualizer
vis.run()
# Destroy the visualizer window
vis.destroy_window()
