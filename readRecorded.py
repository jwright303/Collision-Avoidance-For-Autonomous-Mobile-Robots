import h5Reader as rdr
import open3d as o3d
import numpy as np
import sys
import argparse
import time
from sensor_msgs.msg import PointCloud2
import numpy as np 



def readOneImage():
   
    pc = o3d.io.read_point_cloud("./ptclds/test/d_image_20220420-223040-000.pcd")
    print(pc)
    
   

    ls1, ls2, ls3 = rdr.getAxisLines()
    o3d.visualization.draw_geometries([pc],
                                  zoom=0.3412,
                                  front=[0.4257, -0.2125, -0.8795],
                                  lookat=[2.6172, 2.0475, 1.532],
                                  up=[-0.0694, -0.9768, 0.2024])



if __name__ == '__main__':
    
    readOneImage()
   
