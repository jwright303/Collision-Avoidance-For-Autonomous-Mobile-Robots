import open3d as o3d
import os
import open3d.ml as _ml3d
import open3d.ml.tf as ml3d
import numpy as np

def random():
  cfg_file = "../Open3D-ML/ml3d/configs/pointpillars_kitti.yml"
  cfg = _ml3d.utils.Config.load_from_file(cfg_file)

  model = ml3d.models.PointPillars(**cfg.model)
  cfg.dataset['dataset_path'] = "./PreAct_3D_F"
  dataset = ml3d.datasets.KITTI(cfg.dataset.pop('dataset_path', None), **cfg.dataset)
  pipeline = ml3d.pipelines.ObjectDetection(model, dataset=dataset, device="gpu", **cfg.pipeline)

  # download the weights.
  ckpt_folder = "./logs/"
  os.makedirs(ckpt_folder, exist_ok=True)
  ckpt_path = ckpt_folder + "pointpillars_kitti_202012221652utc.pth"
  pointpillar_url = "https://storage.googleapis.com/open3d-releases/model-zoo/pointpillars_kitti_202012221652utc.pth"
  if not os.path.exists(ckpt_path):
    cmd = "wget {} -O {}".format(pointpillar_url, ckpt_path)
    os.system(cmd)

  # load the parameters.
  pipeline.load_ckpt(ckpt_path=ckpt_path)

  test_split = dataset.get_split("test")
  data = test_split.get_data(0)

  # run inference on a single example.
  # returns dict with 'predict_labels' and 'predict_scores'.
  result = pipeline.run_inference(data)

  # evaluate performance on the test set; this will write logs to './logs'.
  pipeline.run_test()

  vis = ml3d.vis.Visualizer()
  vis.visualize_dataset(dataset, "all", indices=range(4))
  return

def createData():
  num_points = 100000
  points = np.random.rand(num_points, 3).astype(np.float32)

  data = []
  for i in range(0, 179):
    pc = o3d.io.read_point_cloud("./PreAct_3D_F/pcd_" + str(i) + ".ply")
    dp = {
        'name': 'pc_' + str(i),
        'points': np.asarray(pc.points),
        'random_colors': np.random.rand(*points.shape).astype(np.float32),
        'int_attr': (points[:,0]*5).astype(np.int32)
        }
    data.append(dp)

  return data

def main():
  #dataset = ml3d.datasets.Custom3D(dataset_path='./Toronto_3D')
  #print(pc)
  #print(pc.points)
  #print(len(pc.points))

  #data = o3d.io.read_point_cloud("./Open3D-ML/PreAct_3D_F/pcd_1.ply")

  #print(points.shape)
  #print(data.points)
  data = createData()
  
  model = PointPillars()
  pipeline = ObjectDetection(model=model, dataset=data, max_epoch=100)

  pipeline.run_train()

  #vis = ml3d.vis.Visualizer()
  #vis.visualize(data)


  return

main()

