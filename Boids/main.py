from boids_simulation import BoidsSimulation
from vispy import app


if __name__ == '__main__':
    app.create()
    window = BoidsSimulation(1000, 1000, 600)
    window.show()
    app.run()