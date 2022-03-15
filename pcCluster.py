import open3d as o3d
import cv2
import time
import matplotlib.pyplot as plt
import numpy as np
import sys
import argparse

MIN_POINTS = 20
EPS = 0.3
verbose = False

#0.2 is around the highest you can go with still fairly good preformance
#0.1 is around the lowest you can go before it starts to become really slow
VOXEL_D = 0.07

def boxDetectionTest():
    box = bboxs[0]
    bpoints = np.asarray(box.get_box_points())
    bcent = box.get_center()
    bext = box.get_extent()

    cx = bcent[0]
    cy = bcent[1]
    cz = bcent[2]

    #cx = bext[0]
    #cy = bext[1]
    #cz = bext[2]
    pz = bpoints[:,2]
    mIn = np.amax(pz)
   
    print("check point")
    print(cx, mIn)

    cornersA = ([cx-0.2,cy,mIn], [cx+0.2,cy,mIn])
    lines = [(0, 1)]
    colors = [[0, 0, 1] for i in range(len(lines))]
    ls1 = o3d.geometry.LineSet()
    ls1.points = o3d.utility.Vector3dVector(cornersA)
    ls1.lines = o3d.utility.Vector2iVector(lines)
    ls1.colors = o3d.utility.Vector3dVector(colors)



    return


########################################
### Function for clustering the point cloud
### Takes in the minimum_points parameter for the clustering algorithm, and the point cloud to cluster on 
### Returns a clustered point cloud, and a list of the cluster number corresponding to the points in the point cloud
########################################
def clusterFilter(mp, eps,  pcld, v=False):
    if verbose or v:
        print("Minimum Points: ", mp)

    if verbose or v:
        o3d.visualization.draw_geometries([pcld])
    #Read in a point cloud, and create a spare point cloud 
    #pcld = o3d.io.read_point_cloud("./PreAct_3D_F/pcd_80.ply")
    pcld = pcld.voxel_down_sample(voxel_size=VOXEL_D)
    #pcld = pcld.voxel_down_sample(voxel_size=0.02)
    #pcld, ind = pcld.remove_statistical_outlier(nb_neighbors=20,
    #                                                    std_ratio=2.0)
    pcld_copy = o3d.geometry.PointCloud()

    #Get the points of the point cloud for a little manipulation
    arr = np.asarray(pcld.points)

    #First fix the coordinate system of the point cloud, this way X (index 0) is right/left and Z (index 2) is front/back
    #arr[:, [0, 1, 2]] = arr[:, [0, 2, 1]]
    #Save the fixed coordinate system to the copy point cloud
    pcld_copy.points = o3d.utility.Vector3dVector(arr)
    
    #Show the initial point cloud we will be working with
    #pcld.points = o3d.utility.Vector3dVector(arr)
    if verbose or v:
        o3d.visualization.draw_geometries([pcld])

    
    #Cropping the point cloud, remove the floor and some of the top as well as some of the noise from the furthest distance
    newA = arr[np.logical_not(np.logical_and(arr[:,1] < -0.01, arr[:,1] > -0.4))]
    #newA = newA[newA[:,2] < 9.5]
    
    #Show the cropped point cloud
    pcld.points = o3d.utility.Vector3dVector(newA)
    if verbose or v:
        o3d.visualization.draw_geometries([pcld])

    #Cluster the cropped point cloud - Using the DBSCAN algorithm "A density-based algorithm for discovering clusters in large spatial databases with noise"
    #This takes three parameters
    #       eps - the density parameter that is used to find the neighboring points
    #       min_points - the minimum number of points needed to register something as a cluster
    #The function returns a labels array which assigns every point in the point cloud to a cluster a special cluster is also made (cluster 0) for the noise
    #
    # Note: The following 6 lines were taken from the Open3d website and modified slightly - From the Geometry section of the tutorial, under the DBSCAN header
    # URL: http://www.open3d.org/docs/latest/tutorial/geometry/pointcloud.html#DBSCAN-clustering
    #
    labels = np.array(pcld.cluster_dbscan(eps=eps, min_points=mp, print_progress=False))
    max_label = labels.max()
    
    if verbose or v:
        print(f"Number of labels: {max_label + 1}\n")
        print("Labels len", len(labels))
    
    #Create distinct colors for each of the clusters
    colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0

    #Display the point cloud with all the clusters
    pcld_clustered = o3d.geometry.PointCloud()
    pcld_clustered.points = o3d.utility.Vector3dVector(newA)
    pcld_clustered.colors = o3d.utility.Vector3dVector(colors[:, :3])
    if verbose or v:
        o3d.visualization.draw_geometries([pcld_clustered])

    #Remove all every point that was assigned to the noise cluster - make sure its removed from the point cloud, labels, and colors array
    aFin = newA[colors[:,3] != 0]
    labels = labels[colors[:,3] != 0]
    colors = colors[colors[:,3] != 0]

    #Update the point cloud with the new opints and the new colors
    pcld.points = o3d.utility.Vector3dVector(aFin)
    pcld.colors = o3d.utility.Vector3dVector(colors[:, :3])


    #First show the clustered point clouds with all the noise removed, then show it overlayed on the origional point cloud
    if verbose or v:
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
    if verbose:
        print(cPoints.shape)
    boxes = []
    
    #Iterate through all the clusters, each time get the points for just that cluster
    #Easily create a bounding box around just those points, and add that to the list of bounding boxes
    for i in range(0, (max(labels) + 1)):
        objPoints = cPoints[np.where(labels == i)]
        obj.points = o3d.utility.Vector3dVector(objPoints)
        
        oBox = obj.get_axis_aligned_bounding_box()
        oBox.color = (1, 0, 0)
        boxes.append(oBox)

    #o3d.visualization.draw_geometries(boxes)
    
    return boxes


if __name__=="__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--pth", help="specify the path of the pclds", type=str)
    parser.add_argument("--pref", help="specify the prefix of the point clouds", type=str)
    parser.add_argument("--pcNum", help="specify the number of point clouds", nargs='?', const=60, type=int)
    parser.add_argument("--verbose", help="sepcify if extra information should be printed during the process", nargs='?', const=False, type=bool)
    
    args = parser.parse_args()

    pth = args.pth
    pref = args.pref
    pcNum = args.pcNum
    verbose = args.verbose

    #Load in a sample point cloud from some of our simulated data
    pcld = o3d.io.read_point_cloud(pth + pref + str(pcNum) + ".ply")
    pcld_copy = o3d.geometry.PointCloud()

    #Fix the point cloud dimensions so that x is right and z is forward
    arr = np.asarray(pcld.points)
    #arr[:, [0, 1, 2]] = arr[:, [0, 2, 1]]
    pcld.points = o3d.utility.Vector3dVector(arr)
    pcld_copy.points = o3d.utility.Vector3dVector(arr)
  
    #Cluster the point cloud 
    pcld_cluster, labels = clusterFilter(20, 0.3, pcld)

    #Create bounding boxes for all the clusters
    bboxs = objBoundingBoxes(pcld_cluster, labels)
    
    #Display the point cloud and the bounding boxes together
    #pcld.points = o3d.utility.Vector3dVector(arr)
    if verbose:
        print("bounding boxes", len(bboxs))

    bboxs.append(pcld_copy)

    o3d.visualization.draw_geometries(bboxs)
    
    pass
