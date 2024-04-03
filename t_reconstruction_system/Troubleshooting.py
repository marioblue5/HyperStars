import time
import open3d as o3d
import open3d.core as o3c
# Define your attributes
attr_names = ['tsdf', 'weight', 'color']
attr_dtypes = [o3d.core.Dtype.Float32, o3d.core.Dtype.Float32, o3d.core.Dtype.Float32]
attr_channels = [1, 1, 3]

# Define other parameters
voxel_size = 0.005859375
block_resolution = 16
block_count = 32500

# Specify the device
device = o3d.core.Device('CUDA:0')  # Create a Device object for CUDA device
print(device)
# Create the VoxelBlockGrid
device = o3d.core.Device(
    'CUDA:0' if o3d.core.cuda.is_available() else 'CPU:0')
start = time.time()
voxel_grid = o3d.t.geometry.VoxelBlockGrid(
    attr_names=('tsdf', 'weight', 'color'),
    attr_dtypes=(o3c.float32, o3c.float32, o3c.float32),
    attr_channels=attr_channels,
    voxel_size=voxel_size,
    block_resolution=16,
    block_count=block_count,
    device=device)
print(time.time() - start)