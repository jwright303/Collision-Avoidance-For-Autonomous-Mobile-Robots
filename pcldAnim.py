import h5Reader as rdr
import open3d as o3d
import numpy as np
import sys
import argparse

#POINT_CLOUD_NUM = 150
def distanceFilter(pclds):

  for pc in pclds:
    arr = np.asarray(pc.points)
    #arr /= -230
    sq = np.square(arr)
    sm = np.sum(sq, axis=1)
    arr = arr[sm < 80.0]
    pc.points = o3d.utility.Vector3dVector(arr)

  return pclds

def cropTesting(pclds):
  for pc in pclds:
    arr = np.asarray(pc.points)
    arr = arr[arr[:,1] > 1.0]
    pc.points = o3d.utility.Vector3dVector(arr)

  return pclds

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
  #61 63 64 66 68
  #newA = [pclds[70]] + [pclds[61]] + pclds[63:65] + [pclds[66]] + [pclds[68]] + pclds[:61] + pclds[62:63] + pclds[65:66] + pclds[67:68] + [pclds[69]]
  #pclds = distanceFilter(pclds)
  #pclds = cropTesting(pclds)

  rdr.viewPCs([pclds])
  
  return

main()
