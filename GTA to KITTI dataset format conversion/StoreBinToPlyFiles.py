import os
from GtaSample import GtaSample
from KittiSample import KittiSample
from LoadBinPointclouds import loadKittiVelodyneFile
from LoadBinPointclouds import savePlyFile
from kitti_util import compute_box_3d
#from KittiSample import inverse_rigid_trans

pathToPointcloudBinDirectory = 'D:/Desktop/BinToPly/FromBin/'

outputpath = 'D:/Desktop/BinToPly/ToPly/'

counter = 0

# Create ply point clouds from bin pointclouds (with intensity) from kitti dataset, with a red-green color contrast to trepresent the intensity value of each point
for subdir, dirs, files in os.walk(pathToPointcloudBinDirectory):

    for filename in files:

        # dimensions of the cars in a label
        label_cars_dims = []

        kittipointcloud = loadKittiVelodyneFile(pathToPointcloudBinDirectory + filename, include_luminance = True)

        savePlyFile(outputpath + filename.split('.')[0] + ".ply", kittipointcloud)
        savePlyFile(outputpath + filename.split('.')[0] + "_intensity" + ".ply", kittipointcloud, attributes = 'i')

        counter+=1

        # print(str(int(counter/len(files) * 100)) + '%') # <- tirei aqui

