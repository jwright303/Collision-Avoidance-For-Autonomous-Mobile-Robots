import h5Reader as rdr
import open3d as o3d
import numpy as np
import sys


def main():
  if len(sys.argv) != 2:
    print("Invalid command line arguments, only one parameter can be supplied, the index of the point cloud desired")
    return -1

  ind = int(sys.argv[1])
  print("photo index: ", ind)




  data = o3d.io.read_point_cloud("./Open3D-ML/PreAct_3D_F/pcd_" + str(ind) + ".ply")
  rdr.singleVis(data)
  
  return

main()
