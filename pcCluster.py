import open3d as o3d
import cv2
import time
import matplotlib.pyplot as plt
import numpy as np

########################################
### Function for clustering the point cloud
### Takes in the minimum_points parameter for the clustering algorithm, and the point cloud to cluster on 
### Returns a clustered point cloud, and a list of the cluster number corresponding to the points in the point cloud
########################################
def clusterFilter(mp, pcld):
    print("Minimum Points: ", mp)

    #Read in a point cloud, and create a spare point cloud 
    pcld = o3d.io.read_point_cloud("./PreAct_3D_F/pcd_80.ply")
    pcld_copy = o3d.geometry.PointCloud()

    #Get the points of the point cloud for a little manipulation
    arr = np.asarray(pcld.points)

    #First fix the coordinate system of the point cloud, this way X (index 0) is right/left and Z (index 2) is front/back
    arr[:, [0, 1, 2]] = arr[:, [0, 2, 1]]
    #Save the fixed coordinate system to the copy point cloud
    pcld_copy.points = o3d.utility.Vector3dVector(arr)
    
    #Show the initial point cloud we will be working with
    pcld.points = o3d.utility.Vector3dVector(arr)
    o3d.visualization.draw_geometries([pcld])

    
    #Cropping the point cloud, remove the floor and some of the top as well as some of the noise from the furthest distance
    newA = arr[np.logical_and(arr[:,1] > 0.07, arr[:,1] < 6)]
    newA = newA[newA[:,2] < 9.5]
    
    #Show the cropped point cloud
    pcld.points = o3d.utility.Vector3dVector(newA)
    o3d.visualization.draw_geometries([pcld])

    #Cluster the cropped point cloud - Using the DBSCAN algorithm "A density-based algorithm for discovering clusters in large spatial databases with noise"
    #This takes three parameters
    #       eps - the density parameter that is used to find the neighboring points
    #       min_points - the minimum number of points needed to register something as a cluster
    #The function returns a labels array which assigns every point in the point cloud to a cluster a special cluster is also made (cluster 0) for the noise
    labels = np.array(pcld.cluster_dbscan(eps=0.3, min_points=mp, print_progress=True))
    max_label = labels.max()
    
    print(f"Number of labels: {max_label + 1}\n")
    print("Labels len", len(labels))
    
    #Create distinct colors for each of the clusters
    colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0

    #Display the point cloud with all the clusters
    pcld_clustered = o3d.geometry.PointCloud()
    pcld_clustered.points = o3d.utility.Vector3dVector(newA)
    pcld_clustered.colors = o3d.utility.Vector3dVector(colors[:, :3])

    #Remove all every point that was assigned to the noise cluster - make sure its removed from the point cloud, labels, and colors array
    aFin = newA[colors[:,3] != 0]
    labels = labels[colors[:,3] != 0]
    colors = colors[colors[:,3] != 0]

    #Update the point cloud with the new opints and the new colors
    pcld.points = o3d.utility.Vector3dVector(aFin)
    pcld.colors = o3d.utility.Vector3dVector(colors[:, :3])


    #First show the clustered point clouds with all the noise removed, then show it overlayed on the origional point cloud
    o3d.visualization.draw_geometries([pcld])
    o3d.visualization.draw_geometries([pcld_copy, pcld])
    
    return pcld, labels

##########################################
# Function for adding bounding boxes to each of the clusters
# Takes in the clustered point cloud as well as the corresponding labels for every point
# Returns a list of all the bounding boxes for the clustered point cloud
# Iterates through all the labels, and gets the corresponding cluster by filtering out all other points, then creates a bounding box that fits around those points and adds it to the list
#########################################
def objBoundingBoxes(pcld_cluster, labels):

    #Create a new point cloud that will house the cluster/object
    obj = o3d.geometry.PointCloud()
    cPoints = np.asarray(pcld_cluster.points)
    print(cPoints.shape)
    boxes = []
    
    #Iterate through all the clusters, each time get the points for just that cluster
    #Easily create a bounding box around just those points, and add that to the list of bounding boxes
    for i in range(1, max(labels) + 1):
        objPoints = cPoints[np.where(labels == i)]
        obj.points = o3d.utility.Vector3dVector(objPoints)
        
        oBox = obj.get_axis_aligned_bounding_box()
        oBox.color = (1, 0, 0)
        boxes.append(oBox)

    #o3d.visualization.draw_geometries(boxes)
    
    return boxes


if __name__=="__main__":
    #Load in a sample point cloud from some of our simulated data
    pcld = o3d.io.read_point_cloud("./PreAct_3D_F/pcd_80.ply")
  
    #Cluster the point cloud 
    pcld_cluster, labels = clusterFilter(30, pcld)

    #Create bounding boxes for all the clusters
    bboxs = objBoundingBoxes(pcld_cluster, labels)
    

    #Fix dimensions of origional point cloud
    arr = np.asarray(pcld.points)
    arr[:, [0, 1, 2]] = arr[:, [0, 2, 1]]

    #Display the point cloud and the bounding boxes together
    pcld.points = o3d.utility.Vector3dVector(arr)
    bboxs.append(pcld)

    o3d.visualization.draw_geometries(bboxs)
    



    pass
