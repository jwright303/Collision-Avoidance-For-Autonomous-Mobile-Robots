import h5Reader as rdr
import open3d as o3d
import numpy as np
import argparse 


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--pth", help="specify the path of the pclds", type=str)
  parser.add_argument("--pref", help="specify the prefix of the point clouds", type=str)
  parser.add_argument("--pcNum", help="specify the number of point clouds", type=int)
  
  args = parser.parse_args()
  pth = args.pth
  pref = args.pref
  pcNum = args.pcNum

  data = o3d.io.read_point_cloud(pth + pref + str(pcNum) + ".ply")
  arr = np.asarray(data.points)

  #newA = arr[arr[:,2] > 0.3]
  newA = arr
  data.points = o3d.utility.Vector3dVector(newA)
  
  rdr.singleVis(data)
  
  return

main()
