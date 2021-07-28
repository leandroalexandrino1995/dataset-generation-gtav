import os
from GtaSample import GtaSample

#from KittiSample import KittiSample
from LoadBinPointclouds import loadKittiVelodyneFile
from LoadBinPointclouds import savePlyFile
import argparse
from dataclasses import dataclass
from UiConfigParams import ConfigParams, EntityType, PointAttributes
from KittiSampleManager import KittiSampleManager

import sys

import string

# kitti labels output directory
#kittiLabelsDir = 'data_object_label_2/training/label_2/'
# velodyne samples output directory
#kittiVelodyneDir = 'data_object_velodyne/training/'
# image view samples output directory
#kittiViewsDir = 'data_object_image_2/training/'
# calibration matrices samples output directory
#kittiCalibDir = 'data_object_calib/training/calib/'

def compute(rootDir, rootKittiOutputDir, configurations):
    
    # to generate the naming sequence for the kitti samples
    gtaSampleCounter = len(os.listdir(rootDir))

    try:
        kittiTrainSampleCounter = len(os.listdir(rootKittiOutputDir+ConfigParams.kittiLabelsDir))
    except FileNotFoundError:
        kittiTrainSampleCounter = 0
    
    try:
        kittiTestSampleCounter = len(os.listdir(rootKittiOutputDir+ConfigParams.kittiVelodyneDirTesting))
    except FileNotFoundError:
        kittiTestSampleCounter = 0

    kittiSampleCounter = kittiTrainSampleCounter + kittiTestSampleCounter

    # print(len(os.listdir(rootKittiOutputDir+"/data_object_label_2/training/label_2")))

    print("Current number of samples in " + rootKittiOutputDir + ": " + str(kittiSampleCounter))
    print("Current number of training samples: " + str(kittiTrainSampleCounter))
    print("Current number of testing samples: " + str(kittiTestSampleCounter))
    print("Number of GTA samples: " + str(gtaSampleCounter))

    f = open("GTASample.txt", "r")
    GTAFolder = int(f.read())
    toSave = GTAFolder
    # GTAFolder = int(GTAFolder.replace('LiDAR_PointCloud',''))
    # print(GTAFolder)

    # walk through all samples in rootDir and create the kitti output accordingly
    for subdir, dirs, files in os.walk(rootDir):
        # preserve the order of the original point clouds
        dirs = sorted(dirs, key=lambda filename: int(filename.replace('LiDAR_PointCloud','')))
        for dirName in dirs[GTAFolder:]:
            # print('\n\n::::::: Current sample directory: ' + dirName + ' :::::::') # Não vale a pena ter com o txt
            
            try:

                # load sample (point cloud + front view image) and create the original pointcloud, a rotated point cloud, a front view point cloud, the kitti dataset resolution image
                pc_sample1 = GtaSample(rootDir + dirName, configurations)   
                
                # save the original point cloud (not rotated) into a file
                #pc_sample1.savePlyFile('Original point cloud.ply', pc_sample1.pcData.list_raw_pc)
                
                # pc_sample1.savePlyFile(configurations.rotatedPointCloudFn, pc_sample1.pcData.list_rotated_raw_pc)
                
                # pc_sample1.savePlyFile(configurations.frontviewPointCloudFn, pc_sample1.pcFvData.list_rotated_raw_pc)
                
                # create a point cloud only with points with label = 2, vehicles
                #pc_sample1.pcFvData. \
                #    generateSingleCategoryPointCloud(2, category_name="vehicles", debug_mode=False)

                pc_sample1.pcData. \
                    generateSingleCategoryPointCloud(EntityType.VEHICLE.value, category_name="vehicles", debug_mode=False)
                
                pc_sample1.pcData. \
                    generateSingleCategoryPointCloud(EntityType.PEDESTRIAN.value, category_name='pedestrians', debug_mode=False)
                
                # if no vehicle points were detected in the front view point cloud, pass to the next sample
                
                # ignore sample if it does not contain any of the desired entity types 
                # if not EntityType.VEHICLE.value in pc_sample1.pcFvData.single_category_pcs_list.keys() \
                #     and not EntityType.PEDESTRIAN.value in pc_sample1.pcFvData.single_category_pcs_list.keys():
                #     continue

                if configurations.genSingleEntities:
                    if EntityType.VEHICLE.value in pc_sample1.pcFvData.single_category_pcs_list.keys():
                        # save the vehicles frontview pointcloud into a file 
                        pc_sample1.savePlyFileFromDict(configurations.vehiclesOnlyPointCloudFn, \
                            pc_sample1.pcData.single_category_pcs_list[EntityType.VEHICLE.value].getColoredPointCloudDictByDetailedLabels(), attributes = PointAttributes.COLOR.value)

                    if EntityType.PEDESTRIAN.value in pc_sample1.pcFvData.single_category_pcs_list.keys():
                        # save the vehicles frontview pointcloud into a file 
                        pc_sample1.savePlyFileFromDict(configurations.pedestriansOnlyPointCloudFn, \
                            pc_sample1.pcData.single_category_pcs_list[EntityType.PEDESTRIAN.value].getColoredPointCloudDictByDetailedLabels(), attributes = PointAttributes.COLOR.value)

                if configurations.genCloudsWithoutBackground:
                    pointsList = pc_sample1.pcData.generatePointCloudWithoutBackground([EntityType.VEHICLE.value, EntityType.PEDESTRIAN.value])

                    pc_sample1.savePlyFile(configurations.noBackgroundPointsCloudFn, pointsList)
                
                else:
                    pc_sample1.savePlyFile(configurations.rotatedPointCloudFn, pc_sample1.pcData.list_rotated_raw_pc)

                #pc_sample1.savePlyFileFromDict("Pedestrians point cloud.ply", \
                #    pc_sample1.pcFvData.single_category_pcs_list[1].getColoredPointCloudDictByDetailedLabels(), attributes = 'c')

                kittiSample = KittiSampleManager(pc_sample1, rootKittiOutputDir, kittiSampleCounter, configurations)

                # kittiSample = KittiSampleManager(pc_sample1, rootKittiOutputDir, 7481, configurations)

                if not kittiSample.isEmpty:
                    kittiSampleCounter += 1
                else:
                    f = open("deleteFolders.txt", "a")
                    f.write(str(toSave) + " ")
                    f.close()
            except KeyboardInterrupt:
                sys.exit("KeyboardInterrupt")
            except Exception as e:
                print("Error occured")
                print(e)
                f = open("deleteFolders.txt", "a")
                f.write(str(toSave) + " ")
                f.close()

            # except ValueError:
            #     print("Value Error")

            toSave += 1
            f = open("GTASample.txt", "w")
            f.write(str(toSave))
            f.close()

            if(kittiSampleCounter == 7481):
                print("Now testing with " + str(kittiTrainSampleCounter) + " samples on the training set")

            #kittiSample1 = KittiSample(pc_sample1, rootKittiOutputDir, configurations.kittiLabelsDir, configurations.kittiVelodyneDir, configurations.kittiViewsDir, configurations.kittiCalibDir, sampleCounter)

            #pc_sample1.outputKittiLabelFile(sampleCounter)

            # show kitti dataset resolution front view with the calculated 2d bounding boxes
            #pc_sample1.imageView.show_image_view_with_2d_bounding_boxes(pc_sample1.imageView.dict_2d_bb_of_kitti_image, pc_sample1.imageView.kitti_image, pc_sample1.pc_fv_raw_data.single_category_pcs_list[2].object_ids_list, window_size = 1)

            #input()

    return

if __name__=='__main__':
    allowExecution = True

    parser = argparse.ArgumentParser(description='Convert GTA dataset to the Kitti dataset format.')
    # required options
    parser.add_argument('--gtaSamplesPath', type=str, help='Path to where the GTA samples are present.')
    parser.add_argument('--kittiOutputPath', type=str, help='Destination directory path to the kitti formatted dataset.')
    parser.add_argument('--targetArchitecure', type=str, help='Specify the target architeture for which to produce the formatted dataset.')   

    # optional options
    #group = parser.add_mutually_exclusive_group()
    parser.add_argument('--useNoise', action='store_true', help='Use the pointcloud with noise for the dataset.')    # default is false, and with this included as an option becaomes true
    parser.add_argument('--addIntensity', type=float, help='Add intensity value to each point of the pointclouds. Float value between 0 and 1.') 
    parser.add_argument('--filterByDistance', type=float, help='Ignore all samples that are have entities further away from the specified distance to lidar.')    
    parser.add_argument('--genSingle', action='store_true', help='Generate an additional directory with pointclouds contain individual entities obtained from the dataset. The entities wil be centered in the origin and the points normalized into a unit sphere.')    
    parser.add_argument('--noBackground', action='store_true', help='Generate an additional directory and store binary pointclouds without background points.')
    parser.add_argument('--ignoreEntities', type=int, help='Select entities to ignore: \n\t- 1: vehicles \n\t- 2: pedestrians')   
    parser.add_argument('--gtaFov', type=int, help='Fov used in GTA mod')   
    args = parser.parse_args()

    print("useNoise: " + str(args.useNoise))
    print("addIntensity: " + str(args.addIntensity))
    print("filterByDistance: " + str(args.filterByDistance))
    print("genSingle: " + str(args.genSingle))
    print("noBackground: " + str(args.noBackground))
    print("ignoreEntities: " + str(args.ignoreEntities))
    if args.gtaSamplesPath and args.kittiOutputPath and args.targetArchitecure:
        configurations = ConfigParams()
        configurations.useNoise = args.useNoise
        configurations.genSingleEntities = args.genSingle
        configurations.genCloudsWithoutBackground = args.noBackground
        configurations.targetArchitecture = args.targetArchitecure
        if args.gtaFov is not None:
            configurations.fov = args.gtaFov
        
        if args.addIntensity is not None:
            configurations.includeIntensity = (True, args.addIntensity)

        if args.filterByDistance is not None:
            configurations.filterByDistance = (True, args.filterByDistance)

        if args.ignoreEntities is None:
            configurations.ignoreVehicles = False
            configurations.ignorePedestrians = False
        else:
            if args.ignoreEntities == 1:
                configurations.ignoreVehicles = True
                configurations.ignorePedestrians = False
            elif args.ignoreEntities == 2:
                configurations.ignoreVehicles = False
                configurations.ignorePedestrians = True
            else:
                print("The --ignoreEntities can only hold two possible values {1, 2}")
                allowExecution = False

        compute(args.gtaSamplesPath + '/', args.kittiOutputPath + '/', configurations)
    else:
        print("The options --gtaSamplesPath, --kittiOutputPath and --targetArchitecure are required to run the program.")