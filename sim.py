import open3d as o3d
import numpy as np
import h5Reader as rdr
import argparse
from pcCluster import *
import time

# Constants that are used to create the rule box - 3 unites forward, and one unit to the left and rihgt
XC = 1
ZC = 3

###############################################
# Function that creates the rule box which is used to determine if there is an imminent Collision
# Takes in no parameters and returns the rule box
# Works by creating points which define the corners, then creating a bounding box that fits in all the points
###############################################
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

  #Creates a bounding box around the bouniding points using open3d built in function
  box = pcld.get_axis_aligned_bounding_box()
  box.color = (1,0,0)

  return box

##############################################
# Rule function which checks to see if a collision is close or a cliff is ahead 
#
# Uses the bounding boxes from the object detection algorithm to determine if object is ahead
# Returns true or false if there is danger (cliff or object) ahead
# Takes in the a bounding box, the scene in array format
##############################################
def danger(box, arr, front):
  #Gets all of the point cloud points from within the bounding box
  points = np.asarray(box.get_box_points())
  
  #Built in open3d function to get the minimum and maximum x cordinates of the bounding box
  minP = box.get_min_bound()[0]
  maxP = box.get_max_bound()[0]

  #From the points within the current bounding box find all of the points within the rule box area 
  pNear = points[np.logical_and(points[:,0] > -XC, points[:,0] < XC)]

  #From the point cloud, gather all the points that are within the critical X area and are below the floor
  cliffC = arr[(arr[:,0] > -XC) & (arr[:,0] < XC) & (arr[:,1] < -0.6)]

  #From the point cloud get all of the points that are within the critical X area nad above the floor
  frntPoints = arr[(arr[:,0] > -XC) & (arr[:,0] < XC) & (arr[:,1] < 2) & (arr[:,2] > -ZC) & (arr[:,1] >= -0.01)]
  geom = o3d.geometry.PointCloud()

  #Rules to determine when danger is
  #First rule checks to see if the bounding box spans the critical area and is close enough
  if (minP < 0 and maxP > 0) and front > -ZC:
    print("Object close and spans the critical area")
    geom.points = o3d.utility.Vector3dVector(frntPoints)
    pcld_cluster, labels = clusterFilter(80, 0.3, geom)
    
    #Sub rule checks to see if there are really any points in front - (for things like doorways)
    if len(labels) == 0:
      return False
    
    #Debugging lines
    #geom.points = o3d.utility.Vector3dVector(frntPoints)
    #pcld_cluster, labels = clusterFilter(80, 0.3, geom)
    #o3d.visualization.draw_geometries([geom])
    return True
  
  #Next rule is for checking if the points within the bounding box are in front of the robot and close enough
  elif pNear.size != 0 and front > -ZC:
    print("Object close and ends are in the critical area")
    return True
  
  #Final rule is for checkinf if there is a cliff - there must be more than 30 points below the floor and within the critical X range
  elif len(cliffC) > 30:
    print("Cliff detected")
    print("Len, Size,", len(cliffC), cliffC.size)
    geom = o3d.geometry.PointCloud()
    geom.points = o3d.utility.Vector3dVector(cliffC)
    return True

  return False

###########################################
# This function tests the current point cloud to see if there is imminent collision or cliff
# 
# First, crops out the back most points for the object detection 
#   Next finds the clusters (objects) from the cropped point cloud
#     If there are any objects detected then it goes to the rules, otherwise it returns none
#
# Takes in the point cloud of the current scene and either returns some information about the scene if it detects a collision or returns None
###########################################
def testCurPcld(curPc):
  arr = np.asarray(curPc.points)
  
  #Crops the point cloud and stores it in a dummy pointcloud for object detection - we only care about close objects
  arr[arr[:,2] > -30]
  geom = o3d.geometry.PointCloud()
  geom.points = o3d.utility.Vector3dVector(arr)
  
  pcld_cluster, labels = clusterFilter(80, 0.3, geom)
  
  #If any objects detected iterate through them and do the danger check
  if len(labels) > 0:
    #Creates a bounding box for each object/ cluster
    bboxs = objBoundingBoxes(pcld_cluster, labels)

    #Iterate through each bounding box and test the danger
    for box in bboxs:
      bpoints = np.asarray(box.get_box_points())
      bcent = box.get_center()
      #Gets the closest points from within the bounding box - closest will be in the Z direction
      mx = np.amax(bpoints[:,2])

      #Checks danger giving it the current bounding box, points of the current point cloud scene, and distance of closest points within the bounding box
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
  vis.add_geometry(boxC)

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

  if res != None:
    print("Frame before collision")
    bbs = res[1]
    bbs.append(res[0])
    bbs.append(res[3])
    bbs.append(res[4])
    print("Index: " + str(res[2]))
    o3d.visualization.draw_geometries(bbs)

  pass
