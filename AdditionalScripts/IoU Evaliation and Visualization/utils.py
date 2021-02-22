import numpy as np
from IouObjects import *

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

def getYRangeFrom3dBB(cornersList):
    '''
    Obtains top and bottom y value of the 3d bounding box
    
    Argument: list of IoUObjects.Vector2
    '''
    yMin = cornersList[0].y 
    yMax = cornersList[0].y 
    for i in range(0, len(cornersList)):
        if cornersList[i].y < yMin:
            yMin = cornersList[i].y
        elif cornersList[i].y > yMax:
            yMax = cornersList[i].y
    return (yMin, yMax)

def calculate_1D_iou(infYLimits, gtYLimits):
    '''
    infYLimits = (infMiny, infMaxy)
    gtYLimits = (gtMiny, gtMaxy)
    '''
    lengthInferedHeight = infYLimits[1] - infYLimits[0]
    lengthGTHeight = gtYLimits[1] - gtYLimits[0]
    
    overlapLimits = []
    if infYLimits[0] > gtYLimits[1]:
        return 0
    elif infYLimits[1] < gtYLimits[0]:
        return 0

    # maximum of the lowest values
    if infYLimits[0] > gtYLimits[0]:
        overlapLimits.append(infYLimits[0])
    elif infYLimits[0] < gtYLimits[0]:
        overlapLimits.append(gtYLimits[0])
    
    # minimun of the highest values
    if infYLimits[1] < gtYLimits[1]:
        overlapLimits.append(infYLimits[1])
    else:
        overlapLimits.append(gtYLimits[1])

    lengthOverlap = overlapLimits[1] - overlapLimits[0]

    return lengthOverlap / (lengthInferedHeight + lengthGTHeight - lengthOverlap)



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

def getPolygonEdges_TupleVersion(polyPointsList):
    '''
    Argument: list of Vector2's
    Returns a list of lists of tuples. Each list of tuples
    correponds to an edge of the polygon
    The input polygon corners must have a clock wise order
    '''
    edgesList = []
    for i in range(0, len(polyPointsList)):
        if i+1 >= len(polyPointsList):
            edgesList.append([(polyPointsList[i][0], polyPointsList[i][1]), (polyPointsList[0][0], polyPointsList[0][1])])
            break

        edgesList.append([(polyPointsList[i][0], polyPointsList[i][1]), (polyPointsList[i+1][0], polyPointsList[i+1][1])])

    return edgesList

def getCenterPointOfVector2Polygon(pointsList):
    '''
    List of points, with type IoUObjects.Vector2D's
    '''
    tupleList = []
    for point in pointsList:
        tupleList.append((point.x, point.y))
    
    return np.array(tupleList).mean(0)

def less(center, a, b):
    '''
    Arguments: 
        - center: [float, float]
        - a and b: (float, float)

    Source: https://stackoverflow.com/a/6989383
    '''
    if a[0] - center[0] >= 0 and b[0] - center[0] < 0:
        return True
    if a[0] - center[0] < 0 and b[0] - center[0] >= 0:
        return False
    if a[0] - center[0] == 0 and b[0] - center[0] == 0:
        if a[1] - center[1] >= 0 or b[1] - center[1] >= 0:
            return a[1] > b[1]
        return b[1] > a[1]

    # compute the cross product of vectors (center -> a) x (center -> b)
    det = (a[0] - center[0]) * (b[1] - center[1]) - (b[0] - center[0]) * (a[1] - center[1])
    if det < 0:
        return True
    if det > 0:
        return False

    # points a and b are on the same line from the center
    # check which point is closer to the center
    d1 = (a[0] - center[0]) * (a[0] - center[0]) + (a[1] - center[1]) * (a[1] - center[1])
    d2 = (b[0] - center[0]) * (b[0] - center[0]) + (b[1] - center[1]) * (b[1] - center[1])
    return d1 > d2

def getClockWiseSortedPoints(center, points):
    '''
    BubbleSort
    Source: https://stackabuse.com/sorting-algorithms-in-python/
    '''
    # We set swapped to True so the loop looks runs at least once
    swapped = True
    while swapped:
        swapped = False
        for i in range(len(points) - 1):
            #if points[i] > points[i + 1]:
            if less(center, points[i + 1], points[i]):
                # Swap the elements
                points[i], points[i + 1] = points[i + 1], points[i]
                # Set the flag to True so we'll loop again
                swapped = True
    
    return points

def polygonArea(vertices):
    '''
    Shoelace formula to calculate the area of a polygon
    the points must be sorted anticlockwise (or clockwise)

    Source: https://algorithmtutor.com/Computational-Geometry/Area-of-a-polygon-given-a-set-of-points/
    '''
    psum = 0
    nsum = 0

    for i in range(len(vertices)):
        sindex = (i + 1) % len(vertices)
        prod = vertices[i][0] * vertices[sindex][1]
        psum += prod

    for i in range(len(vertices)):
        sindex = (i + 1) % len(vertices)
        prod = vertices[sindex][0] * vertices[i][1]
        nsum += prod

    return abs(1/2*(psum - nsum))

def calculateRotated2dIoU(areaGt, areaInf, areaOverlap):
    return areaOverlap / (areaGt + areaInf - areaOverlap)

def calculateRotated3DIoU(volumeGt, volumeInf, volumeOverlap):
    return volumeOverlap / (volumeGt + volumeInf - volumeOverlap)