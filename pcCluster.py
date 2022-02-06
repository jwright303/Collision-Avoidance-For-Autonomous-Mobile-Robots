import open3d as o3d
import cv2
import time
import matplotlib.pyplot as plt
import numpy as np

def clusterFilter(mp, pcld):
    print("Minimum Points: ", mp)

    pcld = o3d.io.read_point_cloud("./PreAct_3D_F/pcd_80.ply")
    pcld_copy = o3d.geometry.PointCloud()
      
    arr = np.asarray(pcld.points)

    arr[:, [0, 1, 2]] = arr[:, [0, 2, 1]]
    pcld_copy.points = o3d.utility.Vector3dVector(arr)


    newA = arr[np.logical_and(arr[:,1] > 0.08, arr[:,1] < 6)]
    newA = newA[newA[:,2] < 10.5]
    
    pcld.points = o3d.utility.Vector3dVector(newA)

    labels = np.array(pcld.cluster_dbscan(eps=0.3, min_points=mp, print_progress=True))
    max_label = labels.max()
    
    print(f"Number of labels: {max_label + 1}\n")
    print("Labels len", len(labels))
    
    colors = plt.get_cmap("tab20")(labels / (max_label if max_label > 0 else 1))
    colors[labels < 0] = 0
    
    print("Colors arr")
    print(np.asarray(colors))

    print("labels arr")
    print(np.asarray(colors).shape)
    print(np.asarray(labels).shape)
    print(len(labels))
    print(max(labels))

    aFin = newA[colors[:,3] != 0]
    labels = labels[colors[:,3] != 0]
    colors = colors[colors[:,3] != 0]

    pcld.points = o3d.utility.Vector3dVector(aFin)
    pcld.colors = o3d.utility.Vector3dVector(colors[:, :3])

    o3d.visualization.draw_geometries([pcld])
    o3d.visualization.draw_geometries([pcld_copy, pcld])
    
    return pcld, labels

def objBoundingBoxes(pcld_cluster, labels):

    obj = o3d.geometry.PointCloud()
    cPoints = np.asarray(pcld_cluster.points)
    print(cPoints.shape)
    boxes = []
    
    for i in range(1, max(labels) + 1):
        objPoints = cPoints[np.where(labels == i)]
        obj.points = o3d.utility.Vector3dVector(objPoints)
        
        oBox = obj.get_axis_aligned_bounding_box()
        oBox.color = (1, 0, 0)
        boxes.append(oBox)

    #o3d.visualization.draw_geometries(boxes)
    
    return boxes


if __name__=="__main__":
    pcld = o3d.io.read_point_cloud("./PreAct_3D_F/pcd_80.ply")
  
    pcld_cluster, labels = clusterFilter(30, pcld)

    bboxs = objBoundingBoxes(pcld_cluster, labels)
    

    arr = np.asarray(pcld.points)

    arr[:, [0, 1, 2]] = arr[:, [0, 2, 1]]
    pcld.points = o3d.utility.Vector3dVector(arr)
    bboxs.append(pcld)

    o3d.visualization.draw_geometries(bboxs)
    



    pass
