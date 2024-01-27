from vispy import app, scene
from vispy.geometry import Rect
import numpy as np

from functions import init_boids, directions

w, h = 640, 480
N = 100
dt = 0.1
asp = w / h
perception = 1 / 20
vrange = (0, 0.1)
#                  cohesion       a   v    wall
coeffs = np.array([0.05, 0.02, 4, 0.03])
# (x,y), (vx, vy), (ax, ay)
boids = np.zeros((N, 6), dtype=np.float64)
init_boids(boids, asp, vrange)

canvas = scene.SceneCanvas(show=True, size=(w, h))
view = canvas.central_widget.add_view()
view.camera = scene.PanZoomCamera(rect=Rect(0, 0, asp, 1))
arrows = scene.Arrow(arrows=directions(boids, dt),
                     arrow_color=(1, 1, 1, 1),
                     arrow_size=5,
                     connect='segments',
                     parent=view.scene)


def update(event):
    # print(event)
    arrows.set_data(arrows=directions(boids, dt))
    canvas.update()


if __name__ == '__main__':
    timer = app.Timer(interval=0, start=True, connect=update)
    canvas.measure_fps()
    app.run()
