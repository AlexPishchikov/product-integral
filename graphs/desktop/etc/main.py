import os
import sys
import math

from math import sin as sin
from math import cos as cos
from math import tan as tan

from math import sinh as sinh
from math import cosh as cosh
from math import tanh as tanh

from math import asin as asin
from math import acos as acos
from math import atan as atan

from math import asinh as asinh
from math import acosh as acosh
from math import atanh as atanh

from math import log as ln

import matplotlib.pyplot

from PyQt5 import uic
from PyQt5.Qt import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap

def calculate(function_params):
    i = function_params.a
    coords = open("function_coords", "w")
    while i < function_params.b:
        x = i
        c = function_params.c
        n = function_params.n
        coords.write(f"{i} {eval(function_params.function)}\n")
        i += function_params.h
    coords.close()

    i = function_params.a
    result = 1.0
    coords = open("integral_coords", "w")
    while i < function_params.b:
        x = i
        c = function_params.c
        n = function_params.n
        result *= eval(function_params.function)
        print("%.10f %.10f" % (i, result), file = coords)
        i += function_params.h
    coords.close()

    i = function_params.a
    coords = open("derivative_coords", "w")
    while i < function_params.b:
        x = i
        c = function_params.c
        n = function_params.n
        f = eval(function_params.function)

        x = i + function_params.h
        fh = eval(function_params.function)
        result = (fh / f) ** (1 / function_params.h)
        print("%.10f %.10f" % (i, result), file = coords)
        i += function_params.h
    coords.close()


def visualize(graph_type):
    os.system("rm graph.png")
    if graph_type.draw_function:
        coords = open("function_coords", "r")

        xy = coords.read().split()
        coords.close()
        x = [float(xy[i]) for i in range(0, len(xy), 2)]
        y = [float(xy[i + 1]) for i in range(0, len(xy), 2)]

        if graph_type.draw_points:
            matplotlib.pyplot.scatter(x, y, c = 'red', linewidths = 2)
        matplotlib.pyplot.plot(x, y, c = 'red', label = 'function')

    if graph_type.draw_integral:
        coords = open("integral_coords", "r")

        xy = coords.read().split()
        coords.close()
        x = [float(xy[i]) for i in range(0, len(xy), 2)]
        y = [float(xy[i + 1]) for i in range(0, len(xy), 2)]

        if graph_type.draw_points:
            matplotlib.pyplot.scatter(x, y, c = 'green', linewidths = 2)
        matplotlib.pyplot.plot(x, y, c = 'green', label = 'integral')

    if graph_type.draw_derivative:
        coords = open("derivative_coords", "r")

        xy = coords.read().split()
        coords.close()
        x = [float(xy[i]) for i in range(0, len(xy), 2)]
        y = [float(xy[i + 1]) for i in range(0, len(xy), 2)]

        if graph_type.draw_points:
            matplotlib.pyplot.scatter(x, y, c = 'blue', linewidths = 2)
        matplotlib.pyplot.plot(x, y, c = 'blue', label = 'derivative')

    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig('graph.png')
    matplotlib.pyplot.close()


class Function_params:
    def __init__(self):
        self.function = "nx + C"
        self.n = 1.0
        self.c = 1.0
        self.a = 1.0
        self.b = 3.0
        self.h = 0.03

class Graph_type:
    def __init__(self):
        self.draw_function = True
        self.draw_integral = True
        self.draw_derivative = True
        self.draw_points = False


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/main.ui', self)
        self.setFixedSize(self.size())
        self.graph = QPixmap('graph.png')
        self.graph_label.setPixmap(self.graph)

        self.function_params = Function_params()
        self.graph_type = Graph_type()

        self.slider_n.setValue(int(self.function_params.n * 10))
        self.slider_c.setValue(int(self.function_params.c * 10))
        self.slider_a.setValue(int(self.function_params.a * 10))
        self.slider_b.setValue(int(self.function_params.b * 10))
        self.slider_h.setValue(int(self.function_params.h * 110))

        self.points_check_box.toggled.connect(self.draw_graph)
        self.function_check_box.toggled.connect(self.draw_graph)
        self.integral_check_box.toggled.connect(self.draw_graph)
        self.derivative_check_box.toggled.connect(self.draw_graph)

        self.slider_n.valueChanged.connect(lambda: self.change_slider('n', self.slider_n.value()))
        self.slider_c.valueChanged.connect(lambda: self.change_slider('c', self.slider_c.value()))
        self.slider_a.valueChanged.connect(lambda: self.change_slider('a', self.slider_a.value()))
        self.slider_b.valueChanged.connect(lambda: self.change_slider('b', self.slider_b.value()))
        self.slider_h.valueChanged.connect(lambda: self.change_slider('h', self.slider_h.value()))

        self.spin_box_n.valueChanged.connect(lambda: self.change_spin_box('n', self.spin_box_n.value()))
        self.spin_box_c.valueChanged.connect(lambda: self.change_spin_box('c', self.spin_box_c.value()))
        self.spin_box_a.valueChanged.connect(lambda: self.change_spin_box('a', self.spin_box_a.value()))
        self.spin_box_b.valueChanged.connect(lambda: self.change_spin_box('b', self.spin_box_b.value()))
        self.spin_box_h.valueChanged.connect(lambda: self.change_spin_box('h', self.spin_box_h.value()))

        self.draw_graph()

    def change_slider(self, name, value):
        if name == 'n':
            self.spin_box_n.setValue(value / 10)
        if name == 'c':
            self.spin_box_c.setValue(value / 10)
        if name == 'a':
            self.spin_box_a.setValue(value / 10)
        if name == 'b':
            self.spin_box_b.setValue(value / 10)
        if name == 'h':
            self.spin_box_h.setValue(value / 110)
        self.draw_graph()

    def change_spin_box(self, name, value):
        new_value = value * 10
        if value > 10:
            new_value = 100
        if value < -10:
            new_value -100
        if name == 'n':
            self.slider_n.setValue(int(new_value))
        if name == 'c':
            self.slider_c.setValue(int(new_value))
        if name == 'a':
            self.slider_a.setValue(int(new_value))
        if name == 'b':
            self.slider_b.setValue(int(new_value))
        if name == 'h':
            new_value *= 11
            if (value * 11) > 110:
                new_value = 110
            self.slider_h.setValue(int(new_value))
        self.draw_graph()

    def draw_graph(self):
        self.function_params.function = self.function_line_edit.text().lower()
        self.function_params.n = float(self.spin_box_n.value())
        self.function_params.c = float(self.spin_box_c.value())
        self.function_params.a = float(self.spin_box_a.value())
        self.function_params.b = float(self.spin_box_b.value())
        self.function_params.h = float(self.spin_box_h.value())

        self.graph_type.draw_points = self.points_check_box.isChecked()
        self.graph_type.draw_function = self.function_check_box.isChecked()
        self.graph_type.draw_integral = self.integral_check_box.isChecked()
        self.graph_type.draw_derivative = self.derivative_check_box.isChecked()

        calculate(self.function_params)
        visualize(self.graph_type)

        self.graph = QPixmap('graph.png')
        self.graph_label.setPixmap(self.graph)

app = QApplication(sys.argv)

main = MainWindow()
main.show()

sys.exit(app.exec_())