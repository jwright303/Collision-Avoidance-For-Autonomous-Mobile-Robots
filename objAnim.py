from pcCluster import *
import h5Reader as rdr
import open3d as o3d
import argparse

FILE_NUMB = 150

def runAnimation():
  i = 0
  scene = []
  bboxs = None
  
  print("Starting the point cloud reading")
  vis = o3d.visualization.Visualizer()
  vis.create_window()
  ctr = vis.get_view_control()

  #ctr = vis.get_view_control()
  #ctr.change_field_of_view(step=90)
  pcld = o3d.io.read_point_cloud("./PreAct_3D_F/pcd_" + str(0) + ".ply")
  geom = o3d.geometry.PointCloud()
  geom.points = pcld.points
  vis.add_geometry(geom)


  
  
  for i in range(1, FILE_NUMB):
    pcld = o3d.io.read_point_cloud("./PreAct_3D_F/pcd_" + str(i) + ".ply")
    pcld_copy = o3d.geometry.PointCloud()
    #scene.append(pcld)
    ctr.change_field_of_view(step=-90.0)
    
    arr = np.asarray(pcld.points)
    arr[:, [0, 1, 2]] = arr[:, [0, 2, 1]]
    arr[:,2] *= -1
    pcld.points = o3d.utility.Vector3dVector(arr)
    pcld_copy.points = o3d.utility.Vector3dVector(arr)

    if bboxs is not None:
      for box in bboxs:
        vis.remove_geometry(box)
  
    #Cluster the point cloud 
    pcld_cluster, labels = clusterFilter(30, pcld)

    #Create bounding boxes for all the clusters
    bboxs = objBoundingBoxes(pcld_cluster, labels)
    
    #Start the visualization with the first point cloud of the scene
    
    #Runs through the scene 3 times befor3 moving to the next
    #Loops through the point clouds
    #vis.add_geometry(geom)
    geom.points = pcld_copy.points

    for box in bboxs:
      vis.add_geometry(box)
    #for box in bboxs:
    #  vis.add_geometry(box)
    #Update visualizer with the new frame
    vis.update_geometry(geom)
    vis.poll_events()
    vis.update_renderer()

    #i = i + 1
    #By default runs simulation way to fast - so pauses between very breifly
    #time.sleep(0.2)
    #vis.clear_geometries()

    #Move on to next scene after 3 iterations
  vis.destroy_window()
  return



def danger(box, arr, front):
  points = np.asarray(box.get_box_points())
  minP = box.get_min_bound()[0]
  maxP = box.get_max_bound()[0]

  pNear = points[np.logical_and(points[:,0] > -0.75, points[:,0] < -0.75)]
  cliffC = arr[(arr[:,0] > -0.75) & (arr[:,0] < 0.75) & (arr[:,1] < -0.6)]

  if (minP < 0 and maxP > 0) and front > -3:
    print("Object close and spans the critical area")
    return True
  elif pNear.size != 0 and front > -3:
    print("Object close and ends are in the critical area")
    return True
  elif cliffC.size > 30:
    print("Cliff detected")
    geom = o3d.geometry.PointCloud()
    geom.points = o3d.utility.Vector3dVector(cliffC)
    o3d.visualization.draw_geometries([geom])
    return True
    #Cliff scan check

  return False


def objAnim(pcds):
  bboxs = None
  i = 0
  
  print("Starting the point cloud reading")
  vis = o3d.visualization.Visualizer()
  vis.create_window()
  ctr = vis.get_view_control()

  geom = o3d.geometry.PointCloud()
  geom.points = pcds[0].points
  vis.add_geometry(geom)

  
  for pcld in pcds:
    pcld_copy = o3d.geometry.PointCloud()
    ctr.change_field_of_view(step=-90.0)
    
    arr = np.asarray(pcld.points)
    #arr[:, [0, 1, 2]] = arr[:, [0, 2, 1]]
    #arr[:,2] *= -1
    pcld.points = o3d.utility.Vector3dVector(arr)
    pcld_copy.points = o3d.utility.Vector3dVector(arr)

    if bboxs is not None:
      for box in bboxs:
        vis.remove_geometry(box)
  
    #Cluster the point cloud 
    pcld_cluster, labels = clusterFilter(30, 0.3, pcld)

    #Create bounding boxes for all the clusters
    bboxs = objBoundingBoxes(pcld_cluster, labels)
    
    #Start the visualization with the first point cloud of the scene
    
    #Runs through the scene 3 times befor3 moving to the next
    #Loops through the point clouds
    #vis.add_geometry(geom)
    geom.points = pcld_copy.points

    for box in bboxs:
      vis.add_geometry(box)
    #for box in bboxs:
    #  vis.add_geometry(box)
    #Update visualizer with the new frame
    vis.update_geometry(geom)
    vis.poll_events()
    vis.update_renderer()

    for box in bboxs:
      bpoints = np.asarray(box.get_box_points())
      bcent = box.get_center()

      cx = bcent[0]
      mx = np.amax(bpoints[:,2])
     
      #print("check point")
      #print(cx, mIn)
      if danger(box, arr,  mx):
        print("about to collide", mx)
        return [pcld, bboxs, i]

    i = i + 1
    #By default runs simulation way to fast - so pauses between very breifly
    #time.sleep(0.2)
    #vis.clear_geometries()

    #Move on to next scene after 3 iterations
  vis.destroy_window()


  return None


if __name__=="__main__":
  parser = argparse.ArgumentParser()
  parser.add_argument("--pth", help="specify the path of the pclds", type=str)
  parser.add_argument("--pref", help="specify the prefix of the point clouds", type=str)
  parser.add_argument("--pcNum", help="specify the number of point clouds", type=int)
  
  args = parser.parse_args()
  pth = args.pth
  pref = args.pref
  pcNum = args.pcNum

  pclds = rdr.readPCFromLocation(pth, pref, pcNum)
  res = objAnim(pclds)

  if res != None:
    print("Frame before collision")
    bbs = res[1]
    bbs.append(res[0])
    print("Index: " + str(res[2]))
    o3d.visualization.draw_geometries(bbs)
  #runAnimation()

  pass
