# coding=utf8


class BinFactory(object):

    def __init__(self, width, height, border):
        self._width = width
        self._height = height
        self._border = border
        self._count = 0
        self._ref_bin = None

    def _creat_bin(self):
        return self._pack_algo

    def number_use(self):
        return self._count

    def fitness(self, shape):
        if not self._ref_bin:
            self._ref_bin = self._create_bin()

    def new_bin(self):
        self._count += 1
        return self._create_bin()
