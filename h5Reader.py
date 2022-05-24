import h5py
import numpy as np
import open3d
import time
from matplotlib import pyplot as plt
import sys


def distanceFilter(pclds, distance):
  for pc in pclds:
    arr = np.asarray(pc.points)
    #arr /= -230
    sq = np.square(arr)
    sm = np.sum(sq, axis=1)
    arr = arr[sm < distance]
    pc.points = open3d.utility.Vector3dVector(arr)

  return pclds

# Function for getting lines to display the three axis
# Returns 3 lines for the x, y and z axis that are located at (0, 0)
def getAxisLines():
  cornersA = ([0,0,1], [0,0,-1])
  cornersB = ([0,1,0], [0,-1,0])
  cornersC = ([1,0,0], [-1,0,0])
  lines = [(0, 1)]
  colors = [[1, 0, 0] for i in range(len(lines))]
  ls1 = open3d.geometry.LineSet()
  ls1.points = open3d.utility.Vector3dVector(cornersA)
  ls1.lines = open3d.utility.Vector2iVector(lines)
  ls1.colors = open3d.utility.Vector3dVector(colors)

  colors = [[0, 0, 0] for i in range(len(lines))]
  ls2 = open3d.geometry.LineSet()
  ls2.points = open3d.utility.Vector3dVector(cornersB)
  ls2.lines = open3d.utility.Vector2iVector(lines)
  ls2.colors = open3d.utility.Vector3dVector(colors)

  colors = [[0, 0, 1] for i in range(len(lines))]
  ls3 = open3d.geometry.LineSet()
  ls3.points = open3d.utility.Vector3dVector(cornersC)
  ls3.lines = open3d.utility.Vector2iVector(lines)
  ls3.colors = open3d.utility.Vector3dVector(colors)

  return ls1, ls2, ls3

#Function for visualizing a single point cloud image
#takes in the array of all point clouds, the scene to take one from, and the frame to select
#Draws the point cloud, adjusting the orientation to be behind the camera
def singleVis(ptcld):
  pcd = ptcld
  points = np.asarray(pcd.points)
  #points[:, [0, 1, 2]] = points[:, [0, 2, 1]]
  #pcd.points = open3d.utility.Vector3dVector(points)

  ls1, ls2, ls3 = getAxisLines()
  #print(ls1, ls2, ls3)
  open3d.visualization.draw_geometries([pcd, ls1, ls2, ls3])
  
  #return
  #open3d.visualization.draw_geometries([pcd], 
  #                                     zoom=0.7,
  #                                     front=[ -0.97855071346545319, -0.0033921739789494394, 0.20597814042259249 ], 
  #                                     lookat=[ 6.242122867289174, -0.28737243834214166, 4.2045998627737911 ], 
  #                                     up=[ 0.20597635214661203, 0.00087214010748639964, 0.97855658074942609 ])
  return


def readPCFromLocation(path, prefix, pcNum):
  pclds = []
  for i in range(0, pcNum):
    pc = open3d.io.read_point_cloud(path + prefix + str(i) + ".ply", remove_nan_points=True)
    pnts = np.asarray(pc.points)
    #pnts[:, [0, 1, 2]] = pnts[:, [0, 2, 1]]
    pc.points = open3d.utility.Vector3dVector(pnts)
    pclds.append(pc)

  return pclds


def loadPCldsFromDepthFile():

  return


#This function loads the point clouds in from the h5 file specified here
#This fcuntion returns a 2D array where the first axis is a list of all the scenes, and the second index is a list of all the frames of that scene
def loadPCldsFromFile(path, file):
  f = h5py.File(path + file, 'r')

  #pntClds = []

  #Each scene is a perspective of a different sensor on the robot: front, left, right
  for robotSide in list(f.values()):
    #Two values in this section - description and frame
    frames = list(robotSide.values())[1]
    curS = []

    #Iterate through all the frames, turn them into a point cloud, then add them to the list
    for frame in list(frames.values()):
      cloud = frame['cloud']
      amp = np.asarray(frame['amplitude'])
      npCld = np.array(cloud)

      #Reshapes from a 320 by 240 by 3 into 76800 by 3.
      #These are all just points in 3D space so dementionality can be reduced
      finShp = npCld.reshape(76800, 3)
      ampFix = amp.reshape(76800, 1)

      #Remove all point in the cloud that don't meet the amplitude requirement
      #finShp = finShp[ampFix[:,0] > 28]

      finShp[:, [0, 1, 2]] = finShp[:, [1, 2, 0]]
      finShp[:,2] *= -1

      #Creates a pointcloud object and assignes all the points
      pcd = open3d.geometry.PointCloud()
      pcd.points = open3d.utility.Vector3dVector(finShp)
      curS.append(pcd)

    #pntClds.append(curS)
  
    return curS


def viewPCs(pntClds):
  #Iterate through each scene
  for scene in pntClds:
    #For each scene create a new visualizer
    vis = open3d.visualization.Visualizer()
    vis.create_window()
    
    #Start the visualization with the first point cloud of the scene
    geom = open3d.geometry.PointCloud()

    geom.points = scene[0].points
    vis.add_geometry(geom)
    
    i = 1
    #Runs through the scene 3 times befor3 moving to the next
    while(True): 
      #Loops through the point clouds
      cP = np.asarray(scene[i % len(scene)].points)
      #newA = arr[(arr[:,1] < -0.01) & (arr[:,0] < 4, arr[:,0] > -4)]
      geom.points = scene[i % len(scene)].points
      #Update visualizer with the new frame
      vis.update_geometry(geom)
      vis.poll_events()
      vis.update_renderer()

      i = i + 1
      #By default runs simulation way to fast - so pauses between very breifly
      time.sleep(0.2)

      #Move on to next scene after 3 iterations
      if i == 4 * len(scene):
        time.sleep(6)
        break
    vis.destroy_window()

  #Show single point cloud with propper orientation
  return
