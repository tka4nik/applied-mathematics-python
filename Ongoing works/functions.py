import numpy as np

def init_boids(boids: np.ndarray, asp: float, vrange: tuple[float, float]):
    n = boids.shape[0]
    rng = np.random.default_rng()
    boids[:, 0] = rng.uniform(0., asp, size=n)
    boids[:, 1] = rng.uniform(0., 1., size=n)

    alpha = rng.uniform(0, 2 * np.pi, size=n)
    velocity = rng.uniform(*vrange, size=n)
    c, s = np.cos(alpha), np.sin(alpha)
    boids[:, 2], boids[:, 3] = velocity * c, velocity * s


def directions(boids: np.ndarray, dt=float) -> np.ndarray:
    """

    :param boids:
    :param dt:
    :return: array N * (x0, y0, x1, y1) for Arrow
    """
    return np.hstack((
        boids[:, :2] - dt * boids[:, 2:4],
        boids[:, :2]
    ))
