import h5py
import numpy as np
import open3d
import time
import sys

#Function for visualizing a single point cloud image
#takes in the array of all point clouds, the scene to take one from, and the frame to select
#Draws the point cloud, adjusting the orientation to be behind the camera
def singleVis(pClds, sc, ind):
  pcd = pClds[sc][ind]
  #open3d.visualization.draw_geometries_with_custom_animation([pcd_list])
  #open3d.visualization.draw_geometries([pcd], point_show_normal=True)
  open3d.visualization.draw_geometries([pcd], 
                                       zoom=0.7,
                                       front=[ -0.97855071346545319, -0.0033921739789494394, 0.20597814042259249 ], 
                                       lookat=[ 6.242122867289174, -0.28737243834214166, 4.2045998627737911 ], 
                                       up=[ 0.20597635214661203, 0.00087214010748639964, 0.97855658074942609 ])
  return

#This function loads the point clouds in from the h5 file specified here
#This fcuntion returns a 2D array where the first axis is a list of all the scenes, and the second index is a list of all the frames of that scene
def loadPClds():
  f = h5py.File('sim_with_point_cloud_all_frames.h5', 'r')

  pntClds = []

  #Each scene is a perspective of a different sensor on the robot: front, left, right
  for robotSide in list(f.values()):
    #Two values in this section - description and frame
    frames = list(robotSide.values())[1]
    curS = []

    #Iterate through all the frames, turn them into a point cloud, then add them to the list
    for frame in list(frames.values()):
      cloud = frame['cloud']
      npCld = np.array(cloud)

      #Reshapes from a 320 by 240 by 3 into 76800 by 3.
      #These are all just points in 3D space so dementionality can be reduced
      finShp = npCld.reshape(76800, 3)

      #Creates a pointcloud object and assignes all the points
      pcd = open3d.geometry.PointCloud()
      pcd.points = open3d.utility.Vector3dVector(finShp)
      curS.append(pcd)

    pntClds.append(curS)
  
  #geom = open3d.geometry.PointCloud()
  #geom.points = scene[0].points
  open3d.io.write_point_cloud("test_pntcld.pcd", pntClds[0][0])
  
  return pntClds

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
    vC = vis.get_view_control()
    vC.rotate(15.0, 50.0)
    
    i = 1
    #Runs through the scene 3 times befor3 moving to the next
    while(True): 
      #Loops through the point clouds
      geom.points = scene[i % len(scene)].points
      #Update visualizer with the new frame
      vis.update_geometry(geom)
      vis.poll_events()
      vis.update_renderer()

      i = i + 1
      #By default runs simulation way to fast - so pauses between very breifly
      #time.sleep(0.2)

      #Move on to next scene after 3 iterations
      if i == 3 * len(scene):
        break
    vis.destroy_window()
    return

  #Show single point cloud with propper orientation
  singleVis(pntClds, 0, 10)
  return

def errMess():
  print("Insufficient command line arguments")
  print("To run enter 'python3 h5Reader.py [arg]'")
  print("[arg] can be replaced with view or save to view the point cloud animations or save the point cloud")
  return -1

def main():
  #Load in the point clouds
  pntClds = loadPClds()

  if len(sys.argv) < 2:
    errMess()
  else:
    if sys.argv[1] == "view":
      viewPCs(pntClds)
    elif sys.argv[1] == "save":
      print("not yet working")
    else:
      errMess()



  return

main()
