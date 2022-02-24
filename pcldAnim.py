import h5Reader as rdr
import open3d as o3d
import numpy as np
import sys
import argparse

#POINT_CLOUD_NUM = 150

def main():
  parser = argparse.ArgumentParser()
  parser.add_argument("--pth", help="specify the path of the pclds", type=str)
  parser.add_argument("--pref", help="specify the prefix of the point clouds", type=str)
  parser.add_argument("--pcNum", help="specify the number of point clouds", type=int)
  
  args = parser.parse_args()
  pth = args.pth
  pref = args.pref
  pcNum = args.pcNum

  pclds = rdr.readPCFromLocation(pth, pref, pcNum)
  rdr.viewPCs([pclds])
  
  return

main()
