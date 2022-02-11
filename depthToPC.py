import h5py
from h5Reader import *
import numpy as np
import open3d as o3d
import numpy as np

def random():
  f = h5py.File('actor_robot.h5', 'r')

  #print("keys")
  #print(f.keys())
  #print("\nvalues")
  #print(f.values())
  vals1 = f.values()
  frnt = f["robot_left_front_0"]
  frnt_frames = frnt["frames"]
  first_frm = frnt_frames.keys()
  print(frnt_frames["026045"])

  tst = frnt_frames["026045"]
  depths = tst['depth']
  base = tst['base_color']

  depths_arr = np.asarray(depths)
  base_arr = np.asarray(base)

  maxInv = np.full(base_arr.shape, 24.0, np.float32)
  new_d = np.subtract(maxInv, depths_arr)

  #pcd = o3d.geometry.PointCloud()
  #pcd.points = o3d.utility.Vector3dVector(depths_arr)
  #o3d.visualization.draw_geometries([pcd])
  b_Im = o3d.geometry.Image((base_arr.astype(np.float32)))
  print(base_arr)
  #o3d.visualization.draw_geometries([b_Im])
  d_Im = o3d.geometry.Image((depths_arr.astype(np.float32)))
  #o3d.visualization.draw_geometries([d_Im])
  #img = o3d.geometry.Image((depths_arr.astype(np.float32)))
  print("Depth array")
  print(depths_arr.shape)
  rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(b_Im, d_Im, depth_scale=0.000000001, depth_trunc=50)

  pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
        rgbd_image,
        o3d.camera.PinholeCameraIntrinsic(
            o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
  pcd.transform([[1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,1]])
  pcd.scale(0.1)
  #pcd.paint_uniform_color([1, 0.706, 0])
  o3d.visualization.draw_geometries([pcd])
  print("point cloud shape")
  print(np.asarray(pcd.points).shape)
  print(rgbd_image)

  depths_arr = np.asarray(depths)

  for frm in frnt_frames:
    #print(frm)
    break

  #print(first_frm)
  #print(frnt_frames)
  #print(frnt)
  #print("sub vals")
  #print(f.keys())
  for v in vals1:
    #print(v)
    fms = v['frames']
    #print(fms)
    #print(fms.keys())
    #print(len(fms.keys()))
    #for key in fms.keys():
    #  print(fms[key])
      #for sv in v:
     # print(sv)
    #break
  
  #print(len(vals1))


  return

def getAxisLines():
  cornersA = ([0,0,1], [0,0,-1])
  cornersB = ([0,1,0], [0,-1,0])
  cornersC = ([1,0,0], [-1,0,0])
  lines = [(0, 1)]
  colors = [[1, 0, 0] for i in range(len(lines))]
  ls1 = o3d.geometry.LineSet()
  ls1.points = o3d.utility.Vector3dVector(cornersA)
  ls1.lines = o3d.utility.Vector2iVector(lines)
  ls1.colors = o3d.utility.Vector3dVector(colors)

  colors = [[0, 0, 0] for i in range(len(lines))]
  ls2 = o3d.geometry.LineSet()
  ls2.points = o3d.utility.Vector3dVector(cornersB)
  ls2.lines = o3d.utility.Vector2iVector(lines)
  ls2.colors = o3d.utility.Vector3dVector(colors)

  colors = [[0, 0, 1] for i in range(len(lines))]
  ls3 = o3d.geometry.LineSet()
  ls3.points = o3d.utility.Vector3dVector(cornersC)
  ls3.lines = o3d.utility.Vector2iVector(lines)
  ls3.colors = o3d.utility.Vector3dVector(colors)

  return ls1, ls2, ls3

def main():
  f = h5py.File('actor_robot.h5', 'r')

  frnt = f["robot_left_front_0"]
  frnt_frames = frnt["frames"]
  first_frm = frnt_frames.keys()

  pntClds = []

  for key in first_frm:
    tst = frnt_frames[key]
    depths = tst['depth']
    base = tst['base_color']

    depths_arr = np.asarray(depths)
    base_arr = np.asarray(base)
    base_arr = np.divide(base_arr, 255)

    b_Im = o3d.geometry.Image((base_arr.astype(np.float32)))
    
    d_Im = o3d.geometry.Image((depths_arr.astype(np.float32)))
    
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(b_Im, d_Im, depth_scale=0.05, depth_trunc=500)

    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(
          rgbd_image,
          o3d.camera.PinholeCameraIntrinsic(
              o3d.camera.PinholeCameraIntrinsicParameters.PrimeSenseDefault))
    pcd.transform([[1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,1]])
    print("Printing origional point cloud")
    ls1, ls2, ls3 = getAxisLines()
    o3d.visualization.draw_geometries([pcd, ls1, ls2, ls3])
    
    r = pcd.get_rotation_matrix_from_xyz((0, 0.9 * np.pi, 0))
    pcd = pcd.rotate(r, center=(0,0,0))
    
    bb = pcd.get_axis_aligned_bounding_box()
    cent = bb.get_center()

    #r = pcd.get_rotation_matrix_from_xyz((0.6 * np.pi, 0, 0))
    #pcd = pcd.rotate(r, center=(cent))
    
    pcPoints = np.asarray(pcd.points)
    pcPoints[:,2] *= 0.2
    pcd.points = o3d.utility.Vector3dVector(pcPoints)
    
    print("printing point cloud after transformations")
    ls1, ls2, ls3 = getAxisLines()
    o3d.visualization.draw_geometries([pcd, ls1, ls2, ls3])
    pntClds.append(pcd)

  ls1, ls2, ls3 = getAxisLines()

  print("printing point cloud after transformations with lines")
  o3d.visualization.draw_geometries([pntClds[0], ls1, ls2, ls3])

  return
  viewPCs([pntClds, ls1, ls2, ls3])

  return

main()
