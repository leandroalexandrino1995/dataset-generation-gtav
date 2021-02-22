from pathlib import Path
import numpy as np
import os.path
import math
import struct

class Calibration:

    def __init__(self, imageSize, fov):
        '''
        - imageSize: (img_width, img_height) | integer tuple
        - fov: field of view | integer
        '''
        self.imageSize = imageSize
        self.fov = fov
        
        self.Cu = self.imageSize[0]/2 # half screen width
        self.Cv = self.imageSize[1]/2  # half screen height

        self.hor_fov = Calibration.calcHorizontalFov(self.fov)  
        self.fx = Calibration.calcFx(self.imageSize[0], self.hor_fov) 

        self.vert_fov = Calibration.calcVerticalFov(self.imageSize[0], self.imageSize[1], self.hor_fov)
        self.fy = Calibration.calcFy(self.imageSize[1], self.vert_fov)
        
        self.p0_mat = Calibration.create_P0mat(self.fx, self.fy, self.Cu, self.Cv)

        self.p1_mat = self.p2_mat = self.p3_mat = self.p0_mat

        self.R0 = Calibration.create_R0mat()

        self.V2C = Calibration.create_Velo2CamMat()

        self.C2V = Calibration.inverse_rigid_trans(self.V2C)

        self.tr_imu_to_velo = Calibration.create_tr_imu_to_velo()


    @staticmethod
    def calcHorizontalFov(fov):
        return fov / 360. * 2. * np.pi  
    
    @staticmethod
    def calcVerticalFov(img_width, img_height, hor_fov):
        return 2. * np.arctan(np.tan(hor_fov / 2) * img_height / img_width)
    
    @staticmethod
    def calcFx(img_width, hor_fov):
        return img_width / (2. * np.tan(hor_fov / 2.))
    
    @staticmethod
    def calcFy(img_height, vert_fov):
        return img_height / (2. * np.tan(vert_fov / 2.))

    @staticmethod
    def create_P0mat(fx, fy, Cu, Cv):
        mat = [[fx, 0., Cu, 0.],
                [0., fy, Cv, 0.],
                [0., 0., 1., 0.]]
        mat = np.array(mat)
        return np.reshape(mat, [3,4])

    @staticmethod
    def create_R0mat():
        r0_rect = [[1, 0, 0],
                  [0, 1, 0],
                   [0, 0, 1]]
        # Rotation from reference camera coord to rect camera coord
        r0_rect = np.array(r0_rect)
        return np.reshape(r0_rect,[3,3])

    @staticmethod
    def create_Velo2CamMat():
        '''
        Assumption: camera is at the same position and orientation as the lidar
        '''
        tr_velo_to_cam = [[0, -1, 0, 0],
                          [0, 0, -1, 0],
                          [1, 0, 0, 0]]

        tr_velo_to_cam = np.array(tr_velo_to_cam)
        return np.reshape(tr_velo_to_cam, [3,4])

    @staticmethod
    def create_tr_imu_to_velo():
        tr_imu_to_velo = [[1, 0, 0, 0],
                          [0, 1, 0, 0],
                          [0, 0, 1, 0]]
        
        tr_imu_to_velo = np.array(tr_imu_to_velo)
        return np.reshape(tr_imu_to_velo, [3,4])

    @staticmethod
    def inverse_rigid_trans(Tr):
        ''' Inverse a rigid body transform matrix (3x4 as [R|t])
            [R'|-R't; 0|1]
            
            Ref: https://github.com/charlesq34/frustum-pointnets/blob/master/kitti/kitti_util.py
        '''
        inv_Tr = np.zeros_like(Tr) # 3x4
        inv_Tr[0:3,0:3] = np.transpose(Tr[0:3,0:3])
        inv_Tr[0:3,3] = np.dot(-np.transpose(Tr[0:3,0:3]), Tr[0:3,3])
        return inv_Tr

    def saveCalibrationFile(self, dirname, filename):
        line = Calibration.matToStringKitti("P0", self.p0_mat)
        line += Calibration.matToStringKitti("P1", self.p1_mat)
        line += Calibration.matToStringKitti("P2", self.p2_mat)
        line += Calibration.matToStringKitti("P3", self.p3_mat)
        line += Calibration.matToStringKitti("R0_rect", self.R0)
        line += Calibration.matToStringKitti("Tr_velo_to_cam", self.V2C)
        line += Calibration.matToStringKitti("Tr_imu_to_velo", self.tr_imu_to_velo)

        with open(os.path.join(dirname, filename), "w") as the_file:
            the_file.write(line)

    @staticmethod
    def matToStringKitti(name, mat):
        '''
        Arguments:
            - name: name of the matrix
            - mat: list of lists of int or float values
        Returns:
            - string
        '''
        line = name + ": "
        for i in range(0, len(mat)):
            for j in range(0, len(mat[i])):
                line += str(mat[i][j]) + " "

        line += "\n"
        
        return line

    

