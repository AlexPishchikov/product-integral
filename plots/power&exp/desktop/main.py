import os
import sys

import matplotlib.pyplot

from PyQt5 import uic
from PyQt5.Qt import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap

def visualize(plot_type):
    os.system("if [ -f plot.png ]; then rm plot.png; fi;")
    if plot_type.draw_function:
        coords = open("../solver/function_coords", "r")

        xy = coords.read().split()
        coords.close()
        x = [float(xy[i]) for i in range(0, len(xy), 2)]
        y = [float(xy[i + 1]) for i in range(0, len(xy), 2)]

        if plot_type.draw_points:
            matplotlib.pyplot.scatter(x, y, c = 'red', linewidths = 2)
        matplotlib.pyplot.plot(x, y, c = 'red', label = 'function')

    if plot_type.draw_integral:
        coords = open("../solver/integral_coords", "r")

        xy = coords.read().split()
        coords.close()
        x = [float(xy[i]) for i in range(0, len(xy), 2)]
        y = [float(xy[i + 1]) for i in range(0, len(xy), 2)]

        if plot_type.draw_points:
            matplotlib.pyplot.scatter(x, y, c = 'green', linewidths = 2)
        matplotlib.pyplot.plot(x, y, c = 'green', label = 'integral')

    if plot_type.draw_derivative:
        coords = open("../solver/derivative_coords", "r")

        xy = coords.read().split()
        coords.close()
        x = [float(xy[i]) for i in range(0, len(xy), 2)]
        y = [float(xy[i + 1]) for i in range(0, len(xy), 2)]

        if plot_type.draw_points:
            matplotlib.pyplot.scatter(x, y, c = 'blue', linewidths = 2)
        matplotlib.pyplot.plot(x, y, c = 'blue', label = 'derivative')

    matplotlib.pyplot.legend()
    matplotlib.pyplot.savefig('plot.png')
    matplotlib.pyplot.close()


class Function_params:
    def __init__(self):
        self.type = 0
        self.n = 1.0
        self.c = 1.0
        self.a = 1.0
        self.b = 3.0
        self.h = 0.03

class Plot_type:
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
        self.plot = QPixmap('plot.png')
        self.plot_label.setPixmap(self.plot)

        self.function_params = Function_params()
        self.plot_type = Plot_type()

        self.slider_n.setValue(int(self.function_params.n * 10))
        self.slider_c.setValue(int(self.function_params.c * 10))
        self.slider_a.setValue(int(self.function_params.a * 10))
        self.slider_b.setValue(int(self.function_params.b * 10))
        self.slider_h.setValue(int(self.function_params.h * 110))

        self.power_function_radio_button.toggled.connect(self.draw_plot)
        self.exponential_function_radio_button.toggled.connect(self.draw_plot)

        self.points_check_box.toggled.connect(self.draw_plot)
        self.function_check_box.toggled.connect(self.draw_plot)
        self.integral_check_box.toggled.connect(self.draw_plot)
        self.derivative_check_box.toggled.connect(self.draw_plot)

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

        self.draw_plot()

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
        self.draw_plot()

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
        self.draw_plot()

    def draw_plot(self):
        self.function_params.type = 0 if self.power_function_radio_button.isChecked() else 1
        self.function_params.n = float(self.spin_box_n.value())
        self.function_params.c = float(self.spin_box_c.value())
        self.function_params.a = float(self.spin_box_a.value())
        self.function_params.b = float(self.spin_box_b.value())
        self.function_params.h = float(self.spin_box_h.value())

        self.plot_type.draw_points = self.points_check_box.isChecked()
        self.plot_type.draw_function = self.function_check_box.isChecked()
        self.plot_type.draw_integral = self.integral_check_box.isChecked()
        self.plot_type.draw_derivative = self.derivative_check_box.isChecked()

        os.system(f"./run_solver.sh {self.function_params.type} {self.plot_type.to_string()} {self.function_params.n} {self.function_params.c} {self.function_params.a} {self.function_params.b} {self.function_params.h}")

        visualize(self.plot_type)

        self.plot = QPixmap('plot.png')
        self.plot_label.setPixmap(self.plot)

app = QApplication(sys.argv)

main = MainWindow()
main.show()

sys.exit(app.exec_())
