# CA-ASMR

## Setup
### Needed Packages
To start working with this project, first make sure h5py, opencv (python), numpy, and open3d are installed <br>
Follow the links bellow for instructions on installation. It would also be useful to read through some of the open3d documentation as that is the primary module used

h5py - https://docs.h5py.org/en/stable/build.html#source-installation-on-windows <br>
opencv - https://pypi.org/project/opencv-python/ <br>
open3d - http://www.open3d.org/docs/release/getting_started.html <br>
numpy - https://numpy.org/install/ <br>

### Other Needed Files
Point cloud files are also needed to make use of this repo. They can either be generated from an h5 file using dsetFormat.py, or they can be used directly. If you are generating the point cloud from an h5 file, make sure that you create a directory where they will be stored before running the script, and that you have the h5 file in the same location as the script. If you are using your own point cloud dataset, the format must be as follows:
```
Point_Cloud_Folder
  | pref0.ply
  | pref1.ply
  ...
```
Where pref is your chosen prefix of the point cloud. (This will be supplied through the command line later when running the scripts)

### Other Equipment
For this project we were also given an Esporos ________ camera from our project partners to be able to collect our own point cloud images. While it is not strictly necessary to have a time <br>
of flight camera, some method of obtaining point clouds is needed to be able to make use of this project. It is also important to note that having the right scale of the point clouds is <br>
absolutely necessary to be able to utilize the object detection portion of this project.  

#### Esporos Settings
Mention some of the settings we set for the camera at the very end

## Important Files
The important files in this repository are the following: <br>
  `EdgeDet.py` - Preforms edge detection on an image <br>
  `EdgeDetRT.py` - Preforms edge detection on a stream of images <br>
  `pcCluster.py` - Preforms object detection on an image <br>
  `pcldAnim.py` - Animates the point cloud in the database <br>
  `pcldView.py` - Views a single point cloud <br>
  `objAnim.py` - Animates the point cloud with object detection enabled <br>
  `depthToPC.py` - Converts depth images to point clouds from an h5 file<br>
  `dsetFormat.py` - Creates a dataset from either depth images or point cloud images <br>
  `h5Reader.py` - Reads in point cloud images from an h5 file <br>
  `sim.py` - Simulates the point clouds with object detection and the rules enabled <br>
  
Note that all of these python files should be run on python version 3 or greater. <br>
All of the files except for `h5Reader.py` and `depthToPC.py` take in command line arguments which can be seen by running the program with the -h option (ie. `python3 dsetFormat.py -h`)<br>


## Running
The most relevent program to run is the sim.py program. This program implements the object detection algorithm as well as the rules we created to dertermine when the robot should stop when it detects objects. <br>

The object detection algorithm that it implements is pcCluster, and an example of it running can be found below <br>
See [pcCluster example](https://github.com/jwright303/CA-ASMR/blob/main/OBJREAD.md) for an example of the program running

## Alternative Routes Considered
`Consider breaking this down into Machine Learning Vs Computer Vision then mention all the computer vision options`
During the design phase of our project we considered using a machine learning approach for our object detection. For this method we looked at the PointPillars, You Only Look Once (YOLO), ** <br>
models. While Open3d does provide modules to support this, they require large labeled datasets. Due to the limited time and access to point clouds, we decided to go with a different computer vision based approach. Another option we considered for this project was an edge detection based method.


## Reasoning For Our Approach

## Future Projects

##  
