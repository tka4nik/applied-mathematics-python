from functions import *

import time
from vispy import scene
from vispy.geometry import Rect

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QMainWindow, QSlider, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QCheckBox

from functools import partial


class BoidsSimulation(QMainWindow):
    def __init__(self, N, width, height):
        super().__init__()
        self.wall_bounce_checkbox = None
        self.center_camera_checkbox = None
        self.class_11_label = None
        self.separation_slider_11 = None
        self.cohesion_slider_11 = None
        self.alignment_slider_11 = None
        self.class_12_label = None
        self.separation_slider_12 = None
        self.cohesion_slider_12 = None
        self.alignment_slider_12 = None
        self.class_21_label = None
        self.separation_slider_21 = None
        self.cohesion_slider_21 = None
        self.alignment_slider_21 = None
        self.class_22_label = None
        self.separation_slider_22 = None
        self.cohesion_slider_22 = None
        self.alignment_slider_22 = None

        # ========================================================
        self.N = N
        self.delta_time = 0.01
        self.aspect_ratio = width / height
        self.perception = 1 / 20

        #      s    c     a    w
        # self.coeffitients = np.array([
        #     [.2, 5.0, 2.0, 0.3],  # c11
        #     [.2, 5.0, 2.0, 0.3],  # c12
        #     [.2, 5.0, 2.0, 0.3],  # c21
        #     [.2, 5.0, 2.0, 0.3]   # c22
        # ])
        #
        self.coeffitients = np.array([
            [.1, .1, 2.0, 0.2],
            [.01, 26.0, 2.9, 0.2],
            [1.2, .1, 0.0, 0.2],
            [.1, 7.0, 0.1, 0.2]
        ])

        # self.coeffitients = np.array([
        #     [.0, 40.0, .0, 0.8],
        #     [.0, 40.0, .0, 0.8],
        #     [.0, 40.0, .0, 0.8],
        #     [.0, 40.0, .0, 0.8]
        # ])

        self.velocity_range = np.array([0.2, 0.5])
        self.acceleration_range = np.array([0.0, 2.0])
        self.wall_bounce = False

        # (x,y), (vx, vy), (ax, ay)
        self.boids = np.zeros((self.N, 7), dtype=np.float64)
        init_boids(self.boids, self.aspect_ratio, self.velocity_range)

        # =======================================================

        self.main_layout = QHBoxLayout()
        self.settings_layout = QVBoxLayout()
        self.settings_layout.addStretch()
        self.simulation = QWidget(self)
        self.main_layout.addWidget(self.simulation)

        self.canvas = scene.SceneCanvas(show=True, size=(width, height), parent=self.simulation)
        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.PanZoomCamera(rect=Rect(0, 0, self.aspect_ratio, 1))
        self.main_layout.addWidget(self.canvas.native)
        self.center_camera_flag = False

        self.create_settings(self.settings_layout, width, height)
        self.main_layout.addLayout(self.settings_layout)

        main_widget = QWidget()
        main_widget.setLayout(self.main_layout)
        self.setCentralWidget(main_widget)

        # =======================================================
        self.arrows1 = scene.Arrow(arrows=directions(self.boids[self.boids[:, 6] == 0], self.delta_time),
                                   # arrow_color=(1, 0, 0, 0.9),
                                   arrow_color=(0, 1, 0.306),
                                   arrow_size=7,
                                   connect='segments',
                                   parent=self.view.scene)

        self.arrows2 = scene.Arrow(arrows=directions(self.boids[self.boids[:, 6] == 1], self.delta_time),
                                   # arrow_color=(0, 0, 1, 0.9),
                                   arrow_color=(0, 1, 0.306),
                                   arrow_size=7,
                                   connect='segments',
                                   parent=self.view.scene)

        self.arrows_selected = scene.Arrow(arrows=directions(self.boids[0:0], self.delta_time),
                                           arrow_color=(1, 0.82, 0),
                                           # arrow_color=(0, 1, 0.306),
                                           arrow_size=7,
                                           connect='segments',
                                           parent=self.view.scene)

        # Set up the timer and connect it to the update function
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update)
        self.timer.start()

    def create_settings(self, layout, width, height):
        self.wall_bounce_checkbox = QCheckBox("Wall bounce", self)
        self.wall_bounce_checkbox.stateChanged.connect(self.wall_bounce_change)
        self.wall_bounce_checkbox.setChecked(False)

        self.center_camera_checkbox = QCheckBox("Camera center", self)
        self.center_camera_checkbox.stateChanged.connect(self.center_camera)
        self.center_camera_checkbox.setChecked(False)

        # Interactions between Class1 and Class1
        self.class_11_label = QLabel(self)
        self.class_11_label.setText(f"Interactions for a11: , Separation: {self.coeffitients[0, 0]}, Cohesion: {self.coeffitients[0, 1]}, Alignment: {self.coeffitients[0, 2]}")
        self.separation_slider_11 = QSlider(Qt.Orientation.Horizontal)
        self.cohesion_slider_11 = QSlider(Qt.Orientation.Horizontal)
        self.alignment_slider_11 = QSlider(Qt.Orientation.Horizontal)

        self.separation_slider_11.setRange(0, 50)
        self.separation_slider_11.setValue(int(self.coeffitients[0, 0] * 10))
        self.separation_slider_11.valueChanged.connect(partial(self.separation_change, i=0))

        self.cohesion_slider_11.setRange(0, 100)
        self.cohesion_slider_11.setValue(int(self.coeffitients[0, 1]))
        self.cohesion_slider_11.valueChanged.connect(partial(self.cohesion_change, i=0))

        self.alignment_slider_11.setRange(0, 50)
        self.alignment_slider_11.setValue(int(self.coeffitients[0, 2] * 10))
        self.alignment_slider_11.valueChanged.connect(partial(self.alignment_change, i=0))

        # Interactions between Class1 and Class2
        self.class_12_label = QLabel(self)
        self.class_12_label.setText(
            f"Interactions for a12: , Separation: {self.coeffitients[1, 0]}, Cohesion: {self.coeffitients[1, 1]}, Alignment: {self.coeffitients[1, 2]}")
        self.separation_slider_12 = QSlider(Qt.Orientation.Horizontal)
        self.cohesion_slider_12 = QSlider(Qt.Orientation.Horizontal)
        self.alignment_slider_12 = QSlider(Qt.Orientation.Horizontal)

        self.separation_slider_12.setRange(0, 50)
        self.separation_slider_12.setValue(int(self.coeffitients[1, 0] * 10))
        self.separation_slider_12.valueChanged.connect(partial(self.separation_change, i=1))

        self.cohesion_slider_12.setRange(0, 100)
        self.cohesion_slider_12.setValue(int(self.coeffitients[1, 1]))
        self.cohesion_slider_12.valueChanged.connect(partial(self.cohesion_change, i=1))

        self.alignment_slider_12.setRange(0, 50)
        self.alignment_slider_12.setValue(int(self.coeffitients[1, 2] * 10))
        self.alignment_slider_12.valueChanged.connect(partial(self.alignment_change, i=1))

        # Interactions between Class2 and Class1
        self.class_21_label = QLabel(self)
        self.class_21_label.setText(f"Interactions for a21: , Separation: {self.coeffitients[2, 0]}, Cohesion: {self.coeffitients[2, 1]}, Alignment: {self.coeffitients[2, 2]}")
        self.separation_slider_21 = QSlider(Qt.Orientation.Horizontal)
        self.cohesion_slider_21 = QSlider(Qt.Orientation.Horizontal)
        self.alignment_slider_21 = QSlider(Qt.Orientation.Horizontal)

        self.separation_slider_21.setRange(0, 50)
        self.separation_slider_21.setValue(int(self.coeffitients[2, 0] * 10))
        self.separation_slider_21.valueChanged.connect(partial(self.separation_change, i=2))

        self.cohesion_slider_21.setRange(0, 100)
        self.cohesion_slider_21.setValue(int(self.coeffitients[2, 1]))
        self.cohesion_slider_21.valueChanged.connect(partial(self.cohesion_change, i=2))

        self.alignment_slider_21.setRange(0, 50)
        self.alignment_slider_21.setValue(int(self.coeffitients[2, 2] * 10))
        self.alignment_slider_21.valueChanged.connect(partial(self.alignment_change, i=2))

        # Interactions between Class2 and Class2
        self.class_22_label = QLabel(self)
        self.class_22_label.setText(f"Interactions for a22: , Separation: {self.coeffitients[3, 0]}, Cohesion: {self.coeffitients[3, 1]}, Alignment: {self.coeffitients[3, 2]}")
        self.separation_slider_22 = QSlider(Qt.Orientation.Horizontal)
        self.cohesion_slider_22 = QSlider(Qt.Orientation.Horizontal)
        self.alignment_slider_22 = QSlider(Qt.Orientation.Horizontal)

        self.separation_slider_22.setRange(0, 50)
        self.separation_slider_22.setValue(int(self.coeffitients[3, 0] * 10))
        self.separation_slider_22.valueChanged.connect(partial(self.separation_change, i=3))

        self.cohesion_slider_22.setRange(0, 100)
        self.cohesion_slider_22.setValue(int(self.coeffitients[3, 1]))
        self.cohesion_slider_22.valueChanged.connect(partial(self.cohesion_change, i=3))

        self.alignment_slider_22.setRange(0, 50)
        self.alignment_slider_22.setValue(int(self.coeffitients[3, 2] * 10))
        self.alignment_slider_22.valueChanged.connect(partial(self.alignment_change, i=3))

        layout.addWidget(self.wall_bounce_checkbox)
        layout.addWidget(self.center_camera_checkbox)
        layout.addWidget(self.class_11_label)
        layout.addWidget(self.separation_slider_11)
        layout.addWidget(self.cohesion_slider_11)
        layout.addWidget(self.alignment_slider_11)
        layout.addWidget(self.class_12_label)
        layout.addWidget(self.separation_slider_12)
        layout.addWidget(self.cohesion_slider_12)
        layout.addWidget(self.alignment_slider_12)
        layout.addWidget(self.class_21_label)
        layout.addWidget(self.separation_slider_21)
        layout.addWidget(self.cohesion_slider_21)
        layout.addWidget(self.alignment_slider_21)
        layout.addWidget(self.class_22_label)
        layout.addWidget(self.separation_slider_22)
        layout.addWidget(self.cohesion_slider_22)
        layout.addWidget(self.alignment_slider_22)

    def separation_change(self, value, i):
        self.coeffitients[i, 0] = float(value / 10)
        self.update_labels()
        print(f"Separation {i} changed to: {value / 10}")

    def cohesion_change(self, value, i):
        self.coeffitients[i, 1] = float(value)
        self.update_labels()
        print(f"Cohesion {i} changed to: {value}")

    def alignment_change(self, value, i):
        self.coeffitients[i, 2] = float(value / 10)
        self.update_labels()
        print(f"Alignment {i} changed to: {value / 10}")

    def wall_bounce_change(self, state):
        if state == 2:
            self.wall_bounce = True
        else:
            self.wall_bounce = False
        print(f"Wall bounce changed to: {self.wall_bounce}")

    def center_camera(self, state):
        if state == 2:
            self.center_camera_flag = True
            self.view.camera.center = tuple(self.boids[0, 0:2])
            self.view.camera.zoom(1 / 6)
            self.arrows_selected.set_data(arrows=directions(self.boids[0:1], self.delta_time))
        else:
            self.center_camera_flag = False
            self.view.camera.center = (0.5, 0.5)
            self.view.camera.zoom(1)
            self.arrows_selected.set_data(arrows=directions(self.boids[0:0], self.delta_time))

        print(f"Camera center changed to: {self.center_camera_checkbox}")

    def update_camera(self):
        if self.center_camera_flag:
            delta_distance = self.boids[0, 0:2] - self.view.camera.center[0:2]
            self.view.camera.pan(delta_distance)
            self.arrows_selected.set_data(arrows=directions(self.boids[0:1], self.delta_time))

    def update_labels(self):
        self.class_11_label.setText(f"Interactions for a11: , Separation: {self.coeffitients[0, 0]}, Cohesion: {self.coeffitients[0, 1]}, Alignment: {self.coeffitients[0, 2]}")
        self.class_12_label.setText(f"Interactions for a12: , Separation: {self.coeffitients[1, 0]}, Cohesion: {self.coeffitients[1, 1]}, Alignment: {self.coeffitients[1, 2]}")
        self.class_21_label.setText(f"Interactions for a21: , Separation: {self.coeffitients[2, 0]}, Cohesion: {self.coeffitients[2, 1]}, Alignment: {self.coeffitients[2, 2]}")
        self.class_22_label.setText(f"Interactions for a22: , Separation: {self.coeffitients[3, 0]}, Cohesion: {self.coeffitients[3, 1]}, Alignment: {self.coeffitients[3, 2]}")

    def update(self):
        self.canvas.update()
        self.update_camera()
        self.arrows1.set_data(arrows=directions(self.boids[self.boids[:, 6] == 0], self.delta_time))
        self.arrows2.set_data(arrows=directions(self.boids[self.boids[:, 6] == 1], self.delta_time))

        start_time = time.time()

        flocking(self.boids, self.perception, self.coeffitients, self.aspect_ratio, self.velocity_range,
                 self.acceleration_range, self.wall_bounce)
        propagate(self.boids, self.delta_time, self.velocity_range)
        time.sleep(1.0)

        end_time = time.time()
        self.delta_time = end_time - start_time


        print(self.delta_time)
        self.canvas.measure_fps()
        self.setWindowTitle(f"{self.N} Boids; {np.round(self.canvas.fps, 2)} fps;")

