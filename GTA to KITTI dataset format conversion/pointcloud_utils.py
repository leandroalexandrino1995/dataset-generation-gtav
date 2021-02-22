from pathlib import Path
import numpy as np
import os.path
import math
import struct
import math

def loadKittiVelodyneFile(file_path, include_luminance = False):
    '''
    Loads a kitti velodyne file (ex: 000000.bin) into a list of tuples, where each tuple has (x, y, z) or (x, y, z, l)
    Right now it discards the 4th vaule of each point, i.e. the luminance
    Argument:
        - include_luminance: if the function should also store the pont intensisty value in the list of points
    '''
    # Source: https://github.com/hunse/kitti/blob/master/kitti/velodyne.py
    points = np.fromfile(file_path, dtype=np.float32).reshape(-1, 4)
    points = points[:, :3]  # exclude luminance

    point_tuple_list = []
    for i in range(len(points)):
        point_tuple_list.append((points[i][0], points[i][1], points[i][2],))

    return point_tuple_list


def loadGtaVelodyneBinFile(file_path, include_luminance = False):
    '''
    Loads a kitti velodyne file (ex: 000000.bin) into a list of tuples, where each tuple has (x, y, z) or (x, y, z, l)
    Argument:
        - include_luminance: if the function should also store the pont intensisty value in the list of points
    '''
    f = open(file_path, mode='rb')
    dt=np.dtype('float,float,float')
    numpyList = np.fromfile(f, dt)

    point_tuple_list = []
    for i in range(len(numpyList)):
        point_tuple_list.append((numpyList[i][0], numpyList[i][1], numpyList[i][2],))

    return point_tuple_list


def saveKittiVelodyneFile(tuple_list, filename, directory):
    '''
    Saves pointcloud in binary file and is independent of the number of properties in the pointcloud points
    '''
    with open(directory + filename, "wb") as f:
        for point in tuple_list:
            s = struct.pack('f'*len(point), *point)
            f.write(s)

def addIntensityToPointCloud(tuple_list, dummy_value = 0):
    new_tuple_list = []
    for t in tuple_list:
        new_tuple_list.append((t[0], t[1], t[2], dummy_value))

    return new_tuple_list

def degreesToRad(angle_degrees):
        '''
        Converts degrees into radians.
        Returns:
            - Float angle in radian
        '''
        return angle_degrees * (math.pi/180)

def calcDistanceBetween3dPoints(p1, p2):
    return math.sqrt( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2 )
