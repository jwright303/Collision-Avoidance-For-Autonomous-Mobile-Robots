from pcCluster import *
import open3d as o3d

FILE_NUMB = 179

def main():
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


main()
