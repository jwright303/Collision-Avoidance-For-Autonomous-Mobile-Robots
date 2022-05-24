import h5Reader as rdr
import open3d as o3d
import numpy as np
import argparse 

def fixNFilter(arr):
  #arr[:,2] *= -1
  #arr /= 200
  minV = np.amin(arr, axis=0)
  maxV = np.amax(arr, axis=0)
  print("min values: ", minV)
  print("max values: ", maxV)

  xShift = (minV[0] + maxV[0]) / 2.0
  yShift = (minV[1] + minV[1]) / 4.0
  arr[:,0] -= xShift
  arr[:,1] -= yShift

  #sum_sq = np.dot(arr.T, arr)
  sq = np.square(arr)
  sm = np.sum(sq, axis=1)
  arr = arr[sm < 80.0]
  #print(sm)
  minV = np.amin(sm)
  maxV = np.amax(sm)
  print("min values: ", minV)
  print("max values: ", maxV)
  #print(sm < 1200)
  #arr = arr[sm < 80.0]

  #print(arr)
  #maxV = np.amax(arr, axis=0)
  #print("max values: ", maxV)
  #minV = np.amin(arr, axis=0)
  #print("min values: ", minV)

  #newA = arr[arr[:,2] > 0.3]


  return arr

def shiftTesting(pcld):
  shift = -1.6
  
  arr = np.asarray(pcld.points)
  arr[:,0] += shift
  #arr *= 10
  pcld.points = o3d.utility.Vector3dVector(arr)

  return 


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--pth", help="specify the path of the pclds", type=str)
  parser.add_argument("--pref", help="specify the prefix of the point clouds", type=str)
  parser.add_argument("--pcNum", help="specify the number of point clouds", type=int)
  parser.add_argument("--pcd", help="sepcify if extension is pcd instead of ply", nargs='?', const=False, type=bool)
  
  args = parser.parse_args()
  pth = args.pth
  pref = args.pref
  pcNum = args.pcNum
  pcd = args.pcd
  
  ext = ".ply"
  if pcd:
    ext = ".pcd"

  data = o3d.io.read_point_cloud(pth + pref + str(pcNum) + ext, remove_nan_points=True)
  arr = np.asarray(data.points)
  minV = np.amin(arr, axis=0)
  maxV = np.amax(arr, axis=0)
  print("min values: ", minV)
  print("max values: ", maxV)
  arr = arr[arr[:,2] > -20]
  #arr[:,2] /= 2.5
  shiftTesting(data)

  minV = np.amin(arr, axis=0)
  maxV = np.amax(arr, axis=0)
  print("min values: ", minV)
  print("max values: ", maxV)

  data.points = o3d.utility.Vector3dVector(arr)
  
  rdr.singleVis(data)
  
  return

main()
