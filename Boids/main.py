from functions import *

import time
from vispy import app, scene
from vispy.geometry import Rect

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QMainWindow, QSlider, QVBoxLayout, QWidget, QLabel, QCheckBox


class BoidsSimulation(QMainWindow):
    def __init__(self):
        super().__init__()
        self.wall_bounce_checkbox = None
        self.separation_slider = None
        self.cohesion_label = None
        self.alignment_label = None
        self.separation_label = None
        self.cohesion_slider = None
        self.alignment_slider = None

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # ========================================================
        width, height = 1920, 1080
        N = 5000
        self.delta_time = 0.01
        self.aspect_ratio = width / height
        self.perception = 1 / 20
        # self.coeffitients = {"separation": 1.5,
        #                      "cohesion": .03,
        #                      "alignment": .3,
        #                      "wall": 0.03
        #                      }
        #                             s    c     a    w
        self.coeffitients = np.array([.4, 15.0, 2.0, 0.3])

        self.velocity_range = (0.2, 0.5)
        self.acceleration_range = (0, 3)
        self.wall_bounce = False

        # (x,y), (vx, vy), (ax, ay)
        self.boids = np.zeros((N, 6), dtype=np.float64)
        init_boids(self.boids, self.aspect_ratio, self.velocity_range)
        # ========================================================

        self.canvas = scene.SceneCanvas(show=True, size=(width, height), parent=self.central_widget)
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.PanZoomCamera(rect=Rect(0, 0, self.aspect_ratio, 1))
        self.arrows = scene.Arrow(arrows=directions(self.boids, 0.1), arrow_color=(1, 1, 1, 1), arrow_size=5,
                                  connect='segments',
                                  parent=self.view.scene)

        self.create_sliders(layout, width, height)
        self.setLayout(layout)

        # Set up the timer and connect it to the update function
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def create_sliders(self, layout, width, height):
        self.separation_label = QLabel(self)
        self.separation_label.setText(f"Separation: {self.coeffitients[0]}")
        self.separation_slider = QSlider(Qt.Orientation.Horizontal)
        self.cohesion_label = QLabel(self)
        self.cohesion_label.setText(f"Cohesion: {self.coeffitients[1]}")
        self.cohesion_slider = QSlider(Qt.Orientation.Horizontal)
        self.alignment_label = QLabel(self)
        self.alignment_label.setText(f"Alignment: {self.coeffitients[2]}")
        self.alignment_slider = QSlider(Qt.Orientation.Horizontal)

        self.wall_bounce_checkbox = QCheckBox("Wall bounce", self)
        self.wall_bounce_checkbox.stateChanged.connect(self.wall_bounce_change)
        self.wall_bounce_checkbox.setChecked(False)

        self.separation_slider.setRange(0, 50)
        self.separation_slider.setValue(int(self.coeffitients[0]) * 10)
        self.separation_slider.valueChanged.connect(self.separation_change)

        self.cohesion_slider.setRange(0, 30)
        self.cohesion_slider.setValue(int(self.coeffitients[1]))
        self.cohesion_slider.valueChanged.connect(self.cohesion_change)

        self.alignment_slider.setRange(0, 50)
        self.alignment_slider.setValue(int(self.coeffitients[2] * 10))
        self.alignment_slider.valueChanged.connect(self.alignment_change)

        layout.addWidget(self.canvas.native)
        layout.addWidget(self.wall_bounce_checkbox)
        layout.addWidget(self.separation_label)
        layout.addWidget(self.separation_slider)
        layout.addWidget(self.cohesion_label)
        layout.addWidget(self.cohesion_slider)
        layout.addWidget(self.alignment_label)
        layout.addWidget(self.alignment_slider)

    def separation_change(self, value):
        self.coeffitients[0] = float(value / 10)
        self.separation_label.setText(f"Separation: {value / 10}")
        print(f"Separation changed to: {value / 10}")

    def cohesion_change(self, value):
        self.coeffitients[1] = float(value)
        self.cohesion_label.setText(f"Cohesion: {value}")
        print(f"Cohesion changed to: {value}")

    def alignment_change(self, value):
        self.coeffitients[2] = float(value / 10)
        self.alignment_label.setText(f"Alignment: {value / 10}")
        print(f"Alignment changed to: {value / 10}")

    def wall_bounce_change(self, state):
        if state == 2:
            self.wall_bounce = True
        else:
            self.wall_bounce = False
        print(f"Wall bounce changed to: {self.wall_bounce}")

    def update(self):
        # start_time = time.time()

        flocking(self.boids, self.perception, self.coeffitients, self.aspect_ratio, self.velocity_range,
                 self.acceleration_range, self.wall_bounce)
        propagate(self.boids, self.delta_time, self.velocity_range)

        self.arrows.set_data(arrows=directions(self.boids, self.delta_time))
        self.canvas.update()
        # print(self.coeffitients)
        # end_time = time.time()
        # self.delta_time = end_time - start_time


if __name__ == '__main__':
    app.create()
    simulation_window = BoidsSimulation()
    simulation_window.show()
    app.run()
