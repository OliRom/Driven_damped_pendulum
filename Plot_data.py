import pandas as pd
import os
import Parameters as param
import Other_functions as of
import numpy as np
import matplotlib.pyplot as plt


def plot_teta_vs_t():
    log_path = "test_log.csv"
    log_file = pd.read_csv(log_path)
    time_stamp = "2022_12_13_11_49_02_824007"
    sim_path = os.path.join(param.data_path, time_stamp + ".csv")
    data_file = pd.read_csv(sim_path)
    params = log_file[log_file["time_stamp"] == time_stamp]

    n_tps = int(params.iloc[0]["n_iter"])
    dt = params["dt"]
    t_range = [i*dt for i in range(n_tps)]

    y = data_file["teta"]

    plt.plot(t_range, y)
    plt.show()


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
        first_index = 20 / dt  # Commencer 10 secondes après le début pour laisser le temps de stabiliser
        n_t_per_period = round(2 * np.pi / (dt * ang_freq))
        n_period = max_t * ang_freq / (2 * np.pi)
        indexes = [i * n_t_per_period for i in range(int(n_period+1)) if max_t / dt > i * n_t_per_period > first_index]
        return indexes

    gamma = [of.round_to_precision(g, 8) for g in np.linspace(1.06, 1.53, 10000)]
    driving_ang_freq = 2 * np.pi

    path = "test_log.csv"
    log_file = pd.read_csv(path)

    params = {"gamma": gamma}
    paths = of.get_sim_names(path, params)

    time_indexes = interesting_time_indexes(0.005, driving_ang_freq, 100.0005)
    x = np.zeros(len(paths))
    y = np.zeros((len(x), len(time_indexes)))

    print("Getting data...")

    if len(paths) == 0:
        print("No simulations found")

    for i, path in enumerate(paths):
        full_path = os.path.join(param.data_path, path + ".csv")
        data = pd.read_csv(full_path)["teta"]
        # print(path)
        x[i] = log_file[log_file["time_stamp"] == path]["gamma"]
        y[i, :] = ((data[time_indexes] + np.pi) % (2 * np.pi) - np.pi)

    print("Plotting data...")
    for i in range(len(time_indexes)):
        plt.plot(x, y[:, i], color="blue", marker=',', lw=0, linestyle="")
    plt.show()


# plot_teta_vs_t()
plot_bifurcation()
