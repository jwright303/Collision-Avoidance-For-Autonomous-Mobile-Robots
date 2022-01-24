from h5Reader import loadPClds 
import open3d as o3d
import h5py

def savePly(pntClds):
  i = 0

  for scene in pntClds:
    geom = o3d.geometry.PointCloud()

    for pcld in scene:
      geom.points = pcld.points
      o3d.io.write_point_cloud("PreAct_3D_F/pcd_" + str(i) + ".ply", geom)
      i = i + 1

    return

    #Update visualizer with the new frame

  return

def main():
  pcds = loadPClds()
  savePly(pcds)

  return

main()
