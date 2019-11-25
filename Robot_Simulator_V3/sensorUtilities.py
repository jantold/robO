# class SensorUtilities.
#
# This class defines some utility methods for sensor data.
#
# Note: A polyline is sequence of points, where two consecutive points are a line segment.
#
# O. Bittel; 13.09.2019


from math import *
from Robot_Simulator_V3 import geometry


# --------
# Extracts list of segments from sensor data dists and directions (polar coordinates).
# A segment must be supported by a sequence of at least
# minPoints = 3 sensor data points.
# eps is used by the Douglas-Peucker-Algorithmus (see _extractPolyLine)
#
def extractSegmentsFromSensorData(dists, directions, eps=0.1):
    minPoints = 3
    numberedPointList = []
    nr = -1
    for i in range(len(dists)):
        d = dists[i]
        if d is None:
            continue
        alpha = directions[i]
        x_l = d * cos(alpha)
        y_l = d * sin(alpha)
        nr += 1
        numberedPointList.append([x_l, y_l, nr])

    extractedNumberedPointList = _extractPolyLine(numberedPointList, eps)
    if len(extractedNumberedPointList) == 0:
        return []

    listOfExtractedSegments = []
    for i in range(1,len(extractedNumberedPointList)):
        point1 = extractedNumberedPointList[i-1]
        point2 = extractedNumberedPointList[i]
        if point2[2]-point1[2]+1 >= minPoints:
            listOfExtractedSegments.append([point1[0:2],point2[0:2]])
    return listOfExtractedSegments


# --------
# Extract a polyline from a list of numbered points.
# Points which are closer than eps to a line segment are discarded.
# https://de.wikipedia.org/wiki/Douglas-Peucker-Algorithmus
#
def _extractPolyLine(numberedPointList, eps = 0.1):
    n = len(numberedPointList)
    if n <= 2:
        return numberedPointList

    # Finde Punkt mit groesstem Abstand:
    dmax = 0
    imax = 0
    p1 = (numberedPointList[0][0], numberedPointList[0][1])
    p2 = (numberedPointList[n - 1][0], numberedPointList[n - 1][1])
    l = (p1,p2)
    for i in range(1, len(numberedPointList)):
        p = (numberedPointList[i][0], numberedPointList[i][1])
        d = geometry.distPointSegment(p,l)
        if d > dmax:
            dmax = d
            imax = i

    # Splitte, falls dmax > eps:
    if dmax > eps:
        res1 = _extractPolyLine(numberedPointList[0:imax + 1], eps)
        res2 = _extractPolyLine(numberedPointList[imax:n], eps)
        return res1+res2[1:]
    else:
        return [numberedPointList[0], numberedPointList[n - 1]]


# --------
# Transform several polylines from robot's local to global coordinates.
#
def transformPolylinesL2G(polylines, pose):
    x_R,y_R,theta_R = pose
    polylines_g = []
    for polyline in polylines:
        polyline_g = []
        for p in polyline:
            x = p[0]
            y = p[1]
            x_g = x_R + x*cos(theta_R) - y*sin(theta_R)
            y_g = y_R + x*sin(theta_R) + y*cos(theta_R)
            polyline_g.append([x_g,y_g])
        polylines_g.append(polyline_g)
    return polylines_g


# --------
# Transform robot's local polar coordinates (d,alpha) to global coordinates
#
def transformPolarCoordL2G(d_l, alpha_l, pose):
    x_R,y_R,theta_R = pose
    coord = []
    for i in range(len(d_l)):
        d = d_l[i]
        if d == None:
            continue
        alpha = alpha_l[i]
        x_l = d*cos(alpha)
        y_l = d*sin(alpha)
        x_g = x_R + x_l*cos(theta_R) - y_l*sin(theta_R)
        y_g = y_R + x_l*sin(theta_R) + y_l*cos(theta_R)
        coord.append([x_g,y_g])
    return coord


if __name__ == "__main__":
    points = [[0,0],[1,0.05],[2,0.2],[3,0]]
    print(points)
    polyline = _extractPolyLine(points) # zum Testen dieser Methode muessen Punkte in points nicht nummeriert sein.
    print(polyline)


