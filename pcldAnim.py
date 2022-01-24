import h5Reader as rdr
import open3d as o3d
import numpy as np
import sys


def main():
  pclds = []

  for i in range(0, 179):
    data = o3d.io.read_point_cloud("./Open3D-ML/PreAct_3D_F/pcd_" + str(i) + ".ply")
    pclds.append(data)

  rdr.viewPCs([pclds])
  
  return

main()
