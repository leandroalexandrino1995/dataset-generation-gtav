"""
Created on Sat Mar 24 12:38:17 2018
The KITTI is one of the well known benchmarks for 3D Object detection. Working 
on this dataset requires some understanding of what the different files and their
contnts are. In this piece we use  4 different types of files used from the 
KITTI 3D Objection Detection dataset as follows to do some basic manipulation 
and sanity checks to get basic underdstanding. 
 camera2 image (.png), 
 camera2 label label (.txt),
 calibration (.txt), 
 velodyne point cloud (.bin),
Codes to project 3D data from  camera co-ordinate and velodyne coordinate to  
camera image.  The goal is to see if the  data along with appropriate geometry 
matrices are handled correctly.  2 different types of images are generated - 
camera2 image and bird's eye view of point cloud.  
@author: sg
Refs :
  1. Vision meets Robotics: The KITTI Dataset - http://www.cvlibs.net/publications/Geiger2013IJRR.pdf
  2. 3D Object Detection Evaluation 2017 - http://www.cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d
  3. Download left color images of object data set (12 GB) - http://www.cvlibs.net/download.php?file=data_object_image_2.zip
  4. Download Velodyne point clouds, if you want to use laser information (29 GB) - http://www.cvlibs.net/download.php?file=data_object_velodyne.zip
  5. Download camera calibration matrices of object data set (16 MB) - http://www.cvlibs.net/download.php?file=data_object_calib.zip
  6. Download training labels of object data set (5 MB) - http://www.cvlibs.net/download.php?file=data_object_label_2.zip
  7. Download object development kit (1 MB) (including 3D object detection and bird's eye view evaluation code) - http://kitti.is.tue.mpg.de/kitti/devkit_object.zip
  
"""

import os
import os.path
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from   matplotlib.path import Path
from matplotlib import colors
import numpy as np
from PIL import Image
from math import sin, cos
import argparse

from numpy.testing._private.utils import clear_and_catch_warnings


# basedir = 'C:/data/kitti/data_small/training' # windows
basedir = '../../../MaterialHash_noBackground/GTAtoKITTI/kitti/training/'
# basedir = '../../../KITTI/training/'
# basedir = '../../../Diogo/training/'
# basedir = '../../../Diogo/kitti/training/'
# basedir = 'data' # *nix
left_cam_rgb= 'image_2'
label = 'label_2'
velodyne = 'velodyne'
calib = 'calib'

savedir = "../../../eyeball_test/all_train/"
# savedir = "../../../KITTI/all_train/"
# savedir = "../../../Diogo/all_train/"
# savedir = "../../../Diogo/all_training/"


def loadKittiFiles (frame) :
  '''
  Load KITTI image (.png), calibration (.txt), velodyne (.bin), and label (.txt),  files
  corresponding to a shot.
  Args:
    frame :  name of the shot , which will be appended to externsions to load
                the appropriate file.
  '''
  # load image file 
  fn = basedir+ left_cam_rgb + frame+'.png'
  fn = os.path.join(basedir, left_cam_rgb, frame+'.png')
  left_cam = Image.open(fn).convert ('RGB')
  
  # load velodyne file 
  fn = basedir+ velodyne + frame+'.bin'
  fn = os.path.join(basedir, velodyne, frame+'.bin')
  velo = np.fromfile(fn, dtype=np.float32).reshape(-1, 4)
  
  # load calibration file
  fn = basedir+ calib + frame+'.txt'
  fn = os.path.join(basedir, calib, frame+'.txt')
  calib_data = {}
  with open (fn, 'r') as f :
    for line in f.readlines():
      if ':' in line :
        key, value = line.split(':', 1)
        calib_data[key] = np.array([float(x) for x in value.split()])
  
  # load label file
  fn = basedir+ label + frame+'.txt'
  fn = os.path.join(basedir, label, frame+'.txt')
  label_data = {}
  with open (fn, 'r') as f :
    for line in f.readlines():
      if len(line) > 3:
        key, value = line.split(' ', 1)
        #print ('key', key, 'value', value)
        if key in label_data.keys() :
          label_data[key].append([float(x) for x in value.split()] )
        else:
          label_data[key] =[[float(x) for x in value.split()]]

  for key in label_data.keys():
    label_data[key] = np.array( label_data[key])
    
  return left_cam, velo, label_data, calib_data



def computeBox3D(label, P, ratio=1):
  '''
  takes an object label and a projection matrix (P) and projects the 3D
  bounding box into the image plane.
  
  (Adapted from devkit_object/matlab/computeBox3D.m)
  
  Args:
    label -  object label list or array
  '''
  w = label[7]
  h = label[8]*ratio
  l = label[9]
  x = label[10]
  y = label[11]
  z = label[12]
  ry = label[13]
  
  # compute rotational matrix around yaw axis
  R = np.array([ [+cos(ry), 0, +sin(ry)],
                 [0,        1,        0],
                 [-sin(ry), 0, +cos(ry)] ] )

  # 3D bounding box corners

  x_corners = [0, l, l, l, l, 0, 0, 0] # -l/2
  y_corners = [0, 0, h, h, 0, 0, h, h] # -h
  z_corners = [0, 0, 0, w, w, w, w, 0] # --w/2
  
  x_corners += -l/2
  y_corners += -h
  z_corners += -w/2
  
  # print(y_corners)
  
  # bounding box in object co-ordinate
  corners_3D = np.array([x_corners, y_corners, z_corners])
  # print ( 'corners_3d', corners_3D.shape, corners_3D)
  
  # rotate 
  corners_3D = R.dot(corners_3D)
  # print ( 'corners_3d', corners_3D.shape, corners_3D)
  
  #translate 
  corners_3D += np.array([x, y, z]).reshape((3,1))
  

  
  corners_3D_1 = np.vstack((corners_3D,np.ones((corners_3D.shape[-1]))))
  corners_2D = P.dot (corners_3D_1)
  corners_2D = corners_2D/corners_2D[2]

  # edges, lines 3d/2d bounding box in vertex index 
  edges = [[0,1], [1,2], [2,3], [3,4], [4,5], [5,6], [6,7], [7,0], [0,5], [1,4], [2,7], [3, 6]]
  lines = [[0,1], [1,2], [2,3], [3,4], [4,5], [5,6], [6,7], [7,0], [0,5], [5, 4], [4, 1], [1,2], [2,7], [7,6], [6,3]]
  bb3d_lines_verts_idx = [0,1,2,3,4,5,6,7,0,5,4,1,2,7,6,3]
  
  bb2d_lines_verts = corners_2D[:,bb3d_lines_verts_idx] # 

  # print(bb2d_lines_verts[:2])
  aux = bb2d_lines_verts[1]
  ratio = max(aux)-min(aux)
   
  return corners_2D[:2], corners_3D, bb2d_lines_verts[:2], ratio, h
  
  
  
 
def labelToBoundingBox(ax, labeld, calibd):
  '''
  Draw 2D and 3D bounding boxes.  
  
  Each label  file contains the following ( copied from devkit_object/matlab/readLabels.m)
  #  % extract label, truncation, occlusion
  #  lbl = C{1}(o);                   % for converting: cell -> string
  #  objects(o).type       = lbl{1};  % 'Car', 'Pedestrian', ...
  #  objects(o).truncation = C{2}(o); % truncated pixel ratio ([0..1])
  #  objects(o).occlusion  = C{3}(o); % 0 = visible, 1 = partly occluded, 2 = fully occluded, 3 = unknown
  #  objects(o).alpha      = C{4}(o); % object observation angle ([-pi..pi])
  #
  #  % extract 2D bounding box in 0-based coordinates
  #  objects(o).x1 = C{5}(o); % left   -> in pixel
  #  objects(o).y1 = C{6}(o); % top
  #  objects(o).x2 = C{7}(o); % right
  #  objects(o).y2 = C{8}(o); % bottom
  #
  #  % extract 3D bounding box information
  #  objects(o).h    = C{9} (o); % box width    -> in object coordinate
  #  objects(o).w    = C{10}(o); % box height
  #  objects(o).l    = C{11}(o); % box length
  #  objects(o).t(1) = C{12}(o); % location (x) -> in camera coordinate 
  #  objects(o).t(2) = C{13}(o); % location (y)
  #  objects(o).t(3) = C{14}(o); % location (z)
  #  objects(o).ry   = C{15}(o); % yaw angle  -> rotation aroun the y/vetical axis
  '''
  
  # Velodyne to/from referenece camera (0) matrix
  Tr_velo_to_cam = np.zeros((4,4))
  Tr_velo_to_cam[3,3] = 1
  Tr_velo_to_cam[:3,:4] = calibd['Tr_velo_to_cam'].reshape(3,4)
  #print ('Tr_velo_to_cam', Tr_velo_to_cam)
  
  Tr_cam_to_velo = np.linalg.inv(Tr_velo_to_cam)
  #print ('Tr_cam_to_velo', Tr_cam_to_velo)
  
  # 
  R0_rect = np.zeros ((4,4))
  R0_rect[:3,:3] = calibd['R0_rect'].reshape(3,3)
  R0_rect[3,3] = 1
  #print ('R0_rect', R0_rect)
  P2_rect = calibd['P2'].reshape(3,4)
  #print('P2_rect', P2_rect)
  
  bb3d = []
  bb2d = []
  
  hs = []

  for key in labeld.keys ():
    
    color = 'white'
    if key == 'Car':
      color = 'red'
    elif key == 'Pedestrian':
      color = 'pink'
    elif key == 'DontCare':
      color = 'white'
    
   
    for o in range( labeld[key].shape[0]):
      
      #2D
      left   = labeld[key][o][3]
      bottom = labeld[key][o][4]
      width  = labeld[key][o][5]- labeld[key][o][3]
      height = labeld[key][o][6]- labeld[key][o][4]
      
      p = patches.Rectangle(
        (left, bottom), width, height, fill=False, edgecolor=color, linewidth=1)
      ax.add_patch(p)
      
      xc = (labeld[key][o][5]+labeld[key][o][3])/2
      yc = (labeld[key][o][6]+labeld[key][o][4])/2
      bb2d.append([xc,yc])
      
      #3D
      w3d = labeld[key][o][7]
      h3d = labeld[key][o][8]
      l3d = labeld[key][o][9]
      x3d = labeld[key][o][10]
      y3d = labeld[key][o][11]
      z3d = labeld[key][o][12]
      yaw3d = labeld[key][o][13]
      
   
      if key != 'DontCare' :
        
        corners_2D, corners_3D, paths_2D, ratio, h = computeBox3D(labeld[key][o], P2_rect)
        # corners_2D, corners_3D, paths_2D, ratio, h = computeBox3D(labeld[key][o], P2_rect, height/ratio)
        verts = paths_2D.T # corners_2D.T
        codes = [Path.LINETO]*verts.shape[0]
        codes[0] = Path.MOVETO
        pth  = Path (verts, codes)
        p = patches.PathPatch( pth, fill=False, color='purple', linewidth=2)
        ax.add_patch(p)
        hs.append(h)
        
        
  
  # a sanity test point in velodyne co-ordinate to check  camera2 imaging plane projection
#   testp = [ 11.3, -2.95, -1.0]
#   bb3d.append(testp)
  
#   xnd = np.array(testp+[1.0])
#   #print ('bb3d xnd velodyne   ', xnd)
#   #xpnd = P2.dot(R0_rect.dot(Tr_velo_to_cam.dot(xnd)))
#   xpnd = Tr_velo_to_cam.dot(xnd)
#   #print ('bb3d xpnd cam0      ', xpnd)
#   xpnd = R0_rect.dot(xpnd)
#   #print ('bb3d xpnd rect cam0 ', xpnd)
#   xpnd = P2_rect.dot(xpnd)
#   #print ('bb3d xpnd cam2 image', xpnd)
#   #print ('bb3d xpnd cam2 image', xpnd/xpnd[2])
  
#   p = patches.Circle( (xpnd[0]/xpnd[2], xpnd[1]/xpnd[2]), fill=False, radius=3, color='red', linewidth=2)
#   ax.add_patch(p)
  
  return np.array(bb2d), np.array(bb3d), corners_3D, hs

def pointCloudToBirdsEyeView(ax2, velo, bb3d):
  ax2.set_xlim (-10,10)
  ax2.set_ylim (-5,35)
  hmax = velo[:,2].max()
  hmin = velo[:,2].min()
  hmean = velo[:, 2].mean()
  hmeadian = np.median ( velo[:, 2] )
  hstd = np.std(velo[:, 2])
  #print ('scalledh', hmax, hmean, hmeadian, hmin, hstd, scalledh.shape, scalledh[:10])
  norm = colors.Normalize(hmean-2*hstd, hmean+2*hstd, clip=True)
  sc2= ax2.scatter(-velo[:,1],
             velo[:,0],
             s = 1,
             c=velo[:,2],
             cmap = 'viridis',
             norm=norm,
             marker = ".",
             )
  ax2.scatter(-bb3d[:,1],
             bb3d[:,0],
             c='red')
  ax2.set_facecolor('xkcd:grey')
  plt.colorbar(sc2)

def main ():
  """
  Completes the plots 
  """

  # for subdir, dirs, files in os.walk(basedir+"/image_2/"):
  #   for file in files:
  #     frame = file[:-4]

  # return

  for frame in ["000000", "000001", "000150", "000205", "000775", "000808", "000871", "001584", "001599", "001955", "002738", "003473", "003592", "007328"]:
      left_cam, velo, label_data, calib_data = loadKittiFiles(frame)
      
      print(label_data)

      f = plt.figure()
      
      # show the left camera image 
      ax = f.add_subplot(111)
      ax.imshow(left_cam)
      
      
      bb2d, bb3d, corners3d, hs = labelToBoundingBox(ax, label_data, calib_data)

      plt.title(frame)
      plt.savefig(savedir+"/"+frame+"_withBB_github.png")


      # plt.savefig("/home/joao/Desktop/Diogo/"+frame+"_withBB_github.png")
      
      # point cloud to bird's eye view scatter plot
      # ax2 = f.add_subplot(3,1,2, )#projection="3d" )
      # pointCloudToBirdsEyeView(ax2, velo, bb3d)

      # to_write = "ply\nformat ascii 1.0\nelement vertex " + str(velo.shape[0]+corners3d.shape[1]) +  "\nproperty float x\nproperty float y\nproperty float z\nproperty float intensity\nend_header\n"
      
      # x = velo[:,0]
      # y = velo[:,1]
      # z = velo[:,2]
      # r = velo[:,3]

      # for i in range(velo.shape[0]):
      #     to_write += str(x[i]) + " " + str(y[i]) + " " + str(z[i]) + " " + str(r[i]) + "\n"

      # for i in range(corners3d.shape[1]):
      #     to_write += str(corners3d[0,i]) + " " + str(corners3d[1,i]) + " " + str(corners3d[2,i]) + " 1\n"

      # with open(savedir+"/"+frame+"_github.ply", "w") as f:
      # # with open("/home/joao/Desktop/Diogo/"+frame+"_github.ply", "w") as f:
      #     f.write(to_write)


if __name__ == '__main__':
  main()

