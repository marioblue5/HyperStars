import open3d as o3d
import numpy as np
import os
import json

# Configuration
path_to_fragments = "/home/stella/open3d_data/extract/LoungeRGBDImages/fragments"  # Update this path
num_fragments = 11  # Update this with the number of fragments you have

def load_pose_graph(pose_graph_path):
    with open(pose_graph_path, "r") as f:
        json_graph = json.load(f)
    return json_graph

def apply_transformation(pcd, transformation):
    return pcd.transform(transformation)


def main(path_to_fragments, num_fragments):
    unified_pcd = o3d.geometry.PointCloud()
    
    for i in range(num_fragments):
        pcd_path = os.path.join(path_to_fragments, f"fragment_pcd_{i:03d}.ply")
        pose_graph_path = os.path.join(path_to_fragments, f"fragment_posegraph_{i:03d}.json")
        
        # Load the point cloud
        pcd = o3d.io.read_point_cloud(pcd_path)
        
        # Load and apply the pose graph transformation
        pose_graph = load_pose_graph(pose_graph_path)
        for node in pose_graph["nodes"]:
            # Ensure it's a numpy array, then reshape to 4x4 matrix
            transformation_flat = np.array(node["pose"], dtype=np.float64)
            transformation_matrix = transformation_flat.reshape((4, 4))
            
            if transformation_matrix.shape == (4, 4):  # Ensure it's the correct shape
                pcd.transform(transformation_matrix)  # Apply the transformation
            else:
                print("Error: Transformation matrix is not 4x4.")
        
        # Add the transformed point cloud to the unified scene
        unified_pcd += pcd
    
    # Save the unified point cloud
    unified_scene_path = os.path.join(path_to_fragments, "unified_scene.ply")
    o3d.io.write_point_cloud(unified_scene_path, unified_pcd)
    print(f"Unified scene saved to: {unified_scene_path}")

if __name__ == "__main__":
    main(path_to_fragments, num_fragments)



if __name__ == "__main__":
    main(path_to_fragments, num_fragments)
