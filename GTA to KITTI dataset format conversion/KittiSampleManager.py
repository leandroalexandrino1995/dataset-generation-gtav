from pathlib import Path
import numpy as np
import os.path
import math
import struct
import GtaSample
import kitti_util
from pointcloud_utils import saveKittiVelodyneFile, addIntensityToPointCloud
from Calibration import Calibration
from Labeling import Labeling
from UiConfigParams import ConfigParams


'''
Kitti sample class
Used to create a sample instance
'''
class KittiSampleManager():
    def __init__(self, gtaSample, outputRootDir, sampleCounter, configurations, noBackground=False):
        '''
        Arguments:
            - configurations: UiConfigParams object
        '''
        self.kittiOutputSamplesDir = outputRootDir
        self.kittiLabelsDir = outputRootDir + configurations.kittiLabelsDir
        self.kittiVelodyneDir = outputRootDir + configurations.kittiVelodyneDir
        self.kittiViewsDir = outputRootDir + configurations.kittiViewsDir
        self.kittiCalibDir = outputRootDir + configurations.kittiCalibDir

        self.kittiLabelsDirTesting = outputRootDir + configurations.kittiLabelsDirTesting
        self.kittiVelodyneDirTesting = outputRootDir + configurations.kittiVelodyneDirTesting
        self.kittiViewsDirTesting = outputRootDir + configurations.kittiViewsDirTesting
        self.kittiCalibDirTesting = outputRootDir + configurations.kittiCalibDirTesting

        self.kittiLabelsDirExtra = outputRootDir + configurations.kittiLabelsDirExtra
        self.kittiVelodyneDirExtra = outputRootDir + configurations.kittiVelodyneDirExtra
        self.kittiViewsDirExtra = outputRootDir + configurations.kittiViewsDirExtra
        self.kittiCalibDirExtra = outputRootDir + configurations.kittiCalibDirExtra

        self.gtaSample = gtaSample

        #self.fov = 75   # even though I use 50 in the horizontal fov of gta
        #self.num_views = 1 # number of views to consider (only 1, the front view)
        self.configurations = configurations

        self.noBackground = noBackground

        # if no entries in the label file were created
        self.isEmpty = False

        self.createKittiFormatedDataset(sampleCounter, configurations)

    def createKittiFormatedDataset(self, sampleCounter, configurations):
        # generate file name
        n_digits = len(str(sampleCounter)) if sampleCounter < 7481 else len(str(sampleCounter-7481))
        output_file_name = ""               # ex: 000000.txt
        for i in range(0, 6-n_digits):
            output_file_name = output_file_name + "0"
        
        if len(output_file_name) != 6:
            output_file_name = output_file_name + str(sampleCounter) if sampleCounter < 7481 else output_file_name + str(sampleCounter-7481) 

        # create the hierarchy of directories
        Path(self.kittiOutputSamplesDir).mkdir(parents=True, exist_ok=True)
        Path(self.kittiViewsDir).mkdir(parents=True, exist_ok=True)
        Path(self.kittiVelodyneDir).mkdir(parents=True, exist_ok=True)
        Path(self.kittiLabelsDir).mkdir(parents=True, exist_ok=True)
        Path(self.kittiCalibDir).mkdir(parents=True, exist_ok=True)

        Path(self.kittiViewsDirTesting).mkdir(parents=True, exist_ok=True)
        Path(self.kittiVelodyneDirTesting).mkdir(parents=True, exist_ok=True)
        Path(self.kittiLabelsDirTesting).mkdir(parents=True, exist_ok=True)
        Path(self.kittiCalibDirTesting).mkdir(parents=True, exist_ok=True)

        Path(self.kittiLabelsDirExtra).mkdir(parents=True, exist_ok=True)
        Path(self.kittiVelodyneDirExtra).mkdir(parents=True, exist_ok=True)
        Path(self.kittiViewsDirExtra).mkdir(parents=True, exist_ok=True)
        Path(self.kittiCalibDirExtra).mkdir(parents=True, exist_ok=True)

        # save image
        if sampleCounter < 7481:
            self.gtaSample.imageView.saveImage(self.gtaSample.imageView.kittiImage, self.kittiViewsDir, output_file_name + ".png")
        elif sampleCounter < 14999:
            self.gtaSample.imageView.saveImage(self.gtaSample.imageView.kittiImage, self.kittiViewsDirTesting, output_file_name + ".png")
        else:
            self.gtaSample.imageView.saveImage(self.gtaSample.imageView.kittiImage, self.kittiViewsDirExtra, output_file_name + ".png")
        
        if configurations.includeIntensity[0]:
            # save point cloud - the full rotated point cloud
            if sampleCounter < 7481:
                saveKittiVelodyneFile(addIntensityToPointCloud(self.gtaSample.pcData.list_rotated_raw_pc, dummy_value=self.configurations.includeIntensity[1]), output_file_name + ".bin", self.kittiVelodyneDir)
            elif sampleCounter < 14999:
                saveKittiVelodyneFile(addIntensityToPointCloud(self.gtaSample.pcData.list_rotated_raw_pc, dummy_value=self.configurations.includeIntensity[1]), output_file_name + ".bin", self.kittiVelodyneDirTesting)
            else:
                saveKittiVelodyneFile(addIntensityToPointCloud(self.gtaSample.pcData.list_rotated_raw_pc, dummy_value=self.configurations.includeIntensity[1]), output_file_name + ".bin", self.kittiVelodyneDirExtra)
        else:
            if sampleCounter < 7481:
                saveKittiVelodyneFile(self.gtaSample.pcData.list_rotated_raw_pc, output_file_name + ".bin", self.kittiVelodyneDir)
            elif sampleCounter < 14999:
                saveKittiVelodyneFile(self.gtaSample.pcData.list_rotated_raw_pc, output_file_name + ".bin", self.kittiVelodyneDirTesting)
            else:
                saveKittiVelodyneFile(self.gtaSample.pcData.list_rotated_raw_pc, output_file_name + ".bin", self.kittiVelodyneDirExtra)
        
        # save calibration info
        calib = Calibration((self.gtaSample.imageView.kittiImage.shape[1], self.gtaSample.imageView.kittiImage.shape[0]), self.configurations.fov)
        if sampleCounter < 7481:
            calib.saveCalibrationFile(self.kittiCalibDir, output_file_name + ".txt")
        elif sampleCounter < 14999:
            calib.saveCalibrationFile(self.kittiCalibDirTesting, output_file_name + ".txt")
        else:
            calib.saveCalibrationFile(self.kittiCalibDirExtra, output_file_name + ".txt")

        # labels info
        if sampleCounter < 7481:
            label = Labeling(self.gtaSample, calib, self.kittiLabelsDir, output_file_name + ".txt", configurations, fv_only_entities=True)

            if label.isEmpty:
                self.isEmpty = True
                # print("Gta Sample doesn't have entities! It will be ignored.") # <- tirei aqui
                # remove sample with empty label file
                os.remove(self.kittiVelodyneDir + output_file_name + ".bin")
                os.remove(self.kittiViewsDir + output_file_name + ".png")
                os.remove(self.kittiCalibDir + output_file_name + ".txt")

        elif sampleCounter < 14999:
            label = Labeling(self.gtaSample, calib, self.kittiLabelsDirTesting, output_file_name + ".txt", configurations, fv_only_entities=True)

            # try:
            #     os.remove(self.kittiLabelsDirTesting + output_file_name + ".txt")
            # except FileNotFoundError:
            #     pass


            if label.isEmpty:
                self.isEmpty = True
                # print("Gta Sample doesn't have entities! It will be ignored.") # <- tirei aqui
                # remove sample with empty label file
                os.remove(self.kittiVelodyneDirTesting + output_file_name + ".bin")
                os.remove(self.kittiViewsDirTesting + output_file_name + ".png")
                os.remove(self.kittiCalibDirTesting + output_file_name + ".txt")

        else:
            label = Labeling(self.gtaSample, calib, self.kittiLabelsDirExtra, output_file_name + ".txt", configurations, fv_only_entities=True)

            # try:
            #     os.remove(self.kittiLabelsDirTesting + output_file_name + ".txt")
            # except FileNotFoundError:
            #     pass


            if label.isEmpty:
                self.isEmpty = True
                # print("Gta Sample doesn't have entities! It will be ignored.") # <- tirei aqui
                # remove sample with empty label file
                os.remove(self.kittiVelodyneDirExtra + output_file_name + ".bin")
                os.remove(self.kittiViewsDirExtra + output_file_name + ".png")
                os.remove(self.kittiCalibDirExtra + output_file_name + ".txt")







