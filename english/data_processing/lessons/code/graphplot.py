#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
    Draw time series from csv files or lists

    Data series come from the columns of the csv files multi columns can be used from
    the same file. One column for x values (it can be numerical or date/time data) and
    more columns for y1, y2, .., yn. Alternatively lists can be given with the values.
    As many charts will be drawn as many y columns given.
    If more input files are given multiple lines will be drawn in the same subfigure.
    It is poissible to define different number of y columns for the input csv files.
    The input csv files may have different number of rows and columns. column indeces are
    zero based.
    The data series are given by a list with maximum 6 elementst
    1st the name of the csv file separated by ';' and
        list of column ordinal numbers first is for x, the followings are for y values
        (0 base index), the same column can be repeated
        x column can be numerical or date/time, y columns are numerical
        or complex list [ x1, [y11, y12], x2, [y21 y22]]
    2nd list of multipliers for the columns, default 1 for each column
    3rd list of offsets for the columns, default 0 for each column
    4th list of simple format specifiers for y values, default is matplotlib defaults
    5th list of legend labels for y values, default filename:column

    Here is a simple example with three input files and two subplots

    first.csv:
    1;0.34;2.56
    2;0.58;1.43
    3;1.02;1.1

    second.csv:
    A;1.2;0.86;0.55;6.54
    B;1.9;1.7;0.72;5.78
    C;2.4;1.45;0.4;1.34
    D;2.8;0.86;.88;5.12

    third.csv
    1;0.75;1.8
    2;2.1;2.5
    3;1.8;3.1

    titles = ["line1", "line2", "points"]
    units = ["m", "mm", "degree"]
    data_series = [[['first.csv', [0, 1, 2]], [1, 1, 0.56], [0, 0, 0], ['g--', 'r'], ['l1', 'l2']],
                   [['second.csv', [1, 3, 2]], [1, 1, 1], [0, 0, 0], ['', ''], ['b1', 'b2']],
                   [['third.csv', [0, 2]], [1, 0.75], [0, -0.3], ['b+']]]
    g = GraphPlot(titles, units, data_series)
    g.draw()

"""
import csv
import os.path
import re
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np

class GraphPlot:
    """ class to plot a graph

        :param titles: list of titles for subplots
        :param units: units for aces
        :param data_series: list of list of titles, units and for each data file, filename  column numbers, scales, offsets, formats, labels; scales, offset, formats and labels are optional
    """
    SEPARATOR = ";" # update for your input

    def __init__(self, titles, units, data_series):
        """ initialize instance """
        self.titles = titles
        self.units = units
        self.x = []
        self.y = []
        self.fmts = []
        self.labels = []
        for serie in data_series:
            scales = [1] * len(serie[0][1])    # default scales
            if len(serie) > 1:
                scales = serie[1]
            offsets = [0] * len(serie[0][1])   # default offsets
            if len(serie) > 2:
                offsets = serie[2]
            if isinstance(serie[0][0], str):
                act_x, act_y = self.load(serie[0][0], serie[0][1], scales, offsets)
            else:
                act_x = serie[0][0]
                act_y = serie[0][1]
            self.x.append(act_x)
            self.y.append(act_y)
            fmt = [''] * len(serie[0][1])      # default formats
            if len(serie) > 3:
                fmt = serie[3]
            if isinstance(serie[0][0], str):
                label = ["{}:{}".format(serie[0][0], str(col))
                         for col in serie[0][1][1:]]
            else:
                label = [str(col+1) for col in range(len(serie[1][1:]))]
            if len(serie) > 4:
                label = serie[4]
            self.labels.append(label)
            self.fmts.append(fmt)
        try:
            self.main_title, _ = os.path.splitext(os.path.basename(data_series[0][0]))
        except Exception:
            self.main_title, _ = os.path.splitext(os.path.basename(__file__))

    def draw(self):
        """ draw multi graph """
        rows = max([len(yi) for yi in self.y])
        fig = plt.figure()
        fig.canvas.set_window_title(self.main_title)
        for ind in range(rows):
            ax = plt.subplot(rows, 1, ind+1)
            for i in range(len(self.x)):
                if len(self.y[i]) > ind:
                    if isinstance(self.x[i][0], datetime):
                        plt.plot_date(self.x[i], self.y[i][ind], self.fmts[i][ind],
                                      label=self.labels[i][ind])
                    else:
                        plt.plot(self.x[i], self.y[i][ind], self.fmts[i][ind],
                                 label=self.labels[i][ind])
            plt.xticks(rotation=45)
            plt.xlabel(self.units[0])
            plt.ylabel(self.units[ind+1])
            plt.grid()
            plt.legend()
            ax.set_title(self.titles[ind])
        fig.tight_layout()
        plt.show()
        fig.savefig(self.main_title + '.png')

    @staticmethod
    def load(fname, cols, scales, offsets):
        """ load input data

            :param fname: name of csv input file
            :param cols: ordinal column numbers to use
            :param scales: multipliers for columns
            :param offsets: offsets for columns
            :returns tuple x and y values (multiple y series as list)
        """
        data = []
        with open(fname, newline='') as f:
            reader = csv.reader(f, delimiter=GraphPlot.SEPARATOR)
            for row in reader:
                data.append(row)
        if re.match("[0-9]{4}-[0-9]{2}-[0-9]{2}", data[0][cols[0]]):
            x = [datetime.strptime(row[cols[0]], '%Y-%m-%d %H:%M:%S.%f')
                 for row in data]
        else:
            x = [float(row[cols[0]]) * scales[0] + offsets[0] for row in data]
        y = []
        for i in range(1, len(cols)):
            y.append([float(row[cols[i]]) * scales[i] + offsets[i] for row in data])
        return (x, y)

if __name__ == "__main__":
    from sys import argv
    from math import (sin, cos, pi)

    DEMO_ID = 1
    if len(argv) > 1:
        DEMO_ID = int(argv[1])
    if DEMO_ID == 1:
        TITLES = ["line1", "line2", "points"]
        UNITS = ["m", "mm", "degree", "m"]
        X1 = [1, 2, 3, 4, 5, 6]
        Y11 = [0.34, 0.58, 1.02, 1.21, 1.52, 1.61]
        Y12 = [2.56, 1.43, 1.1, 0.8, 0.48, 0.67]
        X2 = [1.2, 1.9, 2.4, 2.8, 3.5, 5.8]
        Y21 = [0.86, 1.7, 1.45, 0.86, 1.2, 3.0]
        Y22 = [0.55, 0.72, 0.4, 0.88, 0.99, 2.0]
        # x3 == x1
        Y31 = [1.8, 2.5, 3.1, 2.6, 2.3, 2.8]
        DATA_SERIES = [[[X1, [Y11, Y12, Y12]],
                        [1, 1, 0.56, 1], [0, 0, 0, 1],
                        ['g--', 'r', 'ro'], ['l1', 'l2', 'l2']],
                       [[X2, [Y22, Y21, Y22]],
                        [1, 1, 1, 0.75], [0, 0, 0, -0.5],
                        ['', '', 'yx'], ['b1', 'b2', 'b1']],
                       [[X1, [Y31]], [1, 0.75], [0, -0.3], ['b+']]]
        G = GraphPlot(TITLES, UNITS, DATA_SERIES)
        G.draw()
    elif DEMO_ID == 2:
        TITLES = ["trigonometry"]
        UNITS = ["fok", "-", "-"]
        DATA_SERIES = [[['test/sin_cos.csv', [0, 2]], [1, 1], [0, 0],
                        [''], ['sin']],
                       [['test/sin_cos.csv', [0, 3]], [1, 1], [0, 0],
                        [''], ['cos']]]
        G = GraphPlot(TITLES, UNITS, DATA_SERIES)
        G.draw()
    elif DEMO_ID == 3:
        TITLES = ["trigonometry"]
        UNITS = ["fok", "-", "-"]
        X = list(range(0, 370, 10))
        Y1 = [sin(xi / 180 * pi) for xi in range(0, 370, 10)]
        Y2 = [cos(xi / 180 * pi) for xi in range(0, 370, 10)]
        DATA_SERIES = [[[X, [Y1]], [0, 2], [1, 1], [0, 0],
                        [''], ['sin']],
                       [[X, [Y2]], [0, 3], [1, 1], [0, 0],
                        [''], ['cos']]]
        G = GraphPlot(TITLES, UNITS, DATA_SERIES)
        G.draw()
