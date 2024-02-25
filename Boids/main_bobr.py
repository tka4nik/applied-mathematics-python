import numpy as np
from vispy import app, scene
from vispy.geometry import Rect
from funcs import init_boids, directions, propagate, flocking
app.use_app('pyglet')

w, h = 1280, 960
N = 500
dt = 0.1
asp = w / h
perception = 1/20
# walls_order = 8
better_walls_w = 0.05
vrange=(0, 0.1)
arange=(0, 0.05)

#                    c      a    s      w
coeffs = np.array([0.05, 0.02,   0.1,  0.03])

# 0  1   2   3   4   5
# x, y, vx, vy, ax, ay
boids = np.zeros((N, 6), dtype=np.float64)
init_boids(boids, asp, vrange=vrange)
# boids[:, 4:6] = 0.1

canvas = scene.SceneCanvas(show=True, size=(w, h))
view = canvas.central_widget.add_view()
view.camera = scene.PanZoomCamera(rect=Rect(0, 0, asp, 1))
arrows = scene.Arrow(arrows=directions(boids, dt),
                     arrow_color=(1, 1, 1, 1),
                     # width=5,
                     arrow_size=10,
                     connect='segments',
                     parent=view.scene)


def update(event):
    flocking(boids, perception, coeffs, asp, vrange, better_walls_w)
    propagate(boids, dt, vrange, arange)
    arrows.set_data(arrows=directions(boids, dt))
    canvas.update()


if __name__ == '__main__':
    timer = app.Timer(interval=0, start=True, connect=update)
    canvas.measure_fps()
    app.run()
