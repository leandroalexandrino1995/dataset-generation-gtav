import os
# from GtaSample import GtaSample

#from KittiSample import KittiSample
# from LoadBinPointclouds import loadKittiVelodyneFile
# from LoadBinPointclouds import savePlyFile
import argparse
from dataclasses import dataclass
# from UiConfigParams import ConfigParams, EntityType, PointAttributes
# from KittiSampleManager import KittiSampleManager

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

def loadTxtFileToDict(directory_path, filename):
    '''
    The first value in each line becomes the key and the rest the value
    Returns a dictionary list values
    '''
    dict = {}
    with open(os.path.join(directory_path, filename)) as file_in:
        for line in file_in:
            list = []
            line_list = line.rstrip().split(' ')
            # print(line_list) # <- tirei aqui
            key = line_list[0]
            
            for i in range(1, len(line_list)):
                list.append(line_list[i])
            
            dict[key] = list

    return dict

def saveListIntoTxtFile(list_of_str, dirname, filename):
        '''
        Store list of strings into a file
        '''
        with open(os.path.join(dirname, filename), "w") as the_file:
            for i in range(0, len(list_of_str)):
                the_file.write(list_of_str[i] + "\n")


# def compute(rootDir, rootKittiOutputDir, configurations):
def compute(rootDir, reset):
    
    # to generate the naming sequence for the kitti samples
    gtaSampleCounter = len(os.listdir(rootDir))

    # try:
    #     kittiTrainSampleCounter = len(os.listdir(rootKittiOutputDir+ConfigParams.kittiLabelsDir))
    # except FileNotFoundError:
    #     kittiTrainSampleCounter = 0
    
    # try:
    #     kittiTestSampleCounter = len(os.listdir(rootKittiOutputDir+ConfigParams.kittiVelodyneDirTesting))
    # except FileNotFoundError:
    #     kittiTestSampleCounter = 0

    # kittiSampleCounter = kittiTrainSampleCounter + kittiTestSampleCounter

    # print(len(os.listdir(rootKittiOutputDir+"/data_object_label_2/training/label_2")))


    if not reset:
        try:
            f = open("ToCorrect.txt", "r")
            GTAFolder = int(f.read())
            ToCorrect = GTAFolder
            f.close()
        except FileNotFoundError:
            f = open("ToCorrect.txt", "w")
            f.write('0')
            f.close()

            f = open("ToCorrect.txt", "r")
            GTAFolder = int(f.read())
            ToCorrect = GTAFolder
            f.close()

    else:
        f = open("ToCorrect.txt", "w")
        f.write('0')
        f.close()

        f = open("ToCorrect.txt", "r")
        GTAFolder = int(f.read())
        ToCorrect = GTAFolder
        f.close()

    # print("Current number of samples in " + rootKittiOutputDir + ": " + str(kittiSampleCounter))
    # print("Current number of training samples: " + str(kittiTrainSampleCounter))
    # print("Current number of testing samples: " + str(kittiTestSampleCounter))
    print("Number of GTA samples: " + str(gtaSampleCounter))

    print("Corrected: " + str(ToCorrect))

    print("Reset: " + str(reset))

    # GTAFolder = int(GTAFolder.replace('LiDAR_PointCloud',''))
    # print(GTAFolder)

    filename_debug = 'LiDAR_PointCloud_logSampleDebug.txt'
    filename = 'LiDAR_PointCloud_vehicles_dims.txt'

    ignore_object = 1

    good_objects = []

    # walk through all samples in rootDir and create the kitti output accordingly
    for subdir, dirs, files in os.walk(rootDir):
        # preserve the order of the original point clouds
        dirs = sorted(dirs, key=lambda filename: int(filename.replace('LiDAR_PointCloud','')))
        for dirName in dirs[GTAFolder:]:

            good_objects = []

            print('\n\n::::::: Current sample directory: ' + dirName + ' :::::::')
            
            directory_path = rootDir + dirName

            try:
                
                # entityInfoDict = loadTxtFileToDict(directory_path, filename_debug)
                
                # print(entityInfoDict)

                with open(os.path.join(directory_path, filename_debug), encoding='ISO-8859–1') as file_in:
                    lines = file_in.readlines()
                    # print(len("Entity: "))
                    # print(lines)
                    for aux in range(len(lines)):
                        if ("Entity: " in lines[aux]):
                            object = lines[aux].replace("Entity: ", "")
                            object = object.replace("\n","")
                            # print(object)
                        if("Vehicle projected corners coordinates:" in lines[aux]):
                            for line in lines[aux+1:aux+9]:
                                if("-1920, -1080" not in line):
                                    # print("Very Nice!")
                                    good_objects.append(object)
                                    break

                # print(good_objects)

                entityInfoDict = loadTxtFileToDict(directory_path, filename)
                
                newValue = []

                for key, value in entityInfoDict.items():
                    if key in good_objects:
                        newValue = value[:-4] + ['0'] + value[-3:]
                        # newValue.append(value[:-4] + '0' + value[-3:])
                        # print((value[:-4] + ['0'] + value[-3:]))
                        # newValue.append('0')
                        # newValue.append(value[-3:])
                        # print(newValue)
                        entityInfoDict[key] = newValue
                
                # print(entityInfoDict[key])



                with open(os.path.join(directory_path, filename),'w') as file_in:
                    for key in entityInfoDict.keys():
                        file_in.write(key)
                        for i in entityInfoDict[key]:
                            file_in.write(" " + i)
                            # print(i)
                        file_in.write("\n")
                        # print(str(key) + " " + str(entityInfoDict[key]))

                # saveListIntoTxtFile()

                # for object in good_objects:
                #     entityInfoDict.get(object)
                #     print(entityInfoDict.get(object))
                
                

                            
                    # .split("Entity")[1:]
                    # print(lines[0].split("\n")[0].replace(": ", ""))
                    # for i in lines:
                    #     print(i)
                    #     info = i.split("[ GetBestMinMaxCoords() ]")[0] 
                    #     corners = info.split("Vehicle projected corners coordinates:")[-1]
                    #     corners = corners.replace("]: ", "@")
                    #     corners = corners.split("@")
                    #     if(len(corners) > 1):
                    #         corners = corners[1:]
                    #         for corner in corners:
                    #             aux = corner.split("\n")[0]
                    #             if(aux != "-1920, -1080"):
                    #                 ignore_object = 0
                    #                 print("Very Nice")
                    #                 break
                        # for x in info:
                        #     print(x)
                            # print(x.split("Vehicle projected corners coordinates:")[1])
                        # print(i)

                # # load sample (point cloud + front view image) and create the original pointcloud, a rotated point cloud, a front view point cloud, the kitti dataset resolution image
                # pc_sample1 = GtaSample(rootDir + dirName, configurations)   
                
                # # save the original point cloud (not rotated) into a file
                # #pc_sample1.savePlyFile('Original point cloud.ply', pc_sample1.pcData.list_raw_pc)
                
                # # pc_sample1.savePlyFile(configurations.rotatedPointCloudFn, pc_sample1.pcData.list_rotated_raw_pc)
                
                # # pc_sample1.savePlyFile(configurations.frontviewPointCloudFn, pc_sample1.pcFvData.list_rotated_raw_pc)
                
                # # create a point cloud only with points with label = 2, vehicles
                # #pc_sample1.pcFvData. \
                # #    generateSingleCategoryPointCloud(2, category_name="vehicles", debug_mode=False)

                # pc_sample1.pcData. \
                #     generateSingleCategoryPointCloud(EntityType.VEHICLE.value, category_name="vehicles", debug_mode=False)
                
                # pc_sample1.pcData. \
                #     generateSingleCategoryPointCloud(EntityType.PEDESTRIAN.value, category_name='pedestrians', debug_mode=False)
                
                # # if no vehicle points were detected in the front view point cloud, pass to the next sample
                
                # # ignore sample if it does not contain any of the desired entity types 
                # # if not EntityType.VEHICLE.value in pc_sample1.pcFvData.single_category_pcs_list.keys() \
                # #     and not EntityType.PEDESTRIAN.value in pc_sample1.pcFvData.single_category_pcs_list.keys():
                # #     continue

                # if configurations.genSingleEntities:
                #     if EntityType.VEHICLE.value in pc_sample1.pcFvData.single_category_pcs_list.keys():
                #         # save the vehicles frontview pointcloud into a file 
                #         pc_sample1.savePlyFileFromDict(configurations.vehiclesOnlyPointCloudFn, \
                #             pc_sample1.pcData.single_category_pcs_list[EntityType.VEHICLE.value].getColoredPointCloudDictByDetailedLabels(), attributes = PointAttributes.COLOR.value)

                #     if EntityType.PEDESTRIAN.value in pc_sample1.pcFvData.single_category_pcs_list.keys():
                #         # save the vehicles frontview pointcloud into a file 
                #         pc_sample1.savePlyFileFromDict(configurations.pedestriansOnlyPointCloudFn, \
                #             pc_sample1.pcData.single_category_pcs_list[EntityType.PEDESTRIAN.value].getColoredPointCloudDictByDetailedLabels(), attributes = PointAttributes.COLOR.value)

                # if configurations.genCloudsWithoutBackground:
                #     pointsList = pc_sample1.pcData.generatePointCloudWithoutBackground([EntityType.VEHICLE.value, EntityType.PEDESTRIAN.value])

                #     # pc_sample1.savePlyFile(configurations.noBackgroundPointsCloudFn, pointsList)

                #     pc_sample1.savePlyFile(configurations.rotatedPointCloudFn, pointsList)
                
                # else:
                #     pc_sample1.savePlyFile(configurations.rotatedPointCloudFn, pc_sample1.pcData.list_rotated_raw_pc)

                # #pc_sample1.savePlyFileFromDict("Pedestrians point cloud.ply", \
                # #    pc_sample1.pcFvData.single_category_pcs_list[1].getColoredPointCloudDictByDetailedLabels(), attributes = 'c')

                # kittiSample = KittiSampleManager(pc_sample1, rootKittiOutputDir, kittiSampleCounter, configurations)

                # # kittiSample = KittiSampleManager(pc_sample1, rootKittiOutputDir, 7481, configurations)

                # if not kittiSample.isEmpty:
                #     kittiSampleCounter += 1
            except KeyboardInterrupt:
                sys.exit("KeyboardInterrupt")
            except Exception as e:
                print("Error occured")
                print(e)

            # except ValueError:
            #     print("Value Error")

            # return

            ToCorrect += 1
            f = open("ToCorrect.txt", "w")
            f.write(str(ToCorrect))
            f.close()

            # if(kittiSampleCounter == 7481):
            #     print("Now testing with " + str(kittiTrainSampleCounter) + " samples on the training set")

            #kittiSample1 = KittiSample(pc_sample1, rootKittiOutputDir, configurations.kittiLabelsDir, configurations.kittiVelodyneDir, configurations.kittiViewsDir, configurations.kittiCalibDir, sampleCounter)

            #pc_sample1.outputKittiLabelFile(sampleCounter)

            # show kitti dataset resolution front view with the calculated 2d bounding boxes
            #pc_sample1.imageView.show_image_view_with_2d_bounding_boxes(pc_sample1.imageView.dict_2d_bb_of_kitti_image, pc_sample1.imageView.kitti_image, pc_sample1.pc_fv_raw_data.single_category_pcs_list[2].object_ids_list, window_size = 1)

            #input()

if __name__=='__main__':
    allowExecution = True

    parser = argparse.ArgumentParser(description='Convert GTA dataset to the Kitti dataset format.')
    # required options
    parser.add_argument('--gtaSamplesPath', type=str, help='Path to where the GTA samples are present.')
    parser.add_argument('--reset', action="store_true")

    # optional options
    args = parser.parse_args()

    if args.gtaSamplesPath is not None:
        compute(args.gtaSamplesPath + '/', args.reset)

    else:
        print("The option --gtaSamplesPath is required to run the program.")