#-------------------------------------------------------------------------------
# Name:        Enter path on current location
# Purpose:
#
# Author:      Henrik Skov Midtiby
#
# Created:     2013-05-18
# Copyright:   (c) Henirk Skov Midtiby 2013
# Licence:     ?
#-------------------------------------------------------------------------------
#!/usr/bin/env python

import doctest
from numpy import *
import csv
import matplotlib.pylab as plt

def partOfLineSegmentClosestToPoint(lineStart, lineEnd, point):
    direction = lineEnd - lineStart
    value = inner((1.0 * point - lineStart), direction) / inner(direction, direction)
    if(value < 0):
        return lineStart
    if(value > 1):
        return lineEnd
    return lineStart + value * direction
    pass

def minDistFromPointToLineSegment(point, lineStart, lineEnd):
    closestPoint = partOfLineSegmentClosestToPoint(lineStart, lineEnd, point)
    distToClosestPoint = linalg.norm(closestPoint - point)
    return(distToClosestPoint)

def locateClosestLineSegment(path, point):
    minDistance = 10000000000000
    idx = -1
    for k in range(path.shape[0] - 1):
        pointA = array([path[k][0], path[k][1]])
        pointB = array([path[k + 1][0], path[k + 1][1]])
        dist = minDistFromPointToLineSegment(point, pointA, pointB)
        if(dist < minDistance):
            minDistance = dist
            idx = k

    return idx

def locateLineSegmentsWithinDistance(path, point, distance):
    idxList = []
    distList = []
    for k in range(path.shape[0] - 1):
        pointA = array([path[k][0], path[k][1]])
        pointB = array([path[k + 1][0], path[k + 1][1]])
        dist = minDistFromPointToLineSegment(point, pointA, pointB)
        if(dist < distance):
            idxList.append(k)
            distList.append(dist)

    return [idxList, distList]

def loadRoute(filename):
    fh = open(filename, "r")
    reader = csv.reader(fh, delimiter='\t')
    # Some code borrowed from
    # http://stackoverflow.com/questions/2664790/reading-csv-files-in-numpy-where-delimiter-is
    converters = [float, float, int]
    result = array([[conv(col) for col, conv in zip(row, converters)] for row in reader])
    fh.close()
    return result

def main():
    pointA = array([1, 0])
    pointB = array([10, 2])
    pointC = array([3, 3])
    print(partOfLineSegmentClosestToPoint(pointA, pointB, pointC))
    print(minDistFromPointToLineSegment(pointC, pointA, pointB))
    pass
    route = loadRoute("aExperimentalFieldAtTekRoutePlan.csv")
    plt.plot(route[:, 0], route[:, 1], linewidth = 2)

    tempPoint = array([588842.1, 6137312.7])
    plt.scatter(tempPoint[0], tempPoint[1], s = 100)

    [idxList, distList] = locateLineSegmentsWithinDistance(route, tempPoint, 0.5)

    minval = min(idxList)
    maxval = max(idxList)
    if(maxval - minval > len(idxList)):
        pass
    else:
        val = locateClosestLineSegment(route, tempPoint)
        plt.plot(route[val:, 0], route[val:, 1], color = "red", linewidth = 2)

    plt.show()

if __name__ == '__main__':
    main()
