# CA-ASMR

## Setup
### Needed Packages
To start working with this project, first make sure h5py, opencv (python), numpy, and open3d are installed
Follow the links bellow for instructions on installation

h5py - https://docs.h5py.org/en/stable/build.html#source-installation-on-windows
opencv - https://pypi.org/project/opencv-python/
open3d - http://www.open3d.org/docs/release/getting_started.html
numpy - https://numpy.org/install/

### Other Needed Files
Point cloud files are also needed to make use of this repo. They can either be generated from an h5 file or they can be used directly.

## Important Files
The important files in this repository are the following: <br>
  `EdgeDet.py` - Preforms edge detection on an image <br>
  `EdgeDetRT.py` - Preforms edge detection on a stream of images <br>
  `pcCluster.py` - Preforms object detection on an image <br>
  `pcldAnim.py` - Animates the point cloud in the database <br>
  `pcldView.py` - Views a single point cloud <br>
  `objAnim.py` - Animates the point cloud with object detection enabled <br>


## Running
To run pcCluster.py program enter the command below:
```
python pcCluster.py [pcld_index] [verbose]
```
The bracketed sections indicate optional parameters to pass into the program <br>
  [pcld_index] - Supplies the specific index for the program to work with (0-178) <br>
  [verbose] - This will print out the result of each operation on the point cloud <br>

See [pcCluster example](https://github.com/jwright303/CA-ASMR/blob/main/OBJREAD.md) for an example of the program running
