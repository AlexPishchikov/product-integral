import os
import sys

from PyQt5 import uic
from PyQt5.Qt import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap

def run_solver(function_params, plot_type):
    os.system(f"./run_solver.sh {function_params.function} {plot_type.to_string()} {function_params.n} {function_params.c} {function_params.a} {function_params.b} {function_params.h} {function_params.max}")


class Function_params:
    def __init__(self):
        self.function = "x^3"
        self.n = 1.0
        self.c = 1.0
        self.a = 1.0
        self.b = 3.0
        self.h = 0.01
        self.max = 100000

class plot_type:
    def __init__(self):
        self.draw_points = False
        self.draw_function = True
        self.draw_integral = True
        self.draw_derivative = True

    def to_string(self):
        return f"{int(self.draw_points)}{int(self.draw_function)}{int(self.draw_derivative)}{int(self.draw_integral)}"


class MainWindow(QMainWindow):
    def __init__(self):
        os.system("./compile_solver.sh")
        super().__init__()
        uic.loadUi('ui/main.ui', self)
        self.setFixedSize(self.size())
        self.plot = QPixmap('../../solver/plot.svg')
        self.plot_label.setPixmap(self.plot)

        self.function_params = Function_params()
        self.plot_type = plot_type()

        self.slider_n.setValue(int(self.function_params.n * 10))
        self.slider_c.setValue(int(self.function_params.c * 10))
        self.slider_a.setValue(int(self.function_params.a * 10))
        self.slider_b.setValue(int(self.function_params.b * 10))
        self.slider_h.setValue(int(self.function_params.h * 110))

        self.points_check_box.toggled.connect(self.call_solver)
        self.function_check_box.toggled.connect(self.call_solver)
        self.integral_check_box.toggled.connect(self.call_solver)
        self.derivative_check_box.toggled.connect(self.call_solver)

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

        self.call_solver()

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
        self.call_solver()

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
        self.call_solver()

    def call_solver(self):
        self.function_params.function = '"' + self.function_line_edit.text().lower().replace(' ', '').replace(',', '.') + '"'
        self.function_params.n = float(self.spin_box_n.value())
        self.function_params.c = float(self.spin_box_c.value())
        self.function_params.a = float(self.spin_box_a.value())
        self.function_params.b = float(self.spin_box_b.value())
        self.function_params.h = float(self.spin_box_h.value())
        self.function_params.max = self.max_line_edit.text().lower().replace(' ', '').replace(',', '.')

        self.plot_type.draw_points = self.points_check_box.isChecked()
        self.plot_type.draw_function = self.function_check_box.isChecked()
        self.plot_type.draw_integral = self.integral_check_box.isChecked()
        self.plot_type.draw_derivative = self.derivative_check_box.isChecked()

        run_solver(self.function_params, self.plot_type)

        self.plot = QPixmap('../../solver/plot.svg')
        self.plot_label.setPixmap(self.plot)

app = QApplication(sys.argv)

main = MainWindow()
main.show()

sys.exit(app.exec_())
