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
from collections import namedtuple


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
        self.isEmpty = True

        # entityInfoDict
        entityInfoDict = gtaSample.loadTxtFileToDict(configurations.entityInfoFn)

        # will contain all lines of a label.txt file (of a sample)
        contents_list = []

        distances = {}
        left = []
        right = []
        top = []
        bottom = []

        # iterate through all entities in the label file
        for key in entityInfoDict.keys():

            if configurations.ignoreVehicles and entityInfoDict[key][22] == UiConfigParams.KittiTypes.CAR.value:
                continue
            if configurations.ignorePedestrians and entityInfoDict[key][22] == UiConfigParams.KittiTypes.PEDESTRIAN.value:
                continue
##            if int(entityInfoDict[key][-4]) == 1:
##                continue
            
            label_line = ""

            kitti_height, kitti_width, channels = gtaSample.imageView.getKittiImageDimensions()
            # #print("height: " + str(kitti_height))
            # #print("width: " + str(kitti_width))

            # calculate base center position of the entity object, which is used by the kitti dataset to localize objects
            entityBaseCenterPos = (float(entityInfoDict[key][11]), float(entityInfoDict[key][12]), float(entityInfoDict[key][13]) - float(entityInfoDict[key][21])/2)
            lidarPos = (0, 0, 0)
            distance = pointcloud_utils.calcDistanceBetween3dPoints(lidarPos, entityBaseCenterPos)
            # checkif distance of the entity to the vehicle is less than what is specified in the configurations
            if configurations.filterByDistance[0]:
                # #print("Distance: " + str(distance))
                if distance > configurations.filterByDistance[1]:
                    # ignore entity
                    continue

            # #print("entityBaseCenterPos", str(entityBaseCenterPos))

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

            xmin_trunc = 0
            ymin_trunc = 0
            xmax_trunc = 0
            ymax_trunc = 0

            if(round(xmin,2) < 0.00 and abs(round(xmin,2)) > round(gtaSample.imageView.kittiImage.shape[1],2) and abs(round(xmax,2)) > round(gtaSample.imageView.kittiImage.shape[1],2)):
                xmin_trunc = round(gtaSample.imageView.kittiImage.shape[1],2)
            elif(round(xmin,2) < 0.00 and abs(round(xmin,2)) > round(gtaSample.imageView.kittiImage.shape[1],2)):
                xmin_trunc = xmax
            elif(round(xmin,2) < 0.00):
                xmin_trunc = 0.00
            else:
                xmin_trunc = xmin

            if(round(xmax,2) < round(gtaSample.imageView.kittiImage.shape[1],2) and abs(round(xmin,2)) > round(gtaSample.imageView.kittiImage.shape[1],2)):
                xmax_trunc = round(gtaSample.imageView.kittiImage.shape[1],2)
            elif(round(xmax,2) > round(gtaSample.imageView.kittiImage.shape[1],2)):
                xmax_trunc = round(gtaSample.imageView.kittiImage.shape[1],2)
            else:
                xmax_trunc = xmax

            if(round(ymin,2) < 0.00 and abs(round(ymin,2)) > round(gtaSample.imageView.kittiImage.shape[0],2) and abs(round(ymax,2)) > round(gtaSample.imageView.kittiImage.shape[0],2)):
                ymin_trunc = round(gtaSample.imageView.kittiImage.shape[0],2)
            elif(round(ymin,2) < 0.00 and abs(round(ymin,2)) > round(gtaSample.imageView.kittiImage.shape[0],2)):
                ymin_trunc = ymax
            elif(round(ymin,2) < 0.00):
                ymin_trunc = 0.00
            else:
                ymin_trunc = ymin

            if(round(ymax,2) < round(gtaSample.imageView.kittiImage.shape[0],2) and abs(round(ymin,2)) > round(gtaSample.imageView.kittiImage.shape[0],2)):
                ymax_trunc = round(gtaSample.imageView.kittiImage.shape[0],2)
            elif(round(ymax,2) > round(gtaSample.imageView.kittiImage.shape[0],2)):
                ymax_trunc = round(gtaSample.imageView.kittiImage.shape[0],2)
            else:
                ymax_trunc = ymax

            if (round(xmax,2) > round(gtaSample.imageView.kittiImage.shape[1],2) and round(xmin,2) < 0.00 and round(ymin,2) < 0.00 and round(ymax, 2) > round(gtaSample.imageView.kittiImage.shape[0],2)):
                xmax_trunc = xmin_trunc = ymax_trunc = ymin_trunc = 0.00

            

            # xmin_trunc = xmin if round(xmin,2) > 0.00 else 0.00
            # xmin_trunc = xmax if abs(round(xmin,2)) > round(gtaSample.imageView.kittiImage.shape[1],2) else xmin_trunc
            # xmin_trunc = round(gtaSample.imageView.kittiImage.shape[1],2) if abs(round(xmax,2)) > round(gtaSample.imageView.kittiImage.shape[1],2) else xmax

            # xmax_trunc = xmax if round(xmax,2) < round(gtaSample.imageView.kittiImage.shape[1],2) else (round(gtaSample.imageView.kittiImage.shape[1],2))
            # xmax_trunc = xmax_trunc if abs(round(xmin,2)) < round(gtaSample.imageView.kittiImage.shape[1],2) else (round(gtaSample.imageView.kittiImage.shape[1],2))
            
            # ymin_trunc = ymin if round(ymin,2) > 0.00 else 0.00
            # ymin_trunc = ymax if abs(round(ymin,2)) > round(gtaSample.imageView.kittiImage.shape[0],2) else ymin
            # ymin_trunc = round(gtaSample.imageView.kittiImage.shape[0],2) if abs(round(ymax,2)) > round(gtaSample.imageView.kittiImage.shape[0],2) else ymax

            # ymax_trunc = ymax if round(ymax,2) < (round(gtaSample.imageView.kittiImage.shape[0],2)) else (round(gtaSample.imageView.kittiImage.shape[0],2))
            # ymax_trunc = ymax_trunc if abs(round(ymin,2)) < round(gtaSample.imageView.kittiImage.shape[0],2) else (round(gtaSample.imageView.kittiImage.shape[0],2))

            # if (xmin < 0.00 and xmax < 0.00 or xmin > gtaSample.imageView.kittiImage.shape[1] and xmax > gtaSample.imageView.kittiImage.shape[1] or ymin < 0.00 and ymax < 0.00 or ymin > gtaSample.imageView.kittiImage.shape[0] and ymax > gtaSample.imageView.kittiImage.shape[0]):
            #     truncated = 1.00

            # else:
            truncated = round((((xmax_trunc-xmin_trunc)*(ymax_trunc-ymin_trunc))/((xmax-xmin)*(ymax-ymin))),2)
            truncated -= 1
            truncated = round(abs(truncated),2)

            if not self.validateEntityWith2Dboundingbox(xmin, ymin, xmax, ymax, kitti_width, kitti_height):
                # print("entrou aqui")
                # ignore entity
                continue

            if self.isEmpty and entityInfoDict[key][22] != "DontCare" and truncated <= 0.50 and abs(ymax_trunc - ymin_trunc) >= 25:
                self.isEmpty = False

            DontCare = 0

            if entityInfoDict[key][22] != "DontCare" and (truncated > 0.50 or abs(ymax_trunc - ymin_trunc) < 25):
                DontCare = 1

            # object type: car
            if DontCare == 1:
                label_line += "DontCare "
            elif entityInfoDict[key][22] == "DontCare":
                label_line += "Ignore "
            else:
                label_line += entityInfoDict[key][22] + " "

            # truncated
            if (entityInfoDict[key][22] == "DontCare") or DontCare == 1:
                label_line += "-1 "
            else:
                label_line += str(round(truncated,2)) + " "
                    

            # occluded
            if (entityInfoDict[key][22] == "DontCare") or DontCare == 1:
                label_line += "-1 "
            else:
                label_line += "0.00 "

            # alpha
            if (entityInfoDict[key][22] == "DontCare") or DontCare == 1:
                label_line += "-10 "
            else:
                label_line += "0.00 "

            label_line += str(round(xmin_trunc,2)) + " " + str(round(ymin_trunc,2)) + " " + str(round(xmax_trunc,2)) + " " + str(round(ymax_trunc,2)) + " "

            if (entityInfoDict[key][22] == "DontCare") or DontCare == 1:
                label_line += "-1 -1 -1 "
            else:
                label_line += str(bb3d_height) + " " + str(bb3d_width) + " " + str(bb3d_length) + " "
            
            if (entityInfoDict[key][22] == "DontCare") or DontCare == 1:
                label_line += "-1000 -1000 -1000 "
            else:
                label_line += str(orientedEntityPos[0]) + " " + str(orientedEntityPos[1]) + " " + str(orientedEntityPos[2]) + " "

            if (entityInfoDict[key][22] == "DontCare") or DontCare == 1:
                label_line += "-10 "
            else:
                label_line += str(obj_rot_rads) + " "

            # distances[distance] = len(contents_list)535068240231888

            distances[(len(contents_list))] = distance

            left.append(xmin_trunc)
            top.append(ymin_trunc)
            right.append(xmax_trunc)
            bottom.append(ymax_trunc)

            # left.append(xmin)
            # top.append(ymin)
            # right.append(xmax)
            # bottom.append(ymax)

            contents_list.append(label_line)

        distances = dict(sorted(distances.items(), key=lambda item: item[1]))

        # #print("distances: ")
        # #print(distances)


        test = []

        to_print = []

        for x in distances.keys():
            if(len(test) == 0):
                test.append(contents_list[x])
                line = contents_list[x]
                split = line.split(" ")
                if((split[0] != "Ignore")):
                    to_print.append(line)
            else:
                # #print("AQUI!!!!")
                #print(intersection)
                # if (entityInfoDict[key][22] == "DontCare"):
                #     intersection = -1
                # else:
                intersection = self.calculateIntesection(left, top, right, bottom, distances.keys(), len(test)+1)
                if(int(intersection) == 100 or intersection < 0.00):
                    intersection = 3.00
                elif(0.00 < intersection < 30.00 ):
                    intersection = 1.00
                elif(intersection >= 30.00):
                    intersection = 2.00
                line = contents_list[x]
                split = line.split(" ")
                # print(split)
                line_to_append = ""
                if (split[0] == "DontCare"):
                    test.append(line)
                    to_print.append(line)
                elif (split[0] == "Ignore"):
                    test.append(line)
                else:
                    for k in range(len(split)):
                        if k != 2:
                            line_to_append += split[k] + " "
                        else:
                            line_to_append += str(intersection) + " "
                    test.append(line_to_append)
                    to_print.append(line_to_append)

        # print(to_print)

        # # if list not empty
        # if contents_list:          
        #     gtaSample.saveListIntoTxtFile(contents_list, dirname, filename)
        # else:
        #     self.isEmpty = True

            
        # if list not empty
        # if test:          
        #     gtaSample.saveListIntoTxtFile(test, dirname, filename)
        # else:
        #     self.isEmpty = True

        if not self.isEmpty:          
            gtaSample.saveListIntoTxtFile(to_print, dirname, filename)
        

    def calculateIntesection(self, left, top, right, bottom, keys, xs):

        left_sorted = []
        top_sorted = []
        right_sorted = []
        bottom_sorted = []

        keys = list(keys)
        keys = keys[:xs]
        for x in keys:
            left_sorted.append(left[x])
            top_sorted.append(top[x])
            right_sorted.append(right[x])
            bottom_sorted.append(bottom[x])

        # #print("Left sorted")
        # #print(left_sorted)

        # #print("Top sorted")
        # #print(top_sorted)

        # #print("Right sorted")
        # #print(right_sorted)

        # #print("Bottom sorted")
        # #print(bottom_sorted)

        my_left = left_sorted[-1]
        my_top = top_sorted[-1]
        my_right = right_sorted[-1]
        my_bottom = bottom_sorted[-1]

        # rects = [[0] * len(keys)] * len(keys)

        overlapWithMyArea = []

        Rectangle = namedtuple('Rectangle', 'xmin ymin xmax ymax')
        my_area = Rectangle(my_left, my_top, my_right, my_bottom)
        # #print("My area 1")
        # #print(my_area)
        for l,t,r,b in zip(left_sorted[:-1], top_sorted[:-1], right_sorted[:-1], bottom_sorted[:-1]):
            rect = Rectangle(l, t, r, b)
            try:
                aux_l, aux_t, aux_r, aux_b = self.overlapCorners(rect, my_area)
                overlapWithMyArea.append([aux_l, aux_t, aux_r, aux_b])
            except TypeError: 
                continue

        if (len(overlapWithMyArea) == 0):
            return 0.00

        # #print(len(overlapWithMyArea))

        overlappingArea = 0

        # #print("My area")
        # #print(my_area)
        for x in overlapWithMyArea[:-1]:
            # #print("HELLO")
            # # if len(overlapWithMyArea) > 1:
            # #print("XXXXX")
            # #print(x)
            big_area = Rectangle(x[0], x[1], x[2], x[3])
            for y in overlapWithMyArea[1:]:
                try:
                    rect = Rectangle(y[0], y[1], y[2], y[3])
                    aux_l, aux_t, aux_r, aux_b = self.overlapCorners(big_area, rect)
                    return -1
                    # overlapWithMyArea.append([aux_l, aux_t, aux_r, aux_b])
                except TypeError: 
                    continue
            overlappingArea += (self.area(my_area, big_area)/self.area(my_area, my_area))*100

            # else:
        if len(overlapWithMyArea) == 1:
            x = overlapWithMyArea[0]
            # with overlapWithMyArea[0] as x:
            # #print("YYYYYYY")
            big_area = Rectangle(x[0], x[1], x[2], x[3])
            # #print("Big area")
            # #print(big_area)
            # #print(self.area(my_area, big_area))
            try:
                return (self.area(my_area, big_area)/self.area(my_area, my_area))*100
            except ZeroDivisionError:
                return -1

        x = overlapWithMyArea[-1]
        big_area = Rectangle(x[0], x[1], x[2], x[3])

        try:
            overlappingArea += (self.area(my_area, big_area)/self.area(my_area, my_area))*100 ##grelada aqui por algum motivo
            return overlappingArea
        except ZeroDivisionError:
            return -1

    def area(self, a, b):  # returns None if rectangles don't intersect
        dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
        dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
        # #print("dx "+str(dx))
        # #print("dy "+str(dy))
        if (dx>0) and (dy>0):
            return dx*dy
        return 0.00

    def overlapCorners(self, a, b):  # returns None if rectangles don't intersect
        left = max(a.xmin, b.xmin)
        top = max(a.ymin, b.ymin)
        right = min(a.xmax, b.xmax)
        bottom = min(a.ymax, b.ymax)
        dx = right - left
        dy = bottom - top
        if (dx>=0) and (dy>=0):
            return left, top, right, bottom
        # return -1, -1, -1, -1

        # dx = min(a.xmax, b.xmax) - max(a.xmin, b.xmin)
        # dy = min(a.ymax, b.ymax) - max(a.ymin, b.ymin)
        # if (dx>=0) and (dy>=0):
        #     return dx + max(a.xmin, b.xmin)
        # return dx + max(a.xmin, b.xmin)

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

        # #print("Vehicle Rotation Final: " + str(obj_rot_rads))

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
        # #print(len(box3d_pts_2d))
        # #print("POINTS HERE")
        # #print(box3d_pts_2d)
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
        # #print("xmin: " + str(xmin))
        # #print("xmax: " + str(xmax))
        # #print("ymin: " + str(ymin))
        # #print("ymax: " + str(ymax))

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
