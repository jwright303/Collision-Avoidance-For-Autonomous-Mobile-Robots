import h5Reader as rdr
import open3d as o3d
import numpy as np
import sys
import argparse
import time
#from sensor_msgs.msg import PointCloud2
import numpy as np 


PCLD_NUM = 90

def reCreateSet():
  pcs = []
  for i in range(80):
    pc = o3d.io.read_point_cloud("./Camera_Pclds/pcld_" + str(i) + ".pcd")
    points = np.asarray(pc.points)
    print(points)
    mask = ~np.isnan(points).any(axis=1)
    points = points[mask]
    print(points)
    pc.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud("./Camera_Fixed/pcld_" + str(i) + ".ply", pc)
    o3d.visualization.draw_geometries([pc],
                                  zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])
    pcs.append(pc)

  return pcs

def readOneImage():
   
    pc = o3d.io.read_point_cloud("./ptclds/test/d_image_20220420-223040-000.pcd")
    points = np.asarray(pc.points)
    #new = []
    #for row in points:
    #    if not np.isnan(row[0]):
    #      new.append(row)
    #print(np.asarray(new))
    #o3d.io.write_point_cloud("test.ply", pc)
    #pc.points = o3d.utility.Vector3dVector(new)
    print(pc)

    mask = ~np.isnan(points).any(axis=1)
    points = points[mask]
    pc.points = o3d.utility.Vector3dVector(points)
    print(pc)

    
   

    ls1, ls2, ls3 = rdr.getAxisLines()
    o3d.visualization.draw_geometries([pc],
                                  zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])

def readAll():
  c = 0
  ptclds = []
  st = "d_image_20220421-010505-000.pcd"
  for i in range(1, 18):
    if i < 10:
      pth = "./ptclds/TwoObjects/PointClouds/d_image_20220421-01070"
    else:
      pth = "./ptclds/TwoObjects/PointClouds/d_image_20220421-0107"

    for j in range(0, 7):
      pc = o3d.io.read_point_cloud(pth + str(i) + "-00" + str(j) + ".pcd")
      points = np.asarray(pc.points)
      mask = ~np.isnan(points).any(axis=1)
      points = points[mask]
      pc.points = o3d.utility.Vector3dVector(points)
      out = o3d.io.write_point_cloud("./ptclds/Two_Fixed/pcld_" + str(c) + ".ply", pc)
      if out:
        c += 1
      print(out)
      #o3d.visualization.draw_geometries([pc],
      #                            zoom=0.3412,
      #                            front=[0.4257, -0.2125, -0.8795],
      #                            lookat=[2.6172, 2.0475, 1.532],
      #                            up=[-0.0694, -0.9768, 0.2024])


def simpleTest():
  pc = o3d.io.read_point_cloud("./PreAct_3D_F/pcd_70.ply")
  o3d.io.write_point_cloud("./test.pcd", pc, write_ascii=True)
  return


if __name__ == '__main__':
  #reCreateSet()
  #pclds =  pc.points = o3d.utility.Vector3dVector(new) 
  #readAll()
  #readOneImage()
  simpleTest()
   
