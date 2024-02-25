import numpy as np


def init_boids(boids: np.ndarray, asp: float, vrange: tuple[float, float]):
    n = boids.shape[0]
    random = np.random.default_rng()
    boids[:, 0] = random.uniform(0., asp, size=n)
    boids[:, 1] = random.uniform(0., 1., size=n)

    alpha = random.uniform(0, 2 * np.pi, size=n)
    velocity = random.uniform(*vrange, size=n)
    cos, sin = np.cos(alpha), np.sin(alpha)
    boids[:, 2], boids[:, 3] = velocity * cos, velocity * sin

    # boids[0] = np.array([0.5, 0.5, 0, 0.5, 0, 0])
    # boids[1] = np.array([0.5, 0.55, 0, -0.1, 0, 0])
    # boids[2] = np.array([0.54, 0.525, -0.1, -0.1, 0, 0])
    # print(boids)


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


def distance(boids, i):
    return np.linalg.norm(boids[i, 0:2] - boids[:, 0:2], axis=1)
    # difference = boids[i, 0:2] - boids[:, 0:2]
    #
    # distances = np.ndarray(difference.shape[0])
    # for j in range(difference.shape[0]):
    #     distances[j] = np.sqrt(np.sum(difference[j] ** 2))
    # return np.sqrt(distances)


def clip_array(array, range):
    min_magnitude, max_magnitude = range
    norm = np.linalg.norm(array, axis=1)
    mask_max = norm > max_magnitude
    mask_min = norm < min_magnitude
    if np.any(mask_max):
        array[mask_max] = (array[mask_max] / np.linalg.norm(array[mask_max], axis=1).reshape(-1, 1)) * max_magnitude

    if np.any(mask_min):
        array[mask_min] = (array[mask_min] / np.linalg.norm(array[mask_min], axis=1).reshape(-1, 1)) * min_magnitude


def clip_vector(vector, range):
    min_magnitude, max_magnitude = range
    norm = np.linalg.norm(vector)
    mask_max = norm > max_magnitude
    mask_min = norm < min_magnitude
    if mask_max:
        vector[mask_max] = (vector[mask_max] / np.linalg.norm(vector[mask_max])) * max_magnitude

    if mask_min:
        vector[mask_min] = (vector[mask_min] / np.linalg.norm(vector[mask_min])) * min_magnitude


def compute_walls_interations(boids, i, aspect_ratio):
    mask_walls = np.empty(4)
    mask_walls[0] = boids[i, 1] > 1
    mask_walls[1] = boids[i, 0] > aspect_ratio
    mask_walls[3] = boids[i, 0] < 0
    mask_walls[2] = boids[i, 1] < 0

    if mask_walls[0]:
        boids[i, 1] = 0
    if mask_walls[1]:
        boids[i, 0] = 0
    if mask_walls[2]:
        boids[i, 1] = 1
    if mask_walls[3]:
        boids[i, 0] = aspect_ratio


def compute_walls_interations_bounce(boids, i, aspect_ratio):
    mask_walls = np.empty(4)
    mask_walls[0] = boids[i, 1] > 1
    mask_walls[1] = boids[i, 0] > aspect_ratio
    mask_walls[2] = boids[i, 1] < 0
    mask_walls[3] = boids[i, 0] < 0

    if mask_walls[0]:
        boids[i, 3] = -boids[i, 3]
        boids[i][1] = 1 - 0.001

    if mask_walls[1]:
        boids[i, 2] = -boids[i, 2]
        boids[i, 0] = aspect_ratio - 0.001

    if mask_walls[2]:
        boids[i, 3] = -boids[i, 3]
        boids[i, 1] = 0.001

    if mask_walls[3]:
        boids[i, 2] = -boids[i, 2]
        boids[i, 0] = 0.001


def separation(boids, i, distance_mask):
    distance_mask[i] = False
    directions = boids[i, :2] - boids[distance_mask][:, :2]
    directions *= (1 / (np.linalg.norm(directions, axis=0) + 0.0001))
    acceleration = np.sum(directions, axis=0)
    return acceleration - boids[i, 2:4]


def alignment(boids, i, distance_mask):
    velocity = boids[distance_mask][:, 2:4]
    acceleration = np.sum(velocity, axis=0)
    acceleration /= velocity.shape[0]
    return acceleration - boids[i, 2:4]


def cohesion(boids, i, distance_mask):
    directions = boids[distance_mask][:, :2] - boids[i, :2]
    acceleration = np.sum(directions, axis=0)
    acceleration /= directions.shape[0]
    return acceleration - boids[i, 2:4]


def flocking(boids, perseption, coeffitients, aspect_ratio, v_range, a_range, wall_bounce):
    a_separation = np.zeros(2)
    a_cohesion = np.zeros(2)
    a_alignment = np.zeros(2)
    for i in range(boids.shape[0]):
        d = distance(boids, i)
        perception_mask = d < perseption
        separation_mask = d < perseption / 2
        separation_mask[i] = False
        cohesion_mask = np.logical_xor(perception_mask, separation_mask) # In the ring between separation and perseption ranges

        if wall_bounce:
            compute_walls_interations_bounce(boids, i, aspect_ratio)
        else:
            compute_walls_interations(boids, i, aspect_ratio)

        # Main interactions
        if np.any(perception_mask):
            if np.any(separation_mask):
                a_separation = separation(boids, i, separation_mask)
            if np.any(cohesion_mask):
                a_cohesion = cohesion(boids, i, cohesion_mask)
            a_alignment = alignment(boids, i, perception_mask)
            clip_vector(a_separation, a_range)
            clip_vector(a_cohesion, a_range)

        acceleration = coeffitients["separation"] * a_separation \
                     + coeffitients["cohesion"] * a_cohesion \
                     + coeffitients["alignment"] * a_alignment
        boids[i, 4:6] = acceleration


def propagate(boids, delta_time, v_range):
    boids[:, 2:4] += boids[:, 4:6] * delta_time
    clip_array(boids[:, 2:4], v_range)
    boids[:, 0:2] += boids[:, 2:4] * delta_time
