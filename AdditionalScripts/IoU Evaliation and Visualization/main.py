import os
import math
import numpy as np
from graphics import *
from utils import *
from IouObjects import *
from shapely.geometry import Point, Polygon, LineString

'''
    IoU calculation steps based on the paper: https://arxiv.org/pdf/1908.03851.pdf
'''

def calculateIoU_BEVRotated_and_3D_BBs(sampleIndex, infBBData, gtBBData, renderResult=False): 
    '''
    Arguments:
    - inferedBBData: [Vector3, Vector3, ...]
    - gtBBData: [Vector3, Vector3, ...]
    - the scale factor is used to resize the display of the bounding boxes and the resulting overlap polygon
    Birds-eye-view 2d bounding boxes IoU
    Use of the x and z coordinates (y is up)
    Corners must be ordered CW, starting from the top face
    '''
    # 0 - Get the corners of the top face of both 3d bounding boxes
    #     The order of the corners is clock-wise, from top-left to bottom-left
    infTopFaceCorners = getBoundingBoxTopFaceCorners(infBBData)
    infTopFaceAreaCenter = getCenterPointOfVector2Polygon(infTopFaceCorners)
    gtTopFaceCorners = getBoundingBoxTopFaceCorners(gtBBData)
    gtTopFaceAreaCenter = getCenterPointOfVector2Polygon(gtTopFaceCorners)

    # 1 - Calculate the BEV area of the two 3d bounding boxes
    print("\nArea BEV infered bounding box: ")
    edge_infA = math.hypot(infTopFaceCorners[1].x-infTopFaceCorners[0].x, infTopFaceCorners[1].y-infTopFaceCorners[0].y)
    edge_infB = math.hypot(infTopFaceCorners[2].x-infTopFaceCorners[1].x, infTopFaceCorners[2].y-infTopFaceCorners[1].y)
    areaInfBB = edge_infA * edge_infB
    print(str(areaInfBB))

    print("\nArea BEV ground truth bounding box: ")
    edge_gtA = math.hypot(gtTopFaceCorners[1].x-gtTopFaceCorners[0].x, gtTopFaceCorners[1].y-gtTopFaceCorners[0].y)
    edge_gtB = math.hypot(gtTopFaceCorners[2].x-gtTopFaceCorners[1].x, gtTopFaceCorners[2].y-gtTopFaceCorners[1].y)
    areaGtBB = edge_gtA * edge_gtB
    print(str(areaGtBB))
    
    # 2 - Determine the corners of the polygon that defines the overlap area
    ##print("\nList of the infered BEV BB vertices inside the ground truth BEV BB area")
    overlapAreaCorners = []
    
    poly_gt = Polygon ( [(gtTopFaceCorners[0].x, gtTopFaceCorners[0].y), 
                            (gtTopFaceCorners[1].x, gtTopFaceCorners[1].y), 
                            (gtTopFaceCorners[2].x, gtTopFaceCorners[2].y), 
                            (gtTopFaceCorners[3].x, gtTopFaceCorners[3].y)] )
    for i in range(0, len(gtTopFaceCorners)):
        p_inf = Point(infTopFaceCorners[i].x, infTopFaceCorners[i].y)

        if p_inf.within(poly_gt):
            overlapAreaCorners.append((infTopFaceCorners[i].x, infTopFaceCorners[i].y))
    ##print(overlapAreaCorners)

    ##print("\nList of the overlaped area points, including the ground truth BEV BB vertices that are inside the infered BEV BB area")
    poly_inf = Polygon ( [(infTopFaceCorners[0].x, infTopFaceCorners[0].y), 
                            (infTopFaceCorners[1].x, infTopFaceCorners[1].y), 
                            (infTopFaceCorners[2].x, infTopFaceCorners[2].y), 
                            (infTopFaceCorners[3].x, infTopFaceCorners[3].y)] )
    for i in range(0, len(infTopFaceCorners)):
        p_gt = Point(gtTopFaceCorners[i].x, gtTopFaceCorners[i].y)
        
        if p_gt.within(poly_inf):
            overlapAreaCorners.append((gtTopFaceCorners[i].x, gtTopFaceCorners[i].y))
    ##print(overlapAreaCorners)

    ##print("\nFor each edge of the infered BB, determine the intersection points with the edges of the ground truth BEV BB")
    
    infTopFaceEdges = getPolygonEdges(infTopFaceCorners)
    gtTopFaceEdges = getPolygonEdges(gtTopFaceCorners)

    for i in range(0, len(infTopFaceEdges)):
        for j in range(0, len(gtTopFaceEdges)):
            infEdge = LineString(infTopFaceEdges[i])
            gtEdge = LineString(gtTopFaceEdges[j])

            if infEdge.intersects(gtEdge):
                intersectionPoint = infEdge.intersection(gtEdge).coords.xy
                overlapAreaCorners.append((intersectionPoint[0][0], intersectionPoint[1][0]))

    ##print(overlapAreaCorners)

    # 3 - order the point in the clock-wise order
    overlapedAreaCenter = np.array(overlapAreaCorners).mean(0)
    ##print("\nPolygon center position:")
    ##print(overlapedAreaCenter)

    # polygon points list in clock-wise order
    sortedPolygonPoints = getClockWiseSortedPoints(overlapedAreaCenter, overlapAreaCorners)
    ##print("\nClock-wise ordered polgon points:")
    ##print(sortedPolygonPoints)

    # 4 - calculate area of the overlap polygon
    ##print("\nOverlapped area:")
    overlappedArea = polygonArea(sortedPolygonPoints)
    ##print(overlappedArea)

    # 5 - Calculate the IoU of the rotated BEV infered bounding box
    iouResultRotated2D = calculateRotated2dIoU(areaGtBB, areaInfBB, overlappedArea)
    ##print("\nIou of the BEV rotated 2D bounding box:")
    ##print(iouResultRotated2D)

    print("\nIoU BEV: " + str(iouResultRotated2D))

    if renderResult:
        drawResult(sampleIndex, gtTopFaceCorners, gtTopFaceAreaCenter, infTopFaceCorners, infTopFaceAreaCenter, overlapAreaCorners, overlapedAreaCenter, scaleFactor)

    #### Calculate height intersection percentage (these steps don't concern 2d rotated bb iou calculation)
    # [1] - get height limits of infered and groundtruth bounding boxes
    infYLimits = getYRangeFrom3dBB(infBBData)
    gtYLimits = getYRangeFrom3dBB(gtBBData)

    # [2] - Calulcate height (1D) IOU
    iouHeight = calculate_1D_iou(infYLimits, gtYLimits)
    print('\nIOU height:')
    print(iouHeight)

    # [3] - Calculate 3D IOU
    iou3D = iouResultRotated2D * iouHeight
    print('\nIOU 3D:')
    print(iou3D)

    return iouResultRotated2D, iou3D

def calculateIous(sampleIndex, gtBB, infBB):
    # get 3d bounding box corners; each face's (top and bottom faces) corners are ordered clock-wise, from top-left to bottom-left
    gtCornersList = get3dBoundingBoxCorners(gtBB)
    infCornersList = get3dBoundingBoxCorners(infBB)

    iouResultRotated2D, iou3D = calculateIoU_BEVRotated_and_3D_BBs(sampleIndex, infCornersList, gtCornersList, renderResult=True)

    return iouResultRotated2D, iou3D

def example():
    # ground truth 3d bounding box
    gtBB = BoundingBoxData((-1.208597, 1.835671, 19.943915), 1.53093, 2.045129, 4.920196, -1.750826)

    # infered 3d bounding box
    infBB = BoundingBoxData((-1.122418, 1.856978, 19.481645), 1.507002, 1.659477, 4.034763, -1.772969)

    calculateIous(0, gtBB, infBB)

def main():
    # inferedDataDirPath = "./Data/Generated Dataset - Frustum PointNet Inferences/predicted/"
    # groundTruthDataDirPath = "./Data/Generated Dataset - Frustum PointNet Inferences/groundtruth/"
    groundTruthDataDirPath = "./Data/Generated Dataset/groundtruth/"

    iouRotated2DList = []
    iou3DList = []

    # inferedFilepaths = []
    # for subdir, dirs, files in os.walk(inferedDataDirPath):
    #     for filename in files:
    #         inferedFilepaths.append(inferedDataDirPath + filename)

    groundTruthFilepaths = []
    for subdir, dirs, files in os.walk(groundTruthDataDirPath):
        for filename in files:
            groundTruthFilepaths.append(groundTruthDataDirPath + filename)

    # if len(inferedFilepaths) != len(groundTruthFilepaths):
    #     print("ERROR: The number of infered results files is not equal to the number of ground truth files")
    #     return

    # iterate through every sample files
    for i in range(0, len(groundTruthFilepaths)): 
        print("\n>>> File: " + groundTruthFilepaths[i])
    # for i in range(0, len(inferedFilepaths)): 
    #     print("\n>>> File: " + inferedFilepaths[i])

    #     with open(inferedFilepaths[i]) as f:
    #         inferedSampleLines = [line.rstrip() for line in f]
        
        with open(groundTruthFilepaths[i]) as f:
            groundTruthSampleLines = [line.rstrip() for line in f]

        # if not inferedSampleLines:
        #     print("Infered sample file does not contain any entries.\nThis sample will be ignored")
        #     continue

        # if (len(inferedSampleLines) != len(groundTruthSampleLines)):
        #     print("The number of objects in the infered data file:\n\t-" + inferedSampleLines[0] + "\nis not the same as in the corresponding ground truth sample.\nThis sample will be ignored")
        #     continue
            
        # if len(inferedSampleLines) > 1:
        #     print("Current script only supports one entry per sample.\nThis sample will be ignored")
        #     continue

        # iterate through every object inside a sample
        # for j in range(0, len(inferedSampleLines)):
        for j in range(0, len(groundTruthSampleLines)):
            # type, truncated, occluded, alpha, minx, miny, maxx, maxy, height, width, length, x, y, z, ry, score
            # infBBParams = inferedSampleLines[j].split(" ")
            gtBBParams = groundTruthSampleLines[j].split(" ")

            if "DontCare" in gtBBParams[0]:
                continue
            
            # ground truth 3d bounding box
            gtBB = BoundingBoxData((float(gtBBParams[11]), float(gtBBParams[12]), float(gtBBParams[13])), float(gtBBParams[8]), float(gtBBParams[9]), float(gtBBParams[10]), float(gtBBParams[14]))

            # infered 3d bounding box
            # infBB = BoundingBoxData((float(infBBParams[11]), float(infBBParams[12]), float(infBBParams[13])), float(infBBParams[8]), float(infBBParams[9]), float(infBBParams[10]), float(infBBParams[14]))

            # iouRotated2D, iou3D = calculateIous(i, gtBB, infBB)

            # iouRotated2DList.append(iouRotated2D)
            # iou3DList.append(iou3D)

            gtBBData = get3dBoundingBoxCorners(gtBB)

            gtTopFaceCorners = getBoundingBoxTopFaceCorners(gtBBData)
            gtTopFaceAreaCenter = getCenterPointOfVector2Polygon(gtTopFaceCorners)

            poly_gt = Polygon ( [(gtTopFaceCorners[0].x, gtTopFaceCorners[0].y), 
                                    (gtTopFaceCorners[1].x, gtTopFaceCorners[1].y), 
                                    (gtTopFaceCorners[2].x, gtTopFaceCorners[2].y), 
                                    (gtTopFaceCorners[3].x, gtTopFaceCorners[3].y)] )

            windowName = 'GT bounding boxes'
            windowSize = (300, 300)

            windowMidPoint = (windowSize[0]/2, windowSize[1]/2)

            image = np.zeros((windowSize[0], windowSize[1], 3), dtype="uint8")
            cv2.imshow(windowName, image)

            gtBoundingBoxEdges = getPolygonEdges(gtTopFaceCorners)

            translationAmount = (int(windowMidPoint[0] - gtTopFaceAreaCenter[0] * scaleFactor), int(windowMidPoint[1] - gtTopFaceAreaCenter[1] * scaleFactor))

            image = drawPolygon(image, gtBoundingBoxEdges, (0, 200, 200), 2, translationAmount, scaleFactor)

            image = cv2.flip(image, 0)
            cv2.imshow(windowName, image)
            cv2.waitKey(0)
    
    # averageIoURotated2D = np.array(iouRotated2DList).mean(0)
    # averageIoU3D = np.array(iou3DList).mean(0)

    # print("\nAverage Iou for BEV bounding boxes: " + str(averageIoURotated2D))
    # print("\nAverage Iou for 3D bounding boxes: " + str(averageIoU3D))




# size of the displayed bounding boxes in opencv window
scaleFactor = 30

if __name__ == "__main__":
    main()





