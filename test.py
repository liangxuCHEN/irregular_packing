# coding=utf8
from element import Element, Point
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from PIL import Image
from read_dxf import find_shape_from_dxf
from min_rectangle_area import min_area_tools
from min_retange import min_rectangle_alog


bin_data = None

# def fitness(shape):
#     # 找空白地方
#     begin_point = Point(0, 0)
#     has_place = True
#     while has_place:
#         tmp_place = bin_data[begin_point.x:begin_point.x + shape.pic_width, begin_point.y:begin_point.y + shape.pic_height]
#         tmp_place = tmp_place + shape
#         if tmp_place.max() > 1:
#             # 有覆盖
#             begin_point
#             continue



# def packing_bin(shape):
#     for i in range(0, shape.pic_width):
#         for j in range(0, shape.pic_height):
#             if star.matrix_data[i, j] == 0:
#                 bin_data.itemset(i + star.x, j + star.y, 0)


def matrix_to_image(data):
    """
    矩阵转为图片，im.show() 查看图片
    :return:
    """
    data = data * 255
    new_im = Image.fromarray(data.astype(np.uint8))
    return new_im


def output_res(all_rects):
    rects = list()
    all_positions = list()
    # print bins_list
    is_new_bin = 0
    for rect in all_rects:
        b, x, y, w, h, rid = rect
        if b == is_new_bin:
            rects.append((x, y, w, h))
        else:
            is_new_bin = b
            all_positions.append(rects)
            rects = list()
            rects.append((x, y, w, h))

    all_positions.append(rects)
    return all_positions


if __name__ == '__main__':
    # filename = 'img/c1.png'
    # shape_1 = Element(0, 0, 'img/c1.png')
    # shape_2 = Element(0, 0, 'img/cube.png')
    # shape_3 = Element(0, 0, 'img/star.png')
    # current_point = Point(0, 0)
    # star.rotate(rotate=270)
    # star.matrix_to_image().show()
    # star.rotate(rotate=180)
    # star.matrix_to_image().show()
    # print star.get_area()

    # input bin
    bin_data = np.zeros((1000, 1000))

    # 图形列表
    # percentage = 0
    # shape_list = [shape_1, shape_2, shape_3]
    # shape_id = 0
    # while len(shape_list) > 0:
    #     # 先填1/3地方 按照矩形BL放置
    #     if percentage < 33:
    #         alog_bl()
    shapes = find_shape_from_dxf('f3.dxf')

    fig = plt.figure()
    ax = plt.axes()
    ax.set_xlim(-10, 20)
    ax.set_ylim(-10, 20)
    output_obj = list()
    print shapes
    for s in shapes:
        width, height, hull_points, areas = min_area_tools.min_rectangle(s)
        output_obj.append(patches.Polygon(hull_points, fc='green'))
    # corner_points_2, hull_points 是最终坐标，然后通过新的坐标
    for p in output_obj:
        ax.add_patch(p)
    plt.gca().set_aspect('equal')
    plt.title('Rate')
    plt.show()
