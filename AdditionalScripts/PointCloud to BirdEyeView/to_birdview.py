import matplotlib.pyplot as plt
import matplotlib
import os
from IouObjects import *
import numpy as np
from shapely.geometry import Point, Polygon, LineString
import cv2

def roty(t):
    ''' Rotation about the y-axis. '''
    c = np.cos(t)
    s = np.sin(t)
    return np.array([[c,  0,  s],
                     [0,  1,  0],
                     [-s, 0,  c]])

def getBoundingBoxTopFaceCorners(cornersList):
    '''
    Assumes that the 3d bounding box is only rotated
    around the y (up, yaw) axis

    Argument: list of IoUObjects.Vector2
    '''
    topCornersList = []
    maxheight = cornersList[0].y
    for i in range(0, len(cornersList)):
        # if a point with higher height is found
        if cornersList[i].y > maxheight:
            maxheight = cornersList[i].y
            # reset list
            topCornersList = [cornersList[i]]
        elif cornersList[i].y == maxheight:
            topCornersList.append(Vector2(cornersList[i].x, cornersList[i].z))

    return topCornersList

def getCenterPointOfVector2Polygon(pointsList):
    '''
    List of points, with type IoUObjects.Vector2D's
    '''
    tupleList = []
    for point in pointsList:
        tupleList.append((point.x, point.y))
    
    return np.array(tupleList).mean(0)

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

def drawPolygon(image, edgesList, color, thickness, translationAmount, scaleFactor):
    #print("\nNew shape edges:")

    for edge in edgesList:
        edge = [(int(edge[0][0]*scaleFactor) + translationAmount[0], int(edge[0][1]*scaleFactor) + translationAmount[1]), (int(edge[1][0]*scaleFactor) + translationAmount[0], int(edge[1][1]*scaleFactor) + translationAmount[1])]
        image = cv2.line(image, edge[0], edge[1], color, thickness)
    
    return image

def getPolygonEdges(polyPointsList):
    '''
    Argument: list of Vector2's
    Returns a list of lists of tuples. Each list of tuples
    correponds to an edge of the polygon
    The input polygon corners must have a clock wise order
    '''
    edgesList = []
    for i in range(0, len(polyPointsList)):
        if i+1 >= len(polyPointsList):
            edgesList.append([(polyPointsList[i].x, polyPointsList[i].y), (polyPointsList[0].x, polyPointsList[0].y)])
            break

        edgesList.append([(polyPointsList[i].x, polyPointsList[i].y), (polyPointsList[i+1].x, polyPointsList[i+1].y)])

    return edgesList

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

    groundTruthDataDirPath = "../../../eyeball_test/train/"

    for subdir, dirs, files in os.walk(groundTruthDataDirPath):
        for dirName in dirs:
            
            img = matplotlib.image.imread(groundTruthDataDirPath+"/"+dirName+"/"+dirName+".png")

            label = groundTruthDataDirPath+"/"+dirName+"/"+dirName+".txt"

            with open(label) as f:
                groundTruthSampleLines = [line.rstrip() for line in f]

            figure = plt.figure()

            ax = figure.add_subplot(111)

            ax.imshow(img)

            velodyne = groundTruthDataDirPath+"/"+dirName+"/"+dirName+".bin"
            
            pointcloud = np.fromfile(velodyne, dtype=np.float32, count=-1).reshape([-1,4])

            x = pointcloud[:, 0]  # x position of point
            y = pointcloud[:, 1]  # y position of point
            z = pointcloud[:, 2]  # z position of point
            r = np.zeros(pointcloud.shape[0])  # reflectance value of point

            to_write = "ply\nformat ascii 1.0\nelement vertex " + str(pointcloud.shape[0]+len(groundTruthSampleLines*8)) +  "\nproperty float x\nproperty float y\nproperty float z\nproperty float intensity\nend_header\n"

            for i in set(range(pointcloud.shape[0])):
                to_write += str(x[i])+" "+str(y[i])+" "+str(z[i])+" "+str(r[i])+"\n"

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
            
                gtBB = BoundingBoxData((float(gtBBParams[11]), float(gtBBParams[12]), float(gtBBParams[13])), float(gtBBParams[8]), float(gtBBParams[9]), float(gtBBParams[10]), float(gtBBParams[14]))

                gtBBData = get3dBoundingBoxCorners(gtBB)

                gtTopFaceCorners = getBoundingBoxTopFaceCorners(gtBBData)
                gtTopFaceAreaCenter = getCenterPointOfVector2Polygon(gtTopFaceCorners)

                poly_gt = Polygon ( [(gtTopFaceCorners[0].x, gtTopFaceCorners[0].y), 
                                        (gtTopFaceCorners[1].x, gtTopFaceCorners[1].y), 
                                        (gtTopFaceCorners[2].x, gtTopFaceCorners[2].y), 
                                        (gtTopFaceCorners[3].x, gtTopFaceCorners[3].y)] )

                print(gtBBData)
                print(gtTopFaceCorners)

                for i in gtBBData:
                    to_write += str(i.x) + " " + str(i.y) + " " + str(i.z) + " 1\n"

            return

            # with open(groundTruthDataDirPath+"/"+dirName+"/"+dirName+".ply", "w") as f:
            #     f.write(to_write)

            plt.title(dirName)
            plt.savefig(groundTruthDataDirPath+"/"+dirName+"/"+dirName+"_withBB.png")

scaleFactor = 30

if __name__ == "__main__":
    main()