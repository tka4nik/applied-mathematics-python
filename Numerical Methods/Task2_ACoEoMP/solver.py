import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

from IPython.display import clear_output


def update_pde_solution(
    u, time, eqs, bcs, ics, grid
):
    # Находим b_i
    Func = eqs.get("F")

    u_prev = u[:-2]
    u_now = u[1:-1]
    u_next = u[2:]

    b = (Func(u_prev) + Func(u_now) + Func(u_next)) / 3

    # Находим eps, tau, h
    eps = eqs.get("eps")
    tau = grid.get("tau")
    h = grid.get("h")

    # Находим коэффициенты для явной схемы
    c_prev = (b * tau) / h + (eps * tau) / (h ** 2)
    c_now = 1 - (b * tau) / h - (2 * eps * tau) / (h ** 2)
    c_next = (eps * tau) / (h ** 2)

    # Делаем шаг по времени
    u_t = np.zeros_like(u)

    u_t[0] = bcs.get("u_left")
    u_t[-1] = bcs.get("u_right")
    u_t[1:-1] = c_prev * u_prev + c_now * u_now + c_next * u_next

    time += tau
    return u_t, time


def solve_pde(
    eqs, bcs, ics, grid_params, 
    frames=250, steps_per_frame=10
) -> dict:
    N = grid_params.get("N")
    a, b = bcs.get("a"), bcs.get("b")
    x_arr = np.linspace(a, b, N+1)
    grid_params["h"] = np.diff(x_arr)[0]


    time_arr = np.array([0.0])
    u_arr = ics.get("u0")(x_arr).reshape(1, -1)
    u_arr = u_arr.astype(float)

    for _ in range(frames):
        u_new = u_arr[-1]
        time = time_arr[-1]

        for _ in range(steps_per_frame):
            u_new, time = update_pde_solution(
                u_new, time, eqs, bcs, ics, grid_params,
            )
        
        u_new = u_new.reshape(1, -1)
        u_arr = np.concatenate((u_arr, u_new), axis=0)
        time_arr = np.append(time_arr, time)
    
    return {"u": u_arr, "times": time_arr, "x": x_arr}


def write_animation(
    solution_dict, eqs, bcs, ics, grid_params, path, fps=15, title=None
) -> None:
    u = solution_dict.get("u")
    x = solution_dict.get("x")
    times = solution_dict.get("times")

    eps = eqs.get("eps")
    n_t = times.size

    if title is None:
        title = f"u(x, t) eps={eps}"

    def initial_plot():
        plt.clf()
        plt.plot(x, u[0], color="lime", label=f"t=0.000")
        plt.title(title)
        plt.legend(loc='lower left')
        plt.grid(True)

    def update_plot(frame):
        t = times[frame]
        plt.clf()
        plt.plot(x, u[frame], color="lime", label=f"t={t:.3f}")
        plt.title(title)
        plt.legend(loc='lower left')
        plt.grid(True)

    fig, ax = plt.subplots()
    ani = animation.FuncAnimation(
        fig, update_plot, frames=n_t, init_func=initial_plot
    )

    FFwriter = FFwriter = animation.FFMpegWriter(fps=fps)
    ani.save(path, writer=FFwriter)


if __name__ == "__main__":
    eqs = {
        "F": lambda u: u*u,
        "eps": 0.1
    }

    u_left = np.pi / 2
    u_right = 3 * np.pi / 2

    bcs = {
        "a": 0,
        "b": 6,
        "u_left": u_left,
        "u_right": u_right
    }

    ics = {
        "u0": lambda x: np.where(x < 3, u_left, u_right)
    }

    # Оптимальные значения (желательно не трогать =))
    grid_params = {
        "tau": 0.0001,
        "N": 700
    }

    sol = solve_pde(
        eqs=eqs, bcs=bcs, ics=ics, grid_params=grid_params,
        frames=500, steps_per_frame=500
    )

    write_animation(
        sol, eqs, bcs, ics, grid_params, 
        path="Animations/square-b.mp4", fps=20,
        title=f"u(x, t)  $\epsilon$={eqs['eps']:.2f}  $F(u)=u*u$"
    )

