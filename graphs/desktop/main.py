import os
import sys

import matplotlib.pyplot

from PyQt5 import uic
from PyQt5.Qt import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap

def visualize(graph_type):
    os.system("rm graph.png")
    if graph_type.draw_function:
        coords = open("../solver/function_coords", "r")

        xy = coords.read().split()
        coords.close()
        x = [float(xy[i]) for i in range(0, len(xy), 2)]
        y = [float(xy[i + 1]) for i in range(0, len(xy), 2)]

        if graph_type.draw_points:
            matplotlib.pyplot.scatter(x, y, c = 'red', linewidths = 2)
        matplotlib.pyplot.plot(x, y, c = 'red', label = 'function')

    if graph_type.draw_integral:
        coords = open("../solver/integral_coords", "r")

        xy = coords.read().split()
        coords.close()
        x = [float(xy[i]) for i in range(0, len(xy), 2)]
        y = [float(xy[i + 1]) for i in range(0, len(xy), 2)]

        if graph_type.draw_points:
            matplotlib.pyplot.scatter(x, y, c = 'green', linewidths = 2)
        matplotlib.pyplot.plot(x, y, c = 'green', label = 'integral')

    if graph_type.draw_derivative:
        coords = open("../solver/derivative_coords", "r")

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
        self.type = 0
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

    def to_string(self):
        return f"{int(self.draw_function == True)}{int(self.draw_integral == True)}{int(self.draw_derivative == True)}"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        os.system("./compile_solver.sh")
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
        self.slider_h.setValue(int(self.function_params.h * 100))

        self.power_function_radio_button.toggled.connect(self.draw_graph)
        self.exponential_function_radio_button.toggled.connect(self.draw_graph)

        self.points_check_box.toggled.connect(self.draw_graph)
        self.function_check_box.toggled.connect(self.draw_graph)
        self.integral_check_box.toggled.connect(self.draw_graph)
        self.derivative_check_box.toggled.connect(self.draw_graph)

        self.slider_n.valueChanged.connect(lambda: self.change_slider('n', self.slider_n.value()))
        self.slider_c.valueChanged.connect(lambda: self.change_slider('c', self.slider_c.value()))
        self.slider_a.valueChanged.connect(lambda: self.change_slider('a', self.slider_a.value()))
        self.slider_b.valueChanged.connect(lambda: self.change_slider('b', self.slider_b.value()))
        self.slider_h.valueChanged.connect(lambda: self.change_slider('h', self.slider_h.value()))

        self.n_spin_box.valueChanged.connect(lambda: self.change_spin_box('n', self.n_spin_box.value()))
        self.c_spin_box.valueChanged.connect(lambda: self.change_spin_box('c', self.c_spin_box.value()))
        self.a_spin_box.valueChanged.connect(lambda: self.change_spin_box('a', self.a_spin_box.value()))
        self.b_spin_box.valueChanged.connect(lambda: self.change_spin_box('b', self.b_spin_box.value()))
        self.h_spin_box.valueChanged.connect(lambda: self.change_spin_box('h', self.h_spin_box.value()))

        self.draw_graph()

    def change_slider(self, name, value):
        if name == 'n':
            self.n_spin_box.setValue(value / 10)
        if name == 'c':
            self.c_spin_box.setValue(value / 10)
        if name == 'a':
            self.a_spin_box.setValue(value / 10)
        if name == 'b':
            self.b_spin_box.setValue(value / 10)
        if name == 'h':
            self.h_spin_box.setValue(value / 10)
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
            if value > 11:
                new_value = 110
            self.slider_h.setValue(int(new_value))
        self.draw_graph()

    def draw_graph(self):
        self.function_params.type = 0 if self.power_function_radio_button.isChecked() else 1
        self.function_params.n = float(self.n_spin_box.value())
        self.function_params.c = float(self.c_spin_box.value())
        self.function_params.a = float(self.a_spin_box.value())
        self.function_params.b = float(self.b_spin_box.value())
        self.function_params.h = float(self.h_spin_box.value())

        self.graph_type.draw_points = self.points_check_box.isChecked()
        self.graph_type.draw_function = self.function_check_box.isChecked()
        self.graph_type.draw_integral = self.integral_check_box.isChecked()
        self.graph_type.draw_derivative = self.derivative_check_box.isChecked()

        os.system(f"./run_solver.sh {self.function_params.type} {self.graph_type.to_string()} {self.function_params.n} {self.function_params.c} {self.function_params.a} {self.function_params.b} {self.function_params.h}")

        visualize(self.graph_type)

        self.graph = QPixmap('graph.png')
        self.graph_label.setPixmap(self.graph)

app = QApplication(sys.argv)

main = MainWindow()
main.show()

sys.exit(app.exec_())
