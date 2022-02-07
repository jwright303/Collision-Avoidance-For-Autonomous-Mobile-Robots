##Program for Object detection on a point cloud

This program works in three main stages. The first stage is loading and cropping the point cloud. In this we remove the floor and some of the noise in the backround of the image

Once the point cloud is cropped, the next step is to preform clustering on the point cloud. We do this using Open3d's DBSCAN algorithm which is a density based clustering algorithm that accounts for noise. The labels of the clustering is returned which we use to remove all the noise, leaving us with just the clusters

Finally, for each cluster we create an axis aligned bounding box for it which acts as our object detection. These bounding boxes are overlayed on the origional point cloud
