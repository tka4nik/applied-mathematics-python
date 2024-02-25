import numpy as np


def init_boids(boids: np.ndarray, asp: float, vrange: tuple[float, float]):
    n = boids.shape[0]
    rng = np.random.default_rng()
    boids[:, 0] = rng.uniform(0., asp, size=n)
    boids[:, 1] = rng.uniform(0., 1., size=n)
    alpha = rng.uniform(0, 2 * np.pi, size=n)
    v = rng.uniform(*vrange, size=n)
    c, s = np.cos(alpha), np.sin(alpha)
    boids[:, 2] = v * c
    boids[:, 3] = v * s


def directions(boids: np.ndarray, dt: float) -> np.ndarray:
    """
    :param boids:
    :param dt:
    :return: array N x (x0, y0, x1, y1) for arrow painting
    """
    return np.hstack((
        boids[:, :2] - dt * boids[:, 2:4],
        boids[:, :2]
    ))


def vclip(v: np.ndarray, vrange: tuple[float, float]):
    norm = np.linalg.norm(v, axis=1)
    mask = norm > vrange[1]
    if np.any(mask):
        v[mask] *= (vrange[1] / norm[mask]).reshape(-1, 1)


def propagate(boids: np.ndarray,
              dt: float,
              vrange: tuple[float, float],
              arange: tuple[float, float]):
    vclip(boids[:, 4:6], arange)
    boids[:, 2:4] += dt * boids[:, 4:6]
    vclip(boids[:, 2:4], vrange)
    boids[:, 0:2] += dt * boids[:, 2:4]


def distances(vecs: np.ndarray) -> np.ndarray:
    n, m = vecs.shape
    delta = vecs.reshape((n, 1, m)) - vecs.reshape((1, n, m))
    D = np.linalg.norm(delta, axis=2)
    return D


def cohesion(boids: np.ndarray,
             idx: int,
             neigh_mask: np.ndarray,
             perception: float) -> np.ndarray:
    center = boids[neigh_mask, :2].mean(axis=0)
    a = (center - boids[idx, :2]) / perception
    return a


def separation(boids: np.ndarray,
               idx: int,
               neigh_mask: np.ndarray,
               perception: float) -> np.ndarray:
    neighbs = boids[neigh_mask, :2] - boids[idx, :2]
    norm = np.linalg.norm(neighbs, axis=1)
    mask = norm > 0
    if np.any(mask):
        neighbs[mask] /= norm[mask].reshape(-1, 1)
    d = neighbs.mean(axis=0)
    norm_d = np.linalg.norm(d)
    if norm_d > 0:
        d /= norm_d
    # d = (boids[neigh_mask, :2] - boids[idx, :2]).mean(axis=0)
    return -d  # / ((d[0] ** 2 + d[1] ** 2) + 1)


def alignment(boids: np.ndarray,
              idx: int,
              neigh_mask: np.ndarray,
              vrange: tuple) -> np.ndarray:
    v_mean = boids[neigh_mask, 2:4].mean(axis=0)
    a = (v_mean - boids[idx, 2:4]) / (2 * vrange[1])
    return a

def walls(boids: np.ndarray, asp: float, param: int):
    c = 1
    x = boids[:, 0]
    y = boids[:, 1]
    order = param

    a_left = 1 / (np.abs(x) + c) ** order
    a_right = -1 / (np.abs(x - asp) + c) ** order

    a_bottom = 1 / (np.abs(y) + c) ** order
    a_top = -1 / (np.abs(y - 1.) + c) ** order

    return np.column_stack((a_left + a_right, a_bottom + a_top))


def smoothstep(edge0: float, edge1: float, x: np.ndarray | float) -> np.ndarray | float:
   x = np.clip((x - edge0) / (edge1 - edge0), 0., 1.)
   return x * x * (3.0 - 2.0 * x)


def better_walls(boids: np.ndarray, asp: float, param: float):
    x = boids[:, 0]
    y = boids[:, 1]
    w = param

    a_left = smoothstep(asp * w, 0.0, x)
    a_right = -smoothstep(asp * (1.0 - w), asp, x)

    a_bottom = smoothstep(w, 0.0, y)
    a_top = -smoothstep(1.0 - w, 1.0, y)

    return np.column_stack((a_left + a_right, a_bottom + a_top))


def flocking(boids: np.ndarray,
             perception: float,
             coeffs: np.ndarray,
             asp: float,
             vrange: tuple,
             order: int):
    D = distances(boids[:, 0:2])
    N = boids.shape[0]
    D[range(N), range(N)] = perception + 1
    mask = D < perception
    wal = better_walls(boids, asp, order)
    for i in range(N):
        if not np.any(mask[i]):
            coh = np.zeros(2)
            alg = np.zeros(2)
            sep = np.zeros(2)
        else:
            coh = cohesion(boids, i, mask[i], perception)
            alg = alignment(boids, i, mask[i], vrange)
            sep = separation(boids, i, mask[i], perception)
        a = coeffs[0] * coh + coeffs[1] * alg + \
            coeffs[2] * sep + coeffs[3] * wal[i]
        boids[i, 4:6] = a