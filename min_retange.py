# coding=utf8
from packer import newPacker
import packer as packer
from maxrects import MaxRectsBl

from my_rectpack_lib import base_tools
from min_rectangle_area.min_area_tools import *

from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.patches as patches

from read_dxf import find_shape_from_dxf


def output_res(all_rects):
    rects = list()
    all_positions = list()
    # print bins_list
    is_new_bin = 0
    for rect in all_rects:
        b, x, y, w, h, rid = rect
        if b == is_new_bin:
            rects.append((x, y, w, h, rid))
        else:
            is_new_bin = b
            all_positions.append(rects)
            rects = list()
            rects.append((x, y, w, h, rid))

    all_positions.append(rects)
    return all_positions


def roting(rot_angle, points):
    # 旋转矩阵
    R = array([[math.cos(rot_angle), math.cos(rot_angle - (math.pi / 2))],
               [math.cos(rot_angle + (math.pi / 2)), math.cos(rot_angle)]])
    rot_points = dot(R, transpose(points))  # 2x2 * 2xn
    return transpose(rot_points)


def calc_use_rate(position, shape_data, bin_data):
    # 计算利用率
    total_use = 0
    for p in position:
        total_use += shape_data[p[4]]['areas']
    return float(int(total_use / (bin_data[0] * bin_data[1]) * 10000)) / 10000


def draw_irregular_pic(positions, rates, width=None, height=None, path=None, border=0, num_list=None,
                 shapes=None, empty_positions=None, title=None, bins_list=None):
    # 多个图像需要处理

    if shapes is not None:
        if num_list is None:
            # 返回唯一的排版列表，以及数量
            num_list = base_tools.find_the_same_position(positions)

    else:
        # 单个图表
        num_list = [1]

    i_p = 0  # 记录板材索引
    i_pic = 1  # 记录图片的索引
    num = len(base_tools.del_same_data(num_list, num_list))
    fig_height = num * 4
    fig1 = Figure(figsize=(8, fig_height))
    # 使用中文
    # path_ttc = os.path.join(settings.BASE_DIR, 'static')
    # path_ttc = os.path.join(path_ttc, 'simsun.ttc')
    # font_set = FontProperties(fname=path_ttc, size=12)

    if title is not None:
        fig1.suptitle(title, fontweight='bold')
    FigureCanvas(fig1)

    for position in positions:
        if num_list[i_p] != 0:
            ax1 = fig1.add_subplot(num, 1, i_pic, aspect='equal')
            i_pic += 1
            ax1.set_title('rate: %s, piece: %d' % (str(rates[i_p]), num_list[i_p]))
            output_obj = list()
            p_id = list()
            for v in position:
                output_obj.append(
                    patches.Rectangle((v[0], v[1]), v[2], v[3], edgecolor='black', lw=border, facecolor='none'))
                p_id.append(v[4])

            if empty_positions is not None:
                for em_v in empty_positions[i_p]:
                    output_obj.append(
                        patches.Rectangle(
                            (em_v[0], em_v[1]), em_v[2], em_v[3], edgecolor='black',
                            lw=border, hatch='/', facecolor='none'))
                    p_id.append('-1')

            index_p = 0
            for p in output_obj:
                # 显示矩形外框
                # ax1.add_patch(p)
                # 计算显示位置
                if shapes is not None:
                    rx, ry = p.get_xy()
                    cx = rx + p.get_width() / 2.0
                    cy = ry + p.get_height() / 2.0
                    # 找到对应的序号
                    # 找到对应的多边形,然后求对应的坐标变换
                    # print shapes[p_id[index_p]]['rectangle'],  p.get_width(),  p.get_height()
                    if shapes[p_id[index_p]]['rectangle'][0] == p.get_width():
                        corner_points = [[x+rx+p.get_width(), y+ry] for x, y in shapes[p_id[index_p]]['points']]
                    else:
                        tmp_points = roting(pi/2, shapes[p_id[index_p]]['points'])
                        corner_points = [[x + rx, y + ry] for x, y in tmp_points]

                    ax1.add_patch(patches.Polygon(corner_points, edgecolor='green',
                                                  lw=border, facecolor='none'))
                    # 标记尺寸
                    shape_label = "({p_id}){width}x{height}".format(
                        p_id=index_p, width=p.get_width(), height=p.get_height())

                    rotation = 0
                    if p.get_width() < 450:
                        if p.get_height() > 450 and p.get_width() > 50:
                            rotation = 90
                        else:
                            shape_label = p_id[index_p]
                    elif p.get_height() < 50:
                        shape_label = p_id[index_p]

                    ax1.annotate(shape_label, (cx, cy), color='black', weight='bold',
                                 fontsize=8, ha='center', va='center', rotation=rotation)
                index_p += 1

            # 坐标长度
            if width is not None and height is not None:
                ax1.set_xlim(0, width)
                ax1.set_ylim(0, height)
            elif bins_list is not None:
                ax1.set_xlim(0, bins_list[i_p][0])
                ax1.set_ylim(0, bins_list[i_p][1])
            else:
                ax1.set_xlim(0, 2430)
                ax1.set_ylim(0, 1210)

        i_p += 1

    if path is not None:
        fig1.savefig('%s.png' % path)
    else:
        fig1.show()


def min_rectangle_alog(shapes=None, bin_data=None, path=None, dxf_file=None):
    """
    用最小矩形替代多边形，进行排料，优点是快速和简单，缺点是利用率不高, 适用于凸多边形
    :param path:
    :param shapes: {'0':{'rectangle':(100, 200), 'points': [[15,20], [10, 25]]}}
    :param bin_data: (width, height)
    :return:
    """
    # 图形生成
    if shapes is None:
        shapes = dict()
        if dxf_file is None:
            for i in range(0, 10):
                # 随机生成多边形
                xy_points = 50 * random.random((7, 2))
                width, height, hull_points, areas = min_rectangle(xy_points)
                shapes[str(i)] = {'rectangle': (width, height), 'points': hull_points, 'areas': areas}
            for i in range(10, 20):
                # 随机生成多边形
                xy_points = 80 * random.random((15, 2))
                width, height, hull_points, areas = min_rectangle(xy_points)
                shapes[str(i)] = {'rectangle': (width, height), 'points': hull_points, 'areas': areas}
            for i in range(20, 30):
                # 随机生成多边形
                xy_points = 160 * random.random((25, 2))
                width, height, hull_points, areas = min_rectangle(xy_points)
                shapes[str(i)] = {'rectangle': (width, height), 'points': hull_points, 'areas': areas}
        else:
            # 从dxf文件中提取数据
            datas = find_shape_from_dxf(dxf_file)
            for i in range(0, len(datas)):
                width, height, hull_points, areas = min_rectangle(datas[i])
                shapes[str(i)] = {'rectangle': (width, height), 'points': hull_points, 'areas': areas}

    my_pack = newPacker(
        bin_algo=packer.PackingBin.BBF,
        pack_algo=MaxRectsBl,
        sort_algo=packer.SORT_AREA,
        rotation=True,
    )

    for key, r in shapes.items():
        my_pack.add_rect(r['rectangle'][0], r['rectangle'][1], rid=key)

    # 板材尺寸
    if bin_data is None:
        bin_data = (500, 500)

    my_pack.add_bin(bin_data[0], bin_data[1], 100)
    my_pack.pack()
    # 返回矩形，坐标点
    solution = output_res(my_pack.rect_list())
    same_bin_list = base_tools.find_the_same_position(solution)
    rate = []
    for s in solution:
        rate.append(calc_use_rate(s, shapes, bin_data))

    if path is None:
        path = 'example'

    draw_irregular_pic(solution, rate, shapes=shapes, width=bin_data[0],
                       height=bin_data[1], path=path, border=1, num_list=same_bin_list)


if __name__ == '__main__':
    min_rectangle_alog(dxf_file='f6.dxf', bin_data=(60, 50), path='dxf_example_6')
    # min_rectangle_alog()
