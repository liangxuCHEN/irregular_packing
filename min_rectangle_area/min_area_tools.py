# coding=utf8
from qhull_2d import *
from min_bounding_rect import *


def min_rectangle(xy_points):
    """
    寻找最小包络矩形,并且把矩形旋转至（0.0）坐标水平放置
    :param xy_points:
    :return:
    """
    hull_points = qhull2D(xy_points)
    hull_points = hull_points[::-1]
    (rot_angle, area, width, height, center_point, corner_points) = minBoundingRect(hull_points)

    # roting -> h level 转回水平放置
    rot_angle += pi * (3 / 2)
    # 旋转矩阵
    R = array([[math.cos(rot_angle), math.cos(rot_angle - (math.pi / 2))],
               [math.cos(rot_angle + (math.pi / 2)), math.cos(rot_angle)]])
    rot_points = dot(R, transpose(hull_points))  # 2x2 * 2xn
    hull_points = transpose(rot_points)
    corner_points_2 = dot(R, transpose(corner_points))
    corner_points = transpose(corner_points_2)

    # 计算平移距离, corner_points[2] 是左下方的点
    dx = -corner_points[2][0]
    dy = -corner_points[2][1]
    corner_points[:, 0] += dx
    corner_points[:, 1] += dy
    hull_points[:, 0] += dx
    hull_points[:, 1] += dy

    # polygon ares
    areas = polygon_areas(hull_points)
    return width, height, hull_points, areas


def polygon_areas(points):
    total_areas = 0
    num = len(points)
    for i in range(0, num):
        end_point = points[(i+1) % num]
        total_areas += points[i][0] * end_point[1] - end_point[0] * points[i][1]

    return 0.5 * total_areas