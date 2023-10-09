import matplotlib.pyplot as plt
import numpy as np
from numba import njit, prange


def mandelbrot_escape_proto(c: complex, r: float = 2.0, max_it: int = 100) -> int:
    z = 0.0 + 0.0j

    i = 0
    for i in range(max_it):
        z = z**2 + c
        if abs(z) > r:
            break

    return i

def mandelbrot_proto(
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    nx: int = 200,
    ny: int = 200,
    r: float = 2.0,
    max_it: int = 100
) -> list[list[int]]:
    dx = (xmax - xmin) / nx
    dy = (ymax - ymin) / ny

    res = []

    for iy in range(ny + 1):
        res.append([])
        for ix in range(nx + 1):
            x = xmin + dx * ix
            y = ymin + dy * iy
            c = x + y * 1j
            it = mandelbrot_escape_proto(c, r=r, max_it=max_it)
            res[-1].append(it)

    return res

img = mandelbrot_proto(
    -1.5, 0.5,
    -1.0, 1.0,
)

plt.figure()
plt.pcolormesh(img)
plt.axis('equal')
plt.colorbar()
plt.tight_layout(pad=1.0)
plt.show()


@njit
def mandelbrot_escape_njit(c: complex, r: float = 2.0, max_it: int = 100) -> int:
    z = 0.0 + 0.0j

    i = 0
    for i in range(max_it):
        z = z**2 + c
        if abs(z) > r:
            break

    return i


@njit
def mandelbrot_proto_njit(
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    nx: int = 200,
    ny: int = 200,
    r: float = 2.0,
    max_it: int = 100
) -> np.ndarray:
    dx = (xmax - xmin) / nx
    dy = (ymax - ymin) / ny

    res = np.empty((ny+1, nx+1), dtype=np.uint16)

    for iy in range(ny + 1):
        for ix in range(nx + 1):
            x = xmin + dx * ix
            y = ymin + dy * iy
            c = x + y * 1j
            it = mandelbrot_escape_njit(c, r=r, max_it=max_it)
            res[iy, ix] = it

    return res


img_njit = mandelbrot_proto_njit(
    -1.5, 0.5,
    -1.0, 1.0,
)

print('eps = ', np.linalg.norm(img - img_njit))


@njit(parallel=True)
def mandelbrot_proto_par(
    xmin: float,
    xmax: float,
    ymin: float,
    ymax: float,
    nx: int = 200,
    ny: int = 200,
    r: float = 2.0,
    max_it: int = 100
) -> np.ndarray:
    dx = (xmax - xmin) / nx
    dy = (ymax - ymin) / ny

    res = np.empty((ny+1, nx+1), dtype=np.uint16)

    for iy in prange(ny + 1):
        for ix in range(nx + 1):
            x = xmin + dx * ix
            y = ymin + dy * iy
            c = x + y * 1j
            it = mandelbrot_escape_njit(c, r=r, max_it=max_it)
            res[iy, ix] = it

    return res


img_par = mandelbrot_proto_par(
    -1.5, 0.5,
    -1.0, 1.0,
)