import matplotlib.pyplot as plt
import matplotlib
import os
from IouObjects import *
import numpy as np

def roty(t):
    ''' Rotation about the y-axis. '''
    c = np.cos(t)
    s = np.sin(t)
    return np.array([[c,  0,  s],
                     [0,  1,  0],
                     [-s, 0,  c]])

def get3dBoundingBoxCorners(bbData):
    '''
    From the data present in the label.txt file of the ground truth
    and infered bounding boxes, calculate the 8 corners of the
    3D bounding box.

    Argument: IoUObjects.BoundingBoxData

    Return: a list of Vector3 objects
        - top face: first 4 points
        - bottom face: last 4 points

    Ref: frustum pointnet
    '''

    # compute rotational matrix around yaw axis
    R = roty(bbData.ry)    

    # 3d bounding box dimensions
    l = bbData.length
    w = bbData.width
    h = bbData.height

    # 3d bounding box corners
    x_corners = [l/2,l/2,-l/2,-l/2,l/2,l/2,-l/2,-l/2]
    y_corners = [0,0,0,0,-h,-h,-h,-h]
    z_corners = [w/2,-w/2,-w/2,w/2,w/2,-w/2,-w/2,w/2]

    # rotate and translate 3d bounding box
    corners_3d = np.dot(R, np.vstack([x_corners,y_corners,z_corners]))

    #print corners_3d.shape
    corners_3d[0,:] = corners_3d[0,:] + bbData.position[0]
    corners_3d[1,:] = corners_3d[1,:] + bbData.position[1]
    corners_3d[2,:] = corners_3d[2,:] + bbData.position[2]

    # corners_3d = [[x coords of the 8 corners], [y coords of 8 the corners], [z coords of the 8 corners]]
    return getCornerVectorsList(corners_3d)

def getCornerVectorsList(bbCorners):
    '''
    Argument example:
        [[-2.65513732 -0.64306091  0.23794332 -1.77413309 -2.65513732 -0.64306091 0.23794332 -1.77413309]
        [ 1.835671    1.835671    1.835671    1.835671    0.304741    0.304741   0.304741   0.304741  ]
        [22.18115469 22.54735297 17.70667531 17.34047703 22.18115469 22.54735297 17.70667531 17.34047703]]

    Return: IoUObjects.Vector3 list
    '''
    cornersList = []

    for i in range(0, len(bbCorners[0])):
        cornersList.append(Vector3(round(bbCorners[0][i], 6), round(bbCorners[1][i], 6), round(bbCorners[2][i], 6)))

    return cornersList

def main():

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

    img = matplotlib.image.imread("/media/joao/My Passport/Elements/testeGTA/training/image_2/000001.png")

    label = "/media/joao/My Passport/Elements/testeGTA/training/label_2/000001.txt"

    with open(label) as f:
        groundTruthSampleLines = [line.rstrip() for line in f]

    figure = plt.figure()

    ax = figure.add_subplot(111)

    ax.imshow(img)
                
    for j in range(0, len(groundTruthSampleLines)):
        gtBBParams = groundTruthSampleLines[j].split(" ")

        if "DontCare" in gtBBParams[0]:
            continue
        
        left = float(gtBBParams[4])
        top = float(gtBBParams[5])
        height = abs(top - float(gtBBParams[7]))
        width = abs(left - float(gtBBParams[6]))
        rect = matplotlib.patches.Rectangle((left, top), width, height, edgecolor='r', facecolor="none")
        ax.add_patch(rect)

    plt.show()

if __name__ == "__main__":
    main()