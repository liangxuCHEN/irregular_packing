# coding=utf8
import dxfgrabber


def find_shape_from_dxf(file_name):
    dxf = dxfgrabber.readfile(file_name)
    all_shapes = list()
    new_polygon = dict()
    for e in dxf.entities:
        if e.dxftype == 'LINE':
            # print (e.start, e.end)
            # 找封闭的多边形
            # 线条不按顺序画
            end_key = '{}x{}'.format(e.end[0], e.end[1])
            star_key = '{}x{}'.format(e.start[0], e.start[1])
            if new_polygon.has_key(end_key):
                # 找到闭合的多边形
                new_polygon[end_key].append([e.start[0], e.start[1]])
                all_shapes.append(new_polygon[end_key])
                new_polygon.pop(end_key)
                continue

            # 开始和结束点转换
            if new_polygon.has_key(star_key):
                # 找到闭合的多边形
                new_polygon[star_key].append([e.end[0], e.end[1]])
                all_shapes.append(new_polygon[star_key])
                new_polygon.pop(star_key)
                continue

            # 找连接的点
            has_find = False
            for key, points in new_polygon.items():
                if points[-1][0] == e.start[0] and points[-1][1] == e.start[1]:
                    new_polygon[key].append([e.end[0], e.end[1]])
                    has_find = True
                    break
                if points[-1][0] == e.end[0] and points[-1][1] == e.end[1]:
                    new_polygon[key].append([e.start[0], e.start[1]])
                    has_find = True
                    break

            if not has_find:
                new_polygon['{}x{}'.format(
                    e.start[0], e.start[1])] = [[e.start[0], e.start[1]], [e.end[0], e.end[1]]]

                # if e.dxftype == 'LWPOLYLINE':
                #     print (e.points)
                # if e.dxftype == 'CIRCLE':
                #     print (e.center, e.radius)
                # if e.dxftype == 'ARC':
                #     print (e.center, e.radius, e.start_angle, e.end_angle)
    return all_shapes


if __name__ == '__main__':
    s = find_shape_from_dxf('f4.dxf')
    print(s)
    print len(s)
