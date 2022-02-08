## Program for Object detection on a point cloud

This program works in three main stages. The first stage is loading and cropping the point cloud. In this we remove the floor and some of the noise in the backround of the image

<img width="527" alt="Screen Shot 2022-02-07 at 10 33 15 AM" src="https://user-images.githubusercontent.com/41707123/152850037-8f420b5f-19cc-449f-aec1-27674406561b.png">
<img width="679" alt="Screen Shot 2022-02-07 at 10 34 04 AM" src="https://user-images.githubusercontent.com/41707123/152850142-774ba9f3-738d-4008-a252-7a99d4b830c9.png">

Once the point cloud is cropped, the next step is to preform clustering on the point cloud. We do this using Open3d's DBSCAN algorithm which is a density based clustering algorithm that accounts for noise. The labels of the clustering is returned which we use to remove all the noise, leaving us with just the clusters

<img width="613" alt="Screen Shot 2022-02-07 at 10 34 46 AM" src="https://user-images.githubusercontent.com/41707123/152850243-b6febdd6-9323-4a6c-8fed-69349385a4de.png">
<img width="591" alt="Screen Shot 2022-02-07 at 10 35 11 AM" src="https://user-images.githubusercontent.com/41707123/152850290-aac2ec84-26c1-45b2-96a2-e41a781c4df0.png">

Finally, for each cluster we create an axis aligned bounding box for it which acts as our object detection. These bounding boxes are overlayed on the origional point cloud

<img width="601" alt="Screen Shot 2022-02-07 at 10 35 50 AM" src="https://user-images.githubusercontent.com/41707123/152850393-b0ed0e34-32e8-49f5-908d-4b6c6d15d435.png">
