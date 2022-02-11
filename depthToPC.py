import h5py
from h5Reader import *
from pcCluster import *
import numpy as np
import open3d as o3d
import numpy as np

HORIZONTAL_FOV_DEG = 108
VERTICAL_FOV_DEG = 81
IM_WIDTH = 320
IM_HEIGHT = 240

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
    
    rgbd_image = o3d.geometry.RGBDImage.create_from_color_and_depth(b_Im, d_Im, depth_scale=1, depth_trunc=500)

    h_rad = HORIZONTAL_FOV_DEG/180.*np.pi
    v_rad = VERTICAL_FOV_DEG/180.*np.pi

    f_hor_pix= (0.5*IM_WIDTH)/np.tan(0.5*h_rad)
    f_vert_pix= (0.5*IM_HEIGHT)/np.tan(0.5*v_rad)

    print(rgbd_image)

    pcd = o3d.geometry.PointCloud.create_from_rgbd_image(rgbd_image, o3d.camera.PinholeCameraIntrinsic(320, 240, f_hor_pix, f_vert_pix, 160, 120))

    pcd.transform([[1,0,0,0],[0,-1,0,0],[0,0,-1,0],[0,0,0,1]])
    #print("Printing origional point cloud")
    #ls1, ls2, ls3 = getAxisLines()
    #o3d.visualization.draw_geometries([pcd, ls1, ls2, ls3])
    
    #print("printing point cloud after transformations")
    #ls1, ls2, ls3 = getAxisLines()
    #o3d.visualization.draw_geometries([pcd, ls1, ls2, ls3])
    pntClds.append(pcd)

  #ls1, ls2, ls3 = getAxisLines()

  #print("printing point cloud after transformations with lines")
  #o3d.visualization.draw_geometries([pntClds[0], ls1, ls2, ls3])

  #viewPCs([pntClds])
  pcld_cluster, labels = clusterFilter(30, pntClds[0], v=True)
  bboxs = objBoundingBoxes(pcld_cluster, labels)

  bboxs.append(pntClds[0])

  o3d.visualization.draw_geometries(bboxs)

  return

main()
