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

        matplotlib.pyplot.scatter(x, y, c = 'red', label = 'function', linewidths = 2)
        matplotlib.pyplot.plot(x, y, c = 'red')

    if graph_type.draw_integral:
        coords = open("../solver/integral_coords", "r")

        xy = coords.read().split()
        coords.close()
        x = [float(xy[i]) for i in range(0, len(xy), 2)]
        y = [float(xy[i + 1]) for i in range(0, len(xy), 2)]


        matplotlib.pyplot.scatter(x, y, c = 'green', label = 'integral', linewidths = 2)
        matplotlib.pyplot.plot(x, y, c = 'green')

    if graph_type.draw_derivative:
        coords = open("../solver/derivative_coords", "r")

        xy = coords.read().split()
        coords.close()
        x = [float(xy[i]) for i in range(0, len(xy), 2)]
        y = [float(xy[i + 1]) for i in range(0, len(xy), 2)]

        matplotlib.pyplot.scatter(x, y, c = 'blue', label = 'derivative', linewidths = 2)
        matplotlib.pyplot.plot(x, y, c = 'blue')

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

        self.function_check_box.toggled.connect(self.draw_graph)
        self.integral_check_box.toggled.connect(self.draw_graph)
        self.derivative_check_box.toggled.connect(self.draw_graph)

        self.slider_n.valueChanged.connect(self.draw_graph)
        self.slider_c.valueChanged.connect(self.draw_graph)
        self.slider_a.valueChanged.connect(self.draw_graph)
        self.slider_b.valueChanged.connect(self.draw_graph)
        self.slider_h.valueChanged.connect(self.draw_graph)

        self.draw_graph()

    def draw_graph(self):
        self.function_params.type = 0 if self.power_function_radio_button.isChecked() else 1
        self.function_params.n = self.slider_n.value() / 10
        self.function_params.c = self.slider_c.value() / 10
        self.function_params.a = self.slider_a.value() / 10
        self.function_params.b = self.slider_b.value() / 10
        self.function_params.h = self.slider_h.value() / 100

        self.n_value_label.setText("n = " + str(self.slider_n.value() / 10))
        self.c_value_label.setText("c = " + str(self.slider_c.value() / 10))
        self.a_value_label.setText("a = " + str(self.slider_a.value() / 10))
        self.b_value_label.setText("b = " + str(self.slider_b.value() / 10))
        self.h_value_label.setText("h = " + str(self.slider_h.value() / 100))

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
