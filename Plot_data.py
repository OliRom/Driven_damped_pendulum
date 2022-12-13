import pandas as pd
import os
import Parameters as param
import Other_functions as of
import numpy as np
import matplotlib.pyplot as plt


def plot_3d():
    """
    Fonction incomplète et hardcodée
    :return:
    """
    path = "test_log.csv"
    temps = np.arange(0, 10.005, 0.01)
    teta0 = [of.round_to_precision(x, 8) for x in np.linspace(0, np.pi / 4, 100)]
    omega0 = [of.round_to_precision(x, 8) for x in np.linspace(0, 2, 100)]

    params = {"teta0": teta0, "omega0": omega0}
    paths = of.get_sim_names(path, params)

    x = temps
    y = teta0
    z = np.zeros((len(x), len(y)))
    for path in paths:
        full_path = os.path.join(param.data_path, path + ".csv")
        data = pd.read_csv(full_path)["teta"]
        first_teta = of.round_to_precision(data[0], 8)
        z[:, y.index(first_teta)] = data

    X, Y = np.meshgrid(x, y)
    ax = plt.axes(projection="3d")
    ax.plot_surface(X, Y, z.T)
    ax.set_xlabel("temps")
    ax.set_ylabel("teta 0")
    plt.show()

    fig, ax = plt.subplots()
    pc = ax.pcolormesh(X, Y, z.T)
    ax.set_xlabel("temps")
    ax.set_ylabel("teta 0")
    fig.colorbar(pc)
    plt.show()


def plot_bifurcation():
    def interesting_time_indexes(dt, ang_freq, max_t):
        first_index = 200 / dt  # Commencer 200 secondes après le début pour laisser le temps de stabiliser
        n_t_per_period = int(2 * np.pi / (dt * ang_freq))
        n_period = max_t * ang_freq / (2 * np.pi)
        indexes = [i * n_t_per_period for i in range(int(n_period+1)) if max_t / dt > i * n_t_per_period > first_index]
        return indexes

    path = "test_log.csv"
    log_file = pd.read_csv(path)

    damping = [of.round_to_precision(d, 5) for d in np.linspace(1.060, 1.087, 1000)]

    params = {"damping": damping}
    paths = of.get_sim_names(path, params)

    time_indexes = interesting_time_indexes(0.01, 3, 1000.005)
    x = np.zeros(len(paths))
    y = np.zeros((len(x), len(time_indexes)))

    print("Getting data...")
    for i, path in enumerate(paths):
        full_path = os.path.join(param.data_path, path + ".csv")
        data = pd.read_csv(full_path)["omega"]
        print(full_path)
        x[i] = log_file[log_file["time_stamp"] == path]["damping"]
        y[i, :] = data[time_indexes]

    print("Plotting...")
    for i in range(len(time_indexes)):
        plt.plot(x, y[:, i], color="blue", marker=',', lw=0, linestyle="")
    plt.show()


plot_bifurcation()
