from functions import *

import time
from vispy import app, scene
from vispy.geometry import Rect


width, height = 3000, 1500
N = 5000
dt = 0.01
aspect_ratio = width / height
perception = 1 / 30
#                  cohesion       a   v    wall
# coeffitients = {"cohesion": 7.0,
#                 "separation": .5,
#                 "alignment": 3,
#                 "wall": 0.03
#                 }
#                        sep  coh  ali  wall
coeffitients = np.array([.4, 15.0, 2.0, 0.3])
velocity_range = np.array([0.2, 0.7])
acceleration_range = np.array([0, 2])

# (x,y), (vx, vy), (ax, ay)
boids = np.zeros((N, 6), dtype=np.float64)
init_boids(boids, aspect_ratio, velocity_range)

canvas = scene.SceneCanvas(show=True, size=(width, height))
view = canvas.central_widget.add_view()
view.camera = scene.PanZoomCamera(rect=Rect(0, 0, aspect_ratio, 1))
arrows = scene.Arrow(arrows=directions(boids, dt), arrow_color=(1, 1, 1, 1), arrow_size=5, connect='segments',
                     parent=view.scene)

# global delta_time
delta_time = dt


def update(event):
    # global delta_time
    # start_time = time.time()

    flocking(boids, perception, coeffitients, aspect_ratio, velocity_range, acceleration_range)
    propagate(boids, delta_time, velocity_range)

    arrows.set_data(arrows=directions(boids, delta_time))
    canvas.update()  # отображение

    # time.sleep(0.05)
    # end_time = time.time()
    # delta_time = end_time - start_time


if __name__ == '__main__':
    timer = app.Timer(interval=0, start=True, connect=update)
    canvas.measure_fps()
    app.run()
