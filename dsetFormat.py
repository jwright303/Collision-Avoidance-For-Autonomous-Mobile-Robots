from h5Reader import *
import depthToPC
import open3d as o3d
import h5py
import numpy as np
import sys
import argparse

def savePlyPC(pntClds, pth, pref):
  i = 0

  geom = o3d.geometry.PointCloud()

  for pcld in pntClds:
    points = np.asarray(pcld.points)
    #points[:, [2, 1]] = points[:, [1, 2]]
    #points[:, [0, 1, 2]] = points[:, [1, 2, 0]]
    points[:, [0, 1, 2]] = points[:, [1, 2, 0]]
    points[:,2] *= -1
    geom.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud(pth + pref + str(i) + ".ply", geom)
    i = i + 1

  return


def savePlyD(pntClds, pth, pref):
  i = 0

  geom = o3d.geometry.PointCloud()

  for pcld in pntClds:
    points = np.asarray(pcld.points)
    #points[:, [2, 1]] = points[:, [1, 2]]
    #points[:, [0, 1, 2]] = points[:, [1, 2, 0]]
    #points[:, [0, 1, 2]] = points[:, [1, 2, 0]]
    geom.points = o3d.utility.Vector3dVector(points)
    o3d.io.write_point_cloud(pth + pref + str(i) + ".ply", geom)
    i = i + 1

  return


def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--pth", help="specify the path of the h5 file", type=str)
  parser.add_argument("--fn", help="specify the filename of the h5 file", type=str)
  parser.add_argument("--destPth", help="specify the destination path to load the pcld files", type=str)
  parser.add_argument("--destPref", help="specify the prefix for the pcld files", type=str)
  parser.add_argument("--fType", help="specify the type of h5 we will be reading - point cloud or depth image (pc or depth)", type=str)

  if len(sys.argv) < 3:
    print("Error, insufficient command line arguments")
    print("Enter the path of the file and the file name when running")
  
  args = parser.parse_args()
  pth = args.pth
  fn = args.fn
  destPth = args.destPth
  desPref = args.destPref
  fType = args.fType
  
  pcds = None

  if fType == "pc":
    pcds = loadPCldsFromFile(pth, fn)
    savePlyPC(pcds, destPth, desPref)
  else:
    pcds = depthToPC.readH5(pth, fn)
    savePlyD(pcds, destPth, desPref)
  #pth = "./"
  #fn = "sim_with_point_cloud_all_frames.h5"

  return

main()
