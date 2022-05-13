import open3d as o3d
import numpy as np
import h5Reader as rdr
import argparse
from pcCluster import *

XC = 1
ZC = 3

def createRuleBox():
  corners = [[-XC, 0, 0],
             [XC, 0, 0],
             [-XC, 0, -ZC],
             [XC, 0, -ZC],
             [-XC, 1, 0],
             [XC, 1, 0],
             [XC, 1, -ZC],
             [XC, 1, -ZC]
            ]


  pcld = o3d.geometry.PointCloud()
  pcld.points = o3d.utility.Vector3dVector(corners)

  box = pcld.get_axis_aligned_bounding_box()
  box.color = (1,0,0)

  return box


def danger(box, arr, front):
  points = np.asarray(box.get_box_points())
  minP = box.get_min_bound()[0]
  maxP = box.get_max_bound()[0]

  pNear = points[np.logical_and(points[:,0] > -XC, points[:,0] < XC)]
  cliffC = arr[(arr[:,0] > -XC) & (arr[:,0] < XC) & (arr[:,1] < -0.6)]
  frntPoints = arr[(arr[:,0] > -XC) & (arr[:,0] < XC) & (arr[:,1] < 2) & (arr[:,2] > -ZC) & (arr[:,1] >= -0.01)]

  if (minP < 0 and maxP > 0) and front > -ZC:
    print("Object close and spans the critical area")
    if frntPoints.size < 10:
      return False
    #pcld = o3d.geometry.PointCloud()
    #pcld.points = o3d.utility.Vector3dVector(frntPoints)
    #scne = o3d.geometry.PointCloud()
    #scne.points = o3d.utility.Vector3dVector(arr)
    #scne.paint_uniform_color([1, 0.706, 0])
    #o3d.visualization.draw_geometries([pcld])
    #o3d.visualization.draw_geometries([scne, pcld])

    return True
  elif pNear.size != 0 and front > -ZC:
    print("Object close and ends are in the critical area")
    return True
#  elif cliffC.size > 30:
#    print("Cliff detected")
#    geom = o3d.geometry.PointCloud()
#    geom.points = o3d.utility.Vector3dVector(cliffC)
#    o3d.visualization.draw_geometries([geom])
#    return True
    #Cliff scan check

  return False


def testCurPcld(curPc):
  arr = np.asarray(curPc.points)
  
  pcld_cluster, labels = clusterFilter(85, 0.3, curPc)
  bboxs = objBoundingBoxes(pcld_cluster, labels)

  for box in bboxs:
    bpoints = np.asarray(box.get_box_points())
    bcent = box.get_center()
    mx = np.amax(bpoints[:,2])
   
    #print("check point")
    #print(cx, mIn)
    if danger(box, arr,  mx):
      print("about to collide", mx)
      return [curPc, bboxs, arr]

  return None


def pcAnim(pclds, boxC):
  #Iterate through each scene
  #For each scene create a new visualizer
  vis = o3d.visualization.Visualizer()
  vis.create_window()
  
  #Start the visualization with the first point cloud of the scene
  geom = o3d.geometry.PointCloud()

  geom.points = pclds[0].points
  vis.add_geometry(geom)
  #vis.add_geometry(boxC)

  print("Begining Simulation..")
  i = 1
  while(True):
    curPc = pclds[i % len(pclds)]
    og = o3d.geometry.PointCloud()
    geom.points = curPc.points
    og.points = curPc.points
    vis.update_geometry(geom)
    vis.poll_events()
    vis.update_renderer()

    pcRes = testCurPcld(curPc)
    if pcRes != None:
      pcRes.insert(2, i)
      pcRes.insert(3, boxC)
      pcRes.insert(4, og)
      return pcRes

    i = i + 1
    #time.sleep(0.2)

    if i == 3 * len(pclds):
      break
  
  vis.destroy_window()

  return None


if __name__=="__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--pth", help="specify the path of the pclds", type=str)
  parser.add_argument("--pref", help="specify the prefix of the point clouds", type=str)
  parser.add_argument("--pcNum", help="specify the number of point clouds", type=int)
  parser.add_argument("--dF", help="specify if a distance filter should be used", nargs='?', const=False, type=bool)
  
  args = parser.parse_args()
  pth = args.pth
  pref = args.pref
  pcNum = args.pcNum
  dF = args.dF

  box = createRuleBox()
  pclds = rdr.readPCFromLocation(pth, pref, pcNum)
  if dF:
    pclds = rdr.distanceFilter(pclds)
  res = pcAnim(pclds, box)
  #res = pcAnim(pclds, None)

  if res != None:
    print("Frame before collision")
    bbs = res[1]
    bbs.append(res[0])
    bbs.append(res[3])
    bbs.append(res[4])
    print("Index: " + str(res[2]))
    o3d.visualization.draw_geometries(bbs)

    #arr = res[4]
    #cliffP = arr[(arr[:,0] > -XC) & (arr[:,0] < XC) & (arr[:,1] < -0.6)]
    #pcld = o3d.geometry.PointCloud()
    #pcld.points = o3d.utility.Vector3dVector(cliffP)
    #pc = res[0]
    #pc.paint_uniform_color([1, 0.706, 0])
    #o3d.visualization.draw_geometries([pc, pcld])

  pass
