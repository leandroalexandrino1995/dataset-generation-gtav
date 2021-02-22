from pathlib import Path
import numpy as np
import os.path
import math
import struct
import sys
sys.path.insert(0, '../GtaSample')
import GtaSample
import pointcloud_utils
import kitti_util
import UiConfigParams

class Labeling:
    '''
    (1 value) label_name: 'Car', 'Van', 'Truck', 'Pedestrian', 'Person_sitting', 'Cyclist', 'Tram', 'Misc' (qq outro tipo de vehiculo) or 'DontCare' (quando se pertende ignorar um veiculo)
    (1 value) trucanted: [0, 1], evaluates how much an object  isn't within the image boundaries
    (1 value) occluded: {0, 1, 2, 3}, fully-visible, partly occluded, largely-occuled, unknown
    (1 value) alpha: [-pi, pi], observation angle of the object
    (4 values) bbox: {left, top, right, bottom}, 2d bounding box of the object in the image
    (3 values) dimensions: {height, width, length}, 3d object dimensions in meters
    (3 values) location: {x, y, z}, 3d object location in camera coordinates in meters
    (1 value) rotation_y: [-pi, pi], rotation around Y-axis (up axis) in camera coordinates
    '''

    def __init__(self, gtaSample, calibObject, dirname, filename, configurations, fv_only_entities=True):
        '''
        fv_only_entities = true => ignore all entites that are not in the front view image

        Values per vehicle: [Entity] 
        | Hash 
        | minCornerX | minCornerY | minCornerZ | projMinCornerX | projMinCornerX 
        | maxCornerX | maxCornerY | maxCornerZ | projMaxCornerX | projMaxCornerY 
        | Posx | Posy | Posz | Rotx | Roty | Rotz 
        | projCenterX | projCenterY 
        | dimX | dimY | dimZ
        | objectType | truncated"
        '''
        self.isEmpty = False

        # entityInfoDict
        entityInfoDict = gtaSample.loadTxtFileToDict(configurations.entityInfoFn)

        # will contain all lines of a label.txt file (of a sample)
        contents_list = []

        # iterate through all entities in the label file
        for key in entityInfoDict.keys():

            if configurations.ignoreVehicles and entityInfoDict[key][22] == UiConfigParams.KittiTypes.CAR.value:
                continue
            if configurations.ignorePedestrians and entityInfoDict[key][22] == UiConfigParams.KittiTypes.PEDESTRIAN.value:
                continue
            
            label_line = ""

            kitti_height, kitti_width, channels = gtaSample.imageView.getKittiImageDimensions()
            print("height: " + str(kitti_height))
            print("width: " + str(kitti_width))

            # calculate base center position of the entity object, which is used by the kitti dataset to localize objects
            entityBaseCenterPos = (float(entityInfoDict[key][11]), float(entityInfoDict[key][12]), float(entityInfoDict[key][13]) - float(entityInfoDict[key][21])/2)
            lidarPos = (0, 0, 0)
            # checkif distance of the entity to the vehicle is less than what is specified in the configurations
            if configurations.filterByDistance[0]:
                print("Distance: " + str(pointcloud_utils.calcDistanceBetween3dPoints(lidarPos, entityBaseCenterPos)))
                if pointcloud_utils.calcDistanceBetween3dPoints(lidarPos, entityBaseCenterPos) > configurations.filterByDistance[1]:
                    # ignore entity
                    continue

            print("entityBaseCenterPos", str(entityBaseCenterPos))

            # due to the point cloud is aditionally transformed to be pointing in the direction of x axis instead of the y axis
            orientedEntityPos = gtaSample.pcData.rotatePointAroundZaxis(entityBaseCenterPos, gtaSample.pcData.rotation_amount)

            # rotate pointcloud to orient it towards the x axis, as in the kitti dataset
            orientedEntityPos = gtaSample.pcData.rotatePointAroundZaxis(orientedEntityPos, pointcloud_utils.degreesToRad(90))
            orientedEntityPos = gtaSample.pcData.rotatePointAroundXaxis(orientedEntityPos, pointcloud_utils.degreesToRad(90))
            #orientedEntityPos = self.orientEntityPointTowardsXaxis(gtaSample, orientedEntityPos)
            #orientedEntityPos = self.rotation_entityposFromVeloToCam(gtaSample, orientedEntityPos, 90)

            # height (dimz), width (dimx), length (dimy)
            bb3d_height = float(entityInfoDict[key][21])
            bb3d_width = float(entityInfoDict[key][19])
            bb3d_length = float(entityInfoDict[key][20])
            
            obj_rot_rads = self.calcEntityRotation(gtaSample, entityInfoDict[key])

            # Calculate 2D and 3D bounding boxes
            box3d_pts_2d, box3d_pts_3d = kitti_util.compute_box_3d(bb3d_length, bb3d_width, bb3d_height, obj_rot_rads, orientedEntityPos, calibObject.p0_mat, calibObject.R0, calibObject.C2V)

            xmin, ymin, xmax, ymax = self.calc2DboundingboxCorners(box3d_pts_2d)

            if not self.validateEntityWith2Dboundingbox(xmin, ymin, xmax, ymax, kitti_width, kitti_height):
                # ignore entity
                continue

            # object type: car
            label_line += entityInfoDict[key][22] + " "
            
            # truncated
            label_line += "0 "

            # occluded
            label_line += "0 "

            # alpha
            label_line += "0 "

            # minx, miny, maxx, maxy
            label_line += str(int(xmin)) + " " + str(int(ymin)) + " " + str(int(xmax)) + " " + str(int(ymax)) + " "

            label_line += str(bb3d_height) + " " + str(bb3d_width) + " " + str(bb3d_length) + " "
            
            label_line += str(orientedEntityPos[0]) + " " + str(orientedEntityPos[1]) + " " + str(orientedEntityPos[2]) + " "

            label_line += str(obj_rot_rads) + " "

            contents_list.append(label_line)

        # if list not empty
        if contents_list:          
            gtaSample.saveListIntoTxtFile(contents_list, dirname, filename)
        else:
            self.isEmpty = True

            

    def orientEntityPointTowardsXaxis(self, gtaSample, position):
        return gtaSample.pcData.rotatePointAroundZaxis(position, gtaSample.pcData.rotation_amount)

    def translation_entityposToCam(self, entityPos, camPos):
        '''
        Arguments:
            - entityPos: np array of floats
            - camPos: np array of floats
        Returns:
            - transform vehicle position | np array of floats
        '''
        vecCamToObj = entityPos - camPos
        return vecCamToObj.dot(vecCamToObj)

    def rotation_entityposFromVeloToCam(self, gtaSample, position, angle):
        '''
        Arguments:
            - gtaSample: GtaSample instance
            - entityPos: position of the objeto to be transformed from velodyne to camera coordinate system
            - angle: rotation angle, in degrees, related to the transformation (the camera and lidar have the same position)
        Returns:
            - (x, y, z) | float tuple
        '''
        pos = gtaSample.pcData.rotatePointAroundZaxis(position, pointcloud_utils.degreesToRad(angle))
        pos = gtaSample.pcData.rotatePointAroundXaxis(pos, pointcloud_utils.degreesToRad(angle))
        return pos

    def calcEntityRotation(self, gtaSample, vehicleInfo):
        obj_rot_rads = 0
        if float(vehicleInfo[24]) < 0 and float(vehicleInfo[25]) < 0: #DONE
            obj_rot_rads = float(vehicleInfo[16]) + gtaSample.rawCamRotation + 90
        elif float(vehicleInfo[24]) < 0 and float(vehicleInfo[25]) > 0: #DONE
            obj_rot_rads = -float(vehicleInfo[16]) + gtaSample.rawCamRotation - 90
        elif float(vehicleInfo[24]) > 0 and float(vehicleInfo[25]) > 0: # almost
            if float(vehicleInfo[26]) < 0:
                obj_rot_rads = -float(vehicleInfo[16]) + gtaSample.rawCamRotation - 90
            else:
                obj_rot_rads = -float(vehicleInfo[16]) + gtaSample.rawCamRotation - 90
        elif float(vehicleInfo[24]) > 0 and float(vehicleInfo[25]) < 0:
            if float(vehicleInfo[26]) < 0:
                obj_rot_rads = float(vehicleInfo[16]) + gtaSample.rawCamRotation - 90 + 180
            else:
                obj_rot_rads = float(vehicleInfo[16]) + gtaSample.rawCamRotation - 90 - 180

        print("Vehicle Rotation Final: " + str(obj_rot_rads))

        obj_rot_rads = pointcloud_utils.degreesToRad(obj_rot_rads)

        # make sure the ry is between [-pi, pi]
        if obj_rot_rads > math.pi:
            obj_rot_rads = -(math.pi + (math.pi - obj_rot_rads)) 
        elif obj_rot_rads < -math.pi:
            obj_rot_rads = math.pi + (math.pi + obj_rot_rads)

        return obj_rot_rads
    
    def calc2DboundingboxCorners(self, box3d_pts_2d):
        xmin = 0
        ymin = 0
        xmax = 0
        ymax = 0
        print(len(box3d_pts_2d))
        print("POINTS HERE")
        print(box3d_pts_2d)
        for i in range(0, len(box3d_pts_2d)):
            if i == 0:
                xmin = box3d_pts_2d[i,0]
                ymin = box3d_pts_2d[i,1]
                xmax = box3d_pts_2d[i,0]
                ymax = box3d_pts_2d[i,1]
            else:
                if box3d_pts_2d[i,0] < xmin:
                    xmin = box3d_pts_2d[i,0]
                elif box3d_pts_2d[i,0] > xmax:
                    xmax = box3d_pts_2d[i,0]
                
                if box3d_pts_2d[i,1] < ymin:
                    ymin = box3d_pts_2d[i,1]
                elif box3d_pts_2d[i,1] > ymax:
                    ymax = box3d_pts_2d[i,1]
        
        return xmin, ymin, xmax, ymax

    def validateEntityWith2Dboundingbox(self, xmin, ymin, xmax, ymax, img_width, img_height):
        print("xmin: " + str(xmin))
        print("xmax: " + str(xmax))
        print("ymin: " + str(ymin))
        print("ymax: " + str(ymax))

        if xmin < 0:
            if xmax < 0:
                return False
        if xmin >= img_width:
            if xmax >= img_width:
                return False
        
        if ymin < 0:
            if ymax < 0:
                return False 
        if ymin >= img_height:
            if ymax >= img_height:
                return False

        return True