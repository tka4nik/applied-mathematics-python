import numpy as np
from numba import njit, prange

@njit(cache=True)
def mandelbrot_point_njit(c, maxit=1000):
    z = 0.0 + 0.0j
    i = 0
    for i in range(maxit):
        z = z**2 + c
        if abs(z) > 2:
            break
    return i

@njit(parallel=True, cache=True)
def mandelbrot_par(xmin, xmax, ymin, ymax, nx, ny, maxit=1000):
    dx = (xmax - xmin) / nx
    dy = (ymax - ymin) / ny
    res = np.empty((ny+1, nx+1), dtype=np.int32)

    for iy in prange(ny + 1):
        for ix in range(nx + 1):
            x = xmin + dx * ix
            y = ymin + dy * iy
            c = x + 1j * y
            it = mandelbrot_point_njit(c, maxit)
            res[iy, ix] = it

    return res