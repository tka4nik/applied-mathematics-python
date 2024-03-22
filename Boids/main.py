from boids_simulation import BoidsSimulation

from vispy import app
import numpy as np

if __name__ == '__main__':
    app.create()
    # Коэффициенты
    coefficients = np.array([
        [.1, .1, 2.0, 0.5, 1],
        [.01, 26.0, 2.9, 0.5, 1],
        [1.2, .1, 0.0, 0.5, 1],
        [.1, 7.0, 0.1, 0.5, 1]
    ])
    window = BoidsSimulation(5000, coefficients, 5000, 3000)
    window.show()
    app.run()
