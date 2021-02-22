import cv2
import numpy as np
from utils import *
import random

def drawRectangle(image, startPoint, endPoint, color, thickness):
    '''
    # Start coordinate, here (5, 5) 
    # represents the top left corner of rectangle 
    startPoint = (5, 5) 
    
    # Ending coordinate, here (220, 220) 
    # represents the bottom right corner of rectangle 
    endPoint = (220, 220) 
    
    # Blue color in BGR 
    color = (255, 0, 0) 
    
    # Line thickness of 2 px 
    thickness = 2
    '''
    
    # Using cv2.rectangle() method 
    # Draw a rectangle with blue line borders of thickness of 2 px 
    image = cv2.rectangle(image, startPoint, endPoint, color, thickness) 

    return image

def drawPolygon(image, edgesList, color, thickness, translationAmount, scaleFactor):
    #print("\nNew shape edges:")

    for edge in edgesList:
        edge = [(int(edge[0][0]*scaleFactor) + translationAmount[0], int(edge[0][1]*scaleFactor) + translationAmount[1]), (int(edge[1][0]*scaleFactor) + translationAmount[0], int(edge[1][1]*scaleFactor) + translationAmount[1])]
        #print("\t" + str(edge))
        image = cv2.line(image, edge[0], edge[1], color, thickness)
    
    return image


def drawResult(sampleIndex, gtBoundingBox, gtCenterPoint, infBoundingBox, infCenterPoint, overlapedArea, overlapAreaCenterPoint, scaleFactor = 30):
    '''
    Each argument is a list of points represented by 2d tuples
    '''
    gtBoundingBoxEdges = getPolygonEdges(gtBoundingBox)
    infBoundingBoxEdges = getPolygonEdges(infBoundingBox)
    overlapedAreaEdges = getPolygonEdges_TupleVersion(overlapedArea)

    windowName = 'Iou Result for BEV bounding boxes'
    windowSize = (300, 300)
    windowChannels = 3

    image = np.zeros((windowSize[0], windowSize[1], 3), dtype="uint8")
    cv2.imshow(windowName, image)

    windowMidPoint = (windowSize[0]/2, windowSize[1]/2)

    # translation amount to translate the center position of the ground truth bounding box to the center of the window
    translationAmount = (int(windowMidPoint[0] - gtCenterPoint[0] * scaleFactor), int(windowMidPoint[1] - gtCenterPoint[1] * scaleFactor))

    image = drawPolygon(image, gtBoundingBoxEdges, (0, 200, 200), 2, translationAmount, scaleFactor)
    image = drawPolygon(image, infBoundingBoxEdges, (200, 0, 200), 2, translationAmount, scaleFactor)
    image = drawPolygon(image, overlapedAreaEdges, (200, 200, 0), 2, translationAmount, scaleFactor)

    print("\n> Ground truth BEV bounding box color: yellow")
    print("> Infered BEV bounding box color: magenta")
    print("> Overlaping area polygon color: cyan")

    image = cv2.flip(image, 0)
    cv2.imshow(windowName, image)
    cv2.waitKey(0); 

    # output images
    cv2.imwrite('./iou_image_results/' + str(sampleIndex) + '.png',image) 
    
    