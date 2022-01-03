import cv2
import numpy as np
import math

width, height = 830, 100
x_max, y_max = 69.0, 50.0
points1 = np.float32([[247, 227], [730, 221], [5, 290], [950, 280]]) # source
points2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
matrix = cv2.getPerspectiveTransform(points1, points2)


def warpImg(frame):
    warpedFrame = cv2.warpPerspective(frame, matrix, (width, height))
    return warpedFrame


def getPosition(point1, point2):
    p = ((point1[0] + point2[0]) / 2, point2[1])  # mid point
    px = (matrix[0][0] * p[0] + matrix[0][1] * p[1] + matrix[0][2]) / (
    (matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2]))
    py = (matrix[1][0] * p[0] + matrix[1][1] * p[1] + matrix[1][2]) / (
    (matrix[2][0] * p[0] + matrix[2][1] * p[1] + matrix[2][2]))
    coordinates = [(x_max * px / width), (y_max * py / height)-4]
    return coordinates


'''
point1____________________________
|                                |
|                                |
|                                |
|                                |
|                                |
____________midPoint__________point2
'''


def match_cam_ino(position, dictionary):
    min_dist = 10000.0
    xy_list = []
    for name, food in dictionary.items():
        xy_list.append(food.position)
    print(xy_list)
    pizza = xy_list[0]
    for coordinate in xy_list:
        dist = math.sqrt((position[0] - coordinate[0] - 6) ** 2 + (position[1] - coordinate[1] - 6) ** 2)
        # dist = np.linalg.norm(position - coordinate)
        if dist < min_dist:
            min_dist = dist
            pizza = coordinate
    for name, food in dictionary.items():
        if pizza == food.position:
            finalweight = food.weight
    return finalweight


def match_cam_ino_2(br_list, dictionary):
    pass

"""
cv2.imshow("pencere", warpImg(frame))
cv2.waitKey(0)
"""