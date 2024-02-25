from functions import *

import time
from vispy import app, scene
from vispy.geometry import Rect

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QMainWindow, QSlider, QVBoxLayout, QWidget, QLabel


class BoidsSimulation(QMainWindow):
    def __init__(self):
        super().__init__()

        self.alignment_label = None
        self.separation_label = None
        self.cohesion_slider = None
        self.separation_slider = None
        self.alignment_slider = None
        self.cohesion_label = None

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        # ========================================================
        width, height = 700, 500
        N = 700
        self.delta_time = 0.1
        self.aspect_ratio = width / height
        self.perception = 1 / 3
        self.coeffitients = {"cohesion": 1.5,
                             "separation": .03,
                             "alignment": .3,
                             "wall": 0.03
                             }

        self.velocity_range = (0.2, 0.5)
        self.acceleration_range = (0, 3)

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
        self.cohesion_label = QLabel(self)
        self.cohesion_label.setText(f"Cohesion: {self.coeffitients['cohesion']}")
        self.cohesion_slider = QSlider(Qt.Orientation.Horizontal)
        self.separation_label = QLabel(self)
        self.separation_label.setText(f"Separation: {self.coeffitients['separation']}")
        self.separation_slider = QSlider(Qt.Orientation.Horizontal)
        self.alignment_label = QLabel(self)
        self.alignment_label.setText(f"Alignment: {self.coeffitients['alignment']}")
        self.alignment_slider = QSlider(Qt.Orientation.Horizontal)
        self.cohesion_slider.setGeometry(50, 0, int(width * 0.7), 30)
        self.separation_slider.setGeometry(50, 40, int(width * 0.7), 30)
        self.alignment_slider.setGeometry(50, 80, int(width * 0.7), 30)

        self.cohesion_slider.setRange(1, 50)
        self.cohesion_slider.setValue(int(self.coeffitients["cohesion"] * 10))
        self.cohesion_slider.valueChanged.connect(self.cohesion_change)

        self.separation_slider.setRange(1, 50)
        self.separation_slider.setValue(int(self.coeffitients["separation"] * 100))
        self.separation_slider.valueChanged.connect(self.separation_change)

        self.alignment_slider.setRange(1, 50)
        self.alignment_slider.setValue(int(self.coeffitients["alignment"] * 10))
        self.alignment_slider.valueChanged.connect(self.alignment_change)

        layout.addWidget(self.canvas.native)
        layout.addWidget(self.cohesion_label)
        layout.addWidget(self.cohesion_slider)
        layout.addWidget(self.separation_label)
        layout.addWidget(self.separation_slider)
        layout.addWidget(self.alignment_label)
        layout.addWidget(self.alignment_slider)

    def cohesion_change(self, value):
        self.coeffitients["cohesion"] = float(value / 10)
        self.cohesion_label.setText(f"Cohesion: {self.coeffitients['cohesion']}")
        print(f"Cohesion changed to: {value / 10}")

    def separation_change(self, value):
        self.coeffitients["separation"] = float(value / 100)
        self.separation_label.setText(f"Separation: {value / 100}")
        print(f"Separation changed to: {value / 100}")

    def alignment_change(self, value):
        self.coeffitients["alignment"] = float(value / 10)
        self.alignment_label.setText(f"Alignment: {value / 10}")
        print(f"Alignment changed to: {value / 10}")

    def update(self):
        start_time = time.time()

        flocking(self.boids, self.perception, self.coeffitients, self.aspect_ratio, self.velocity_range,
                 self.acceleration_range)
        propagate(self.boids, self.delta_time, self.velocity_range)

        self.arrows.set_data(arrows=directions(self.boids, self.delta_time))
        self.canvas.update()

        end_time = time.time()
        self.delta_time = end_time - start_time


if __name__ == '__main__':
    app.create()
    simulation_window = BoidsSimulation()
    simulation_window.show()
    app.run()
