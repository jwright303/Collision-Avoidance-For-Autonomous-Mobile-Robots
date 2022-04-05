# CA-ASMR

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
The most relevent programs to run are pcCluster.py and sim.py. pcCluster

See [pcCluster example](https://github.com/jwright303/CA-ASMR/blob/main/OBJREAD.md) for an example of the program running
