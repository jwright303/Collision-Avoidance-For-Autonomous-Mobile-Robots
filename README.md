# CA-ASMR

### Importance of Collision Avoidance for AMR

Today, robots are becoming increasingly more and more popular and used in many industries. Robots need to maneuver around their environment safely and require a system to detect objects. Our project Collision Avoidance for Autonomous Mobile Robots aims to become the vision for autonomous mobile robots through the use of a suite of detection tools. These tools are developed to assist the autonomous mobile robots in avoiding collisions with objects such as boxes, tables, chairs, as well as avoiding falling off edges/cliffs like sidewalks. 

These detection tools utilize point cloud simulation and bounding boxes as the tools for achieving the object and edge detection. We used simulated data when initially developing the tools. Then we proceeded to obtain some data captured by a ESPROS TOF camera 660, that is in the form of a depth image. These depth images are then converted to a point cloud for usable information used the detection tools. Some applications that object and edge detection might be useful in would include warehouse management, delivery services, cars (self-driving/additional features), security cameras, and so much more. All of these applications would benefit primarily from the increase of efficiency and consequently drive up the profit margin for businesses who incorporate these tools into their operations.

### Our experience beginning

To begin developing and continue the work for this project, you will need to install ROS2 on your system for the robot operating system, as well as QTcreator the IDE. The ROS2 Galactic installation instructions can be found at https://docs.ros.org/en/galactic/Installation.html. The QTcreator installation can be found at https://www.qt.io/download, selecting the try qt option. Similarly like the software required for development. You will also require a ESPROS TOF camera 660 as the capturing device https://www.espros.com/photonics/tofcam660/#pictures. 

Before using the ESPROS TOF camera 660, you will first need to calibrate the specifications of the camera to correctly utilize it. We would recommend that you should ask for guidance from PreAct Technologies (our project partner at the time) as to what the ESPROS TOF camera 660 specifications should be. After the calibration of the camera specifications, the raw data captured from the ESPROS TOF camera 660 will then need to be exported as a ply file usable for point clouds. There are multiple methods available to export the raw data captured from the camera to a ply file. Specifically EPROS has their own software interface for the camera that contains a feature to export as a ply file. Other methods include using functions from modules such as open3d and h5 to convert the depth image into a ply file. Initially our group used the ESPROS software to convert the raw data to ply files. But we were experiencing issues so, our group has been utilizing the depth images captured from the camera and converting them to ply files.

## Setup
### Needed Packages
To start working with this project, first make sure h5py, opencv (python), numpy, and open3d are installed <br>
Follow the links bellow for instructions on installation

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
