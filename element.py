# coding=utf8
from PIL import Image
import numpy as np
from math import sqrt


class Element(object):
    """
    Basic element class
    """

    def __init__(self, x, y, file_name, rate_per_pixel=0.85):

        # 电脑72dpi   1厘米=28.346像素  转换毫米单位 R = 0.35
        # 相片300dp   1厘米=118.11像素  转换毫米单位 R = 0.85
        self._rate_per_pixel = rate_per_pixel
        self._file_name = file_name
        self.matrix_data = self._image_to_matrix()
        self.x = x
        self.y = y

    def _image_to_matrix(self):
        """
        用矩阵表示图形
        :return:
        """
        # 读取图片
        im = Image.open(self._file_name)
        self.pic_width, self.pic_height = im.size
        im = im.convert("1")
        data = im.getdata()
        data = np.matrix(data, dtype='float') / 255.0
        # new_data = np.reshape(data,(width,height))
        new_data = np.reshape(data, (self.pic_height, self.pic_width))

        # 找实际边框
        top_id = 0
        bottom_id = self.pic_height
        left_id = 0
        right_id = self.pic_width
        print top_id, left_id, bottom_id, right_id
        for i in range(0, self.pic_height):
            if max(new_data.A[i]) == 1:
                top_id = i
                break

        for i in range(0, self.pic_height)[::-1]:
            if max(new_data.A[i]) == 1:
                bottom_id = i
                break

        for i in range(0, self.pic_width):
            if max(new_data.T.A[i]) == 1:
                left_id = i
                break

        for i in range(0, self.pic_width)[::-1]:
            if max(new_data.T.A[i]) == 1:
                right_id = i
                break

        data = new_data.A[top_id:bottom_id, left_id:right_id]
        # 重新生成
        print top_id, left_id, bottom_id, right_id
        self.pic_height = bottom_id - top_id
        self.pic_width = right_id - left_id
        new_data = np.matrix(data)

        # 图形参数
        self.width = self.pic_width * self._rate_per_pixel
        self.height = self.pic_height * self._rate_per_pixel
        return new_data

    def matrix_to_image(self):
        """
        矩阵转为图片，im.show() 查看图片
        :return:
        """
        data = self.matrix_data * 255
        new_im = Image.fromarray(data.astype(np.uint8))
        return new_im

    def rotate(self, rotate=90):
        # 顺时针方向
        if rotate == 270:
            self.matrix_data = np.matrix(self.matrix_data.T.A)
        if rotate == 180:
            self.matrix_data = np.matrix(self.matrix_data.T[::-1].T.A)
        if rotate == 90:
            self.matrix_data = np.matrix(self.matrix_data[::-1])

    def get_overlap(self, other_shape):
        """
        Return the amount of overlap between two shapes. Depends on the type of
        shape self and other_shape are and calls the appropriate methods.
        :param other_shape:
        :return:
        """
        pass

    def __lt__(self, other):
        """
        Compare rectangles by area (used for sorting)
        """
        return self.area() < other.area()

    def get_area(self):
        data = self.matrix_data.A
        return np.sum(data==0) * self._rate_per_pixel ** 2

    def move(self, x, y):
        """
        Move self by dx in the x direction and by dy in the y direction.

        Arguments:
            x (int, float): X coordinate
            y (int, float): Y coordinate
        """
        self.x += x
        self.y += y

    def set_position(self, x, y):
        """
        Set the position to (x, y). The position is the upper left corner of
        the shape.
        x (int, float): X coordinate
        y (int, float): Y coordinate
        :return:
        """
        self.x = x
        self.y = y



    @property
    def bottom(self):
        """
        Rectangle bottom edge y coordinate
        """
        return self.y

    @property
    def top(self):
        """
        Rectangle top edge y coordiante
        """
        return self.y + self.height

    @property
    def left(self):
        """
        Rectangle left ednge x coordinate
        """
        return self.x

    @property
    def right(self):
        """
        Rectangle right edge x coordinate
        """
        return self.x + self.width

    @property
    def corner_top_l(self):
        return Point(self.left, self.top)

    @property
    def corner_top_r(self):
        return Point(self.right, self.top)

    @property
    def corner_bot_r(self):
        return Point(self.right, self.bottom)

    @property
    def corner_bot_l(self):
        return Point(self.left, self.bottom)


class Point(object):

    __slots__ = ('x', 'y')

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (self.x == other.x and self.y == other.y)

    def __repr__(self):
        return "P({}, {})".format(self.x, self.y)

    def distance(self, point):
        """
        Calculate distance to another point
        """
        return sqrt((self.x-point.x)**2+(self.y-point.y)**2)

    def distance_squared(self, point):
        return (self.x-point.x)**2+(self.y-point.y)**2

