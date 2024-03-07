from boids_simulation import BoidsSimulation

from vispy import app
import numpy as np

if __name__ == '__main__':
    app.create()
    # Коэффициенты
    coefficients = np.array([
        [.1, .1, 2.0, 0.5, 10],
        [.01, 26.0, 2.9, 0.5, 10],
        [1.2, .1, 0.0, 0.5, 10],
        [.1, 7.0, 0.1, 0.5, 10]
    ])
    window = BoidsSimulation(2000, coefficients, 1000, 700)
    window.show()
    app.run()
