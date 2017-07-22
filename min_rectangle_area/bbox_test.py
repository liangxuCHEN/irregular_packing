# coding=utf8
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from qhull_2d import *
from min_bounding_rect import *

if __name__ == "__main__":
    #
    # Un-comment one of these shapes below:
    #

    # Square
    # xy_points = 10*array([(x,y) for x in arange(10) for y in arange(10)])

    # Random points
    xy_points = 100*random.random((32,2))
    # A rectangle
    #xy_points = array([ [0,0], [1,0], [1,2], [0,2], [0,0] ])

    # A rectangle, with 5th outlier
    # xy_points = array([[0, 0],[10, 0], [15, 5], [10, 15], [7,8], [3, 8], [0,15], [-5, 5], [0, 0]])

    #--------------------------------------------------------------------------#

    # Find convex hull
    #print xy_points
    hull_points = qhull2D(xy_points)

    # Reverse order of points, to match output from other qhull implementations
    hull_points = hull_points[::-1]
    # print type(hull_points)
    # print hull_points
    # print hull_points+5
    # exit(0)

    print 'Convex hull points: \n', hull_points, "\n"

    # Find minimum area bounding rectangle
    (rot_angle, area, width, height, center_point, corner_points) = minBoundingRect(hull_points)

    # print "Minimum area bounding box:"
    print "Rotation angle:", rot_angle, "rad  (", rot_angle*(180/math.pi), "deg )"

    # print "Corner points: \n", corner_points, "\n"  # numpy array
    fig = plt.figure()
    ax = plt.axes()
    ax.set_xlim(-200, 350)
    ax.set_ylim(-200, 350)
    output_obj = list()
    # output_obj.append(patches.Polygon(corner_points, fc='blue'))
    # output_obj.append(patches.Polygon(hull_points, fc='#CCCCCC'))

    # move
    # other = hull_points + 5
    # roting -> h level 转回水平放置
    rot_angle = pi/2 + pi + rot_angle
    R = array([[math.cos(rot_angle), math.cos(rot_angle - (math.pi / 2))],
               [math.cos(rot_angle + (math.pi / 2)), math.cos(rot_angle)]])
    rot_points = dot(R, transpose(hull_points))  # 2x2 * 2xn
    hull_points = transpose(rot_points)
    corner_points_2 = dot(R, transpose(corner_points))
    corner_points = transpose(corner_points_2)
    # print "Rotation angle:", rot_angle_2, "rad  (", rot_angle_2 * (180 / math.pi), "deg )"
    # print "Width:", width_2, " Height:", height_2, "  Area:", area
    # print "Center point: \n", center_point_2  # numpy array
    # print "Corner points: \n", corner_points_2, "\n"  # numpy array

    # 计算平移距离, corner_points[1] 是左下方的点
    print width, height
    print corner_points[0][1] - corner_points[2][1]
    print corner_points[0][0] - corner_points[2][0]
    dx = -corner_points[2][0]
    dy = -corner_points[2][1]
    print dx, dy
    corner_points[:, 0] += dx
    corner_points[:, 1] += dy
    print "new  points: \n", corner_points, "\n"  # numpy array
    hull_points[:, 0] += dx
    hull_points[:, 1] += dy
    output_obj.append(patches.Polygon(corner_points, fc='green'))
    output_obj.append(patches.Polygon(hull_points, fc='yellow'))
    # corner_points_2, hull_points 是最终坐标，然后通过新的坐标
    for p in output_obj:
        ax.add_patch(p)
    plt.gca().set_aspect('equal')
    plt.title('Rate')
    plt.show()


