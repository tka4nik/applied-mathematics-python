import taichi as ti
import taichi_glsl as ts
import time

ti.init(arch=ti.gpu)

aspect_ratio = 16/9
height = 600
width = int(aspect_ratio * height)
resolution = width, height
resolution_float = ts.vec2(float(width), float(height))

pixels = ti.Vector.field(3, dtype=ti.f32, shape=resolution)


@ti.func
def rotate(angle):
    c = ti.cos(angle)
    s = ti.sin(angle)
    return ts.mat([c, -s], [s, c])

@ti.kernel
def render(t: ti.f32):
    # colour_0 = ts.vec3(255., 131., 137.) / 255.0

    for fragCoord in ti.grouped(pixels):
        uv = (fragCoord - 0.5 * resolution_float) / resolution_float[1]
        uv *= 10.0

        m = rotate(0.1*t)
        uv = uv @ m

        frac_uv = ts.fract(uv) - 0.5

        grid = ts.smoothstep(ti.abs(frac_uv).max(), 0.4, 0.5)
        col = ts.vec3(0.)
        col += ts.vec3(1.) * grid

        pixels[fragCoord] = ts.clamp(col, 0., 1.)


if __name__ == "__main__":
    gui = ti.GUI("Taichi basic shader", res=resolution, fast_gui=True)

    start = time.time()
    while gui.running:
        if gui.get_event(ti.GUI.PRESS):
            if gui.event.key == ti.GUI.ESCAPE:
                break
        delta_time = time.time() - start

        render(delta_time)
        gui.set_image(pixels)
        gui.show()
    gui.close()

