import open3d as o3d
import numpy as np
import os 

# Generated basic peg-transfer PointCloud using Open3D from .OBJ files and hard-coded positions in space

block_location = '/home/dvrk-team/dvrk_ctrl_ws/src/peg_sim/ADF/Phantoms/Pegboards/high_res/block5.OBJ'
peg_location = '/home/dvrk-team/dvrk_ctrl_ws/src/peg_sim/ADF/Phantoms/Pegboards/high_res/peg7.OBJ'
peg_board_location = '/home/dvrk-team/dvrk_ctrl_ws/src/peg_sim/ADF/Phantoms/Pegboards/high_res/peg_board.OBJ'

block_mesh = o3d.io.read_triangle_mesh(block_location)
peg_mesh = o3d.io.read_triangle_mesh(peg_location)
peg_board_mesh = o3d.io.read_triangle_mesh(peg_board_location)


block_mesh.translate((0.024444686345014878, 0.2527384840964206, 0.7226560295887468),relative=False)
#Block6 - x=0.004930474261936756, y=0.25285186335907406, z=0.7226560314783721
#Block5 - x=0.024444831191290095, y=0.25273854975962995, z=0.7226560286512541

peg_mesh.translate((0.02455, 0.25263, 0.708911)) # peg 7
peg_board_mesh.translate((0.03352, 0.23481, 0.70891),relative=False)


block_mesh.compute_vertex_normals()
peg_mesh.compute_vertex_normals()
peg_board_mesh.compute_vertex_normals()

peg_board_mesh.paint_uniform_color([1, 1, 1]) # paint peg board grey
peg_mesh.paint_uniform_color([0, 1, 0]) # paint peg blue
block_mesh.paint_uniform_color([1, 0, 0]) # paint block red




#pcd = o3d.io.read_point_cloud(block_location)
block_pcd = block_mesh.sample_points_uniformly(number_of_points=2000) # sample points from mesh to point cloud
peg_pcd = peg_mesh.sample_points_uniformly(number_of_points=2000) # sample points from mesh to point cloud
peg_board_pcd = peg_board_mesh.sample_points_uniformly(number_of_points=5000) # sample points from mesh to point cloud

o3d.visualization.draw_geometries([block_pcd, peg_pcd, peg_board_pcd]) # visualize the point cloud and mesh together
