import numpy as np
from numba import njit, prange


def init_boids(boids: np.ndarray, aspect_ratio: float, vrange: np.ndarray):
    """
    Constructor for boids array
    :param boids: numpy array (N, 6) -> [x, y, vx, vy, ax, ay, class]
    :param vrange: numpy array - allowed velocity range
    """
    n = boids.shape[0]
    random = np.random.default_rng()
    boids[:, 0] = random.uniform(0., aspect_ratio, size=n)
    boids[:, 1] = random.uniform(0., 1., size=n)

    alpha = random.uniform(0, 2 * np.pi, size=n)
    velocity = random.uniform(*vrange, size=n)
    cos, sin = np.cos(alpha), np.sin(alpha)
    boids[:, 2], boids[:, 3] = velocity * cos, velocity * sin
    boids[:, 6] = random.integers(0, 2, size=n)


def directions(boids: np.ndarray, delta_time: float) -> np.ndarray:
    """
    Function that calculates coordinates of the tip of the arrow for each boid
    :param boids: numpy array (N, 6) -> [x, y, vx, vy, ax, ay, class]
    :return: array N * (x0, y0, x1, y1) for Arrow
    """
    return np.hstack((
        boids[:, :2] - delta_time * boids[:, 2:4],
        boids[:, :2]
    ))


@njit
def njit_norm_axis1(vector: np.ndarray):
    """
    Numba-friendly implementation of np.linalg.norm(.., axis=1)
    """
    norm = np.empty(vector.shape[0], dtype=np.float64)
    for j in prange(vector.shape[0]):
        norm[j] = np.sqrt(vector[j, 0] * vector[j, 0] + vector[j, 1] * vector[j, 1])
    return norm


@njit
def njit_norm_vector(vector: np.ndarray):
    """
    Numba-friendly implementation of np.linalg.norm()
    """
    norm = 0
    for j in prange(vector.shape[0]):
        norm += vector[j] * vector[j]
    return np.sqrt(norm)


@njit
def distance(boids: np.ndarray, i: int):
    """
    Numba-friendly implementation of distance function
    :param i: id of a boid
    """
    difference = boids[i, 0:2] - boids[:, 0:2]
    return njit_norm_axis1(difference)


@njit
def clip_array(array: np.ndarray, range: np.ndarray) -> np.ndarray:
    """
    Function that limits array to the specified range horizontally (axis=1)
    """
    min_magnitude, max_magnitude = range
    norm = njit_norm_axis1(array)
    mask_max = norm > max_magnitude
    mask_min = norm < min_magnitude
    new_array = array.copy()
    if np.any(mask_max):
        new_array[mask_max] = (array[mask_max] / njit_norm_axis1(array[mask_max]).reshape(-1, 1)) * max_magnitude

    if np.any(mask_min):
        new_array[mask_min] = (array[mask_min] / njit_norm_axis1(array[mask_min]).reshape(-1, 1)) * min_magnitude

    return new_array


@njit
def clip_vector(vector: np.ndarray, range: np.ndarray) -> np.ndarray:
    """
    Function that limits vector to the specified range
    """
    min_magnitude, max_magnitude = range
    norm = njit_norm_vector(vector)
    mask_max = norm > max_magnitude
    mask_min = norm < min_magnitude
    new_vector = vector.copy()
    if mask_max:
        new_vector = (vector / norm) * max_magnitude

    if mask_min:
        new_vector = (vector / norm) * min_magnitude
    return new_vector


@njit
def separation(boids: np.ndarray, i: int, distance_mask: np.ndarray):
    """
    Calculates acceleration for separation force
    :param boids: numpy array (N, 6) -> [x, y, vx, vy, ax, ay, class]
    :param i: id of a boid
    :param distance_mask: bool array of allowed boids (allowed by distance criteria for example)
    :return: velocity change (acceleration)
    """
    distance_mask[i] = False
    directions = boids[i, :2] - boids[distance_mask][:, :2]
    directions *= (1 / (njit_norm_axis1(directions).reshape(-1, 1) + 0.0001))
    acceleration = np.sum(directions, axis=0)
    return acceleration - boids[i, 2:4]


@njit
def cohesion(boids: np.ndarray, i: int, distance_mask: np.ndarray):
    """
    Calculates acceleration for cohesion force
    :param boids: numpy array (N, 6) -> [x, y, vx, vy, ax, ay, class]
    :param i: id of a boid
    :param distance_mask: bool array of allowed boids (allowed by distance criteria for example)
    :return: velocity change (acceleration)
    """
    directions = boids[distance_mask][:, :2]
    acceleration = (np.sum(directions, axis=0) / directions.shape[0]) - boids[i, :2]
    return acceleration - boids[i, 2:4]


@njit
def alignment(boids: np.ndarray, i: int, distance_mask: np.ndarray):
    """
    Calculates acceleration for alignment force
    :param boids: numpy array (N, 6) -> [x, y, vx, vy, ax, ay, class]
    :param i: id of a boid
    :param distance_mask: bool array of allowed boids (allowed by distance criteria for example)
    :return: velocity change (acceleration)
    """
    velocity = boids[distance_mask][:, 2:4]
    acceleration = np.sum(velocity, axis=0)
    acceleration /= velocity.shape[0]
    return acceleration - boids[i, 2:4]


@njit
def compute_walls_collisions(boids: np.ndarray, i: int, aspect_ratio: float, wall_bounce: bool):
    """
    Calculates behavior of boids in the event of wall collision, supports 2 behaviors:
    - bounce
    - teleportation to the other side
    :param wall_bounce: bool flag
    """
    mask_walls = np.empty(4)
    mask_walls[0] = boids[i, 1] > 1
    mask_walls[1] = boids[i, 0] > aspect_ratio
    mask_walls[2] = boids[i, 1] < 0
    mask_walls[3] = boids[i, 0] < 0

    if wall_bounce:
        if mask_walls[0]:
            boids[i, 3] = -boids[i, 3]
            boids[i, 1] = 1 - 0.001

        if mask_walls[1]:
            boids[i, 2] = -boids[i, 2]
            boids[i, 0] = aspect_ratio - 0.001

        if mask_walls[2]:
            boids[i, 3] = -boids[i, 3]
            boids[i, 1] = 0.001

        if mask_walls[3]:
            boids[i, 2] = -boids[i, 2]
            boids[i, 0] = 0.001
    else:
        if mask_walls[0]:
            boids[i, 1] = 0

        if mask_walls[1]:
            boids[i, 0] = 0

        if mask_walls[2]:
            boids[i, 1] = 1

        if mask_walls[3]:
            boids[i, 0] = aspect_ratio


@njit
def compute_walls_acceleration(boids: np.ndarray, i: int, aspect_ratio: float, perception: float, wall_bounce: bool):
    """
    Calculates acceleration for the smooth walls interactions (works alongside bounce-walls collision)
    """
    if wall_bounce:
        x, y = boids[i, 0:2]
        left_distance = np.abs(x + 0.01)
        right_distance = np.abs((aspect_ratio - x) - 0.01)
        top_distance = np.abs((1 - y) - 0.01)
        bottom_distance = np.abs(y + 0.01)
        a_left = a_right = a_top = a_bottom = 0.0

        if left_distance <= perception * 2:
            a_left = 1 / left_distance ** 2

        if right_distance <= perception * 2:
            a_right = 1 / right_distance ** 2

        if top_distance <= perception * 2:
            a_top = 1 / top_distance ** 2

        if bottom_distance <= perception * 2:
            a_bottom = 1 / bottom_distance ** 2

        return np.array([a_left - a_right, a_bottom - a_top]) - boids[i, 2:4]
    else:
        return np.zeros(2)


@njit(parallel=True)
def flocking(boids: np.ndarray, perception: float, coefficients: np.ndarray, aspect_ratio: float, a_range: np.ndarray, wall_bounce: bool):
    """
    Main function of the simulation. Calculates new acceleration values for boids
    :param boids: numpy array (N, 6) -> [x, y, vx, vy, ax, ay, class]
    :param perception: radius of perception for boids
    :param a_range: allowed acceleration range
    :param wall_bounce: bool flag
    """
    for i in prange(boids.shape[0]):
        # TODO: нечитаемый, но компактый говногод
        boid_class = int(boids[i, 6])
        class_coefficients = coefficients[boid_class * 2: (boid_class * 2) + 2]

        # Accelerations initialization
        a_separation = np.zeros(2)
        a_cohesion = np.zeros(2)
        a_alignment = np.zeros(2)
        a_walls = clip_vector(compute_walls_acceleration(boids, i, aspect_ratio, perception, wall_bounce), a_range) * class_coefficients[0, 3]
        a_noise = np.array([np.random.uniform(-0.1, 0.1), np.random.uniform(-0.1, 0.1)]) * class_coefficients[0, 4]

        # Walls collisions
        compute_walls_collisions(boids, i, aspect_ratio, wall_bounce)

        # Distance masks
        d = distance(boids, i)
        perception_mask = d < perception
        separation_mask = d < (perception / 2)
        separation_mask[i] = False
        cohesion_mask = np.logical_xor(perception_mask, separation_mask)
        alignment_mask = perception_mask
        alignment_mask[i] = False

        # Main interactions
        if np.any(perception_mask):
            for class_index in range(class_coefficients.shape[0]):
                # Class masks
                class_mask = boids[:, 6] == class_index
                class_separation_mask = np.logical_and(separation_mask, class_mask)
                class_cohesion_mask = np.logical_and(cohesion_mask, class_mask)
                class_alignment_mask = np.logical_and(alignment_mask, class_mask)

                if np.any(class_separation_mask):
                    a_separation += class_coefficients[class_index, 0] * separation(boids, i, class_separation_mask)
                if np.any(class_cohesion_mask):
                    a_cohesion += class_coefficients[class_index, 1] * cohesion(boids, i, class_cohesion_mask)
                if np.any(class_alignment_mask):
                    a_alignment += class_coefficients[class_index, 2] * alignment(boids, i, class_alignment_mask)

            a_separation = clip_vector(a_separation, a_range)
            a_cohesion = clip_vector(a_cohesion, a_range)
            a_alignment = clip_vector(a_alignment, a_range)

        acceleration = a_separation + a_cohesion + a_alignment + a_walls + a_noise
        boids[i, 4:6] = acceleration


def propagate(boids, delta_time, v_range):
    """
    Propagates velocitities -> positions of boids
    :param boids: numpy array (N, 6) -> [x, y, vx, vy, ax, ay, class]
    :param v_range: allowed velocity range
    """
    boids[:, 2:4] += boids[:, 4:6] * delta_time
    boids[:, 2:4] = clip_array(boids[:, 2:4], v_range)
    boids[:, 0:2] += boids[:, 2:4] * delta_time
