# coding=utf8

from my_irregular_lib.read_dxf import find_shape_from_dxf
from Polygon import Polygon
from Polygon.IO import writeSVG
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import math


def test_polygon(dxf_file):
    # 从dxf文件中提取数据
    datas = find_shape_from_dxf(dxf_file)
    shapes = list()

    for i in range(0, len(datas)):
        p = Polygon()
        shapes.append(p)
        p.addContour(datas[i])
        p.shift(0,10)
        x, y = p.center()
        p.rotate(math.pi, x, y)
    return shapes


def draw_polygon(shapes):
    ax = plt.axes()
    ax.set_xlim(-10, 150)
    ax.set_ylim(-10, 150)
    output_obj = list()
    for s in shapes:
        print s.contour(0)
        # x, y ,w, h =  s.boundingBox()
        # output_obj.append(patches.Rectangle((x, y), w, h, fc='green'))
        output_obj.append(patches.Polygon(s.contour(0), fc='yellow'))
    # corner_points_2, hull_points 是最终坐标，然后通过新的坐标
    for p in output_obj:
        ax.add_patch(p)
    plt.gca().set_aspect('equal')
    plt.title('Rate')
    plt.show()

if __name__ == '__main__':
    s = test_polygon('f6.dxf')
    writeSVG('Operations.svg', s, width=600)
    draw_polygon(s)
