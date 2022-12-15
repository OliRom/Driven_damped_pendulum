import pandas as pd
import os
import Parameters as param
import Other_functions as of
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors
from scipy.fft import rfft, rfftfreq


def plot_teta_and_omega_vs_t():
    t_max = 30  # Afficher les données jusqu'à ce temps

    log_path = "sim_simple.csv"
    log_file = pd.read_csv(log_path)
    time_stamp = "2022_12_14_16_55_50_644538"
    sim_path = os.path.join(param.data_path, time_stamp + ".csv")
    data_file = pd.read_csv(sim_path)
    params = log_file[log_file["time_stamp"] == time_stamp]

    n_tps = int(params.iloc[0]["n_iter"])
    dt = params["dt"]
    index_max = int(t_max / dt) + 1

    t_range = [i*dt for i in range(n_tps)][:index_max+1]
    teta = data_file["teta"][:index_max + 1]
    omega = data_file["omega"][:index_max + 1]

    plt.plot(t_range, teta, label=r"$\theta$ (rad)")
    plt.plot(t_range, omega, label=r"$\omega$ (rad/s)")
    plt.title("Évolution du pendule en fonction du temps")
    plt.xlabel("Temps (s)")
    # plt.ylabel(r"$\theta$ (rad)")
    plt.legend()
    plt.show()


def plot_3d_teta_omega_vs_other_param():
    """
    Fonction incomplète et hardcodée
    :return:
    """
    variable_name = "damping"
    ajout_dans_le_titre = "du coefficient d'amortissement du pendule"
    y_label = r"$\beta$"

    path = "data_log.csv"
    temps = np.arange(0, 20.0005, 0.005)
    variable = [of.round_to_precision(x, 8) for x in [0]+list(np.linspace(0.01, 1, 100))+list(np.linspace(1, 10, 1000))]
    omega0 = [of.round_to_precision(x, 8) for x in np.linspace(0, 2, 100)]

    params = {variable_name: variable}
    paths = of.get_sim_names(path, params, variable_name)

    x = temps
    y = variable
    teta = np.zeros((len(x), len(y)))
    omega = np.zeros((len(x), len(y)))
    for i, path in enumerate(paths):
        full_path = os.path.join(param.data_path, path + ".csv")
        data = pd.read_csv(full_path)
        # first_teta = of.round_to_precision(data[0], 8)
        teta[:, i] = data["teta"]
        omega[:, i] = data["omega"]

    # Projection en 3D
    X, Y = np.meshgrid(x, y)
    ax = plt.axes(projection="3d")
    ax.plot_surface(X, Y, teta.T)
    ax.set_xlabel("Temps (s)")
    ax.set_ylabel(y_label)
    ax.set_zlabel(r"$\theta$ (rad)")
    plt.title(f"Évolution du pendule en fonction {ajout_dans_le_titre}")
    plt.show()

    # Affichage 3D avec de la couleur
    fig, axs = plt.subplots(1, 2)
    fig.suptitle(f"Évolution du pendule en fonction {ajout_dans_le_titre}", fontsize=20)

    teta = (teta + np.pi) % (2 * np.pi) - np.pi
    pc0 = axs[0].pcolormesh(X, Y, teta.T, cmap="twilight")
    axs[0].set_title("Angle avec la verticale")
    axs[0].set_xlabel("Temps (s)")
    axs[0].set_ylabel(y_label)
    cbar0 = fig.colorbar(pc0, ax=axs[0])
    cbar0.set_label(r"$\theta$ (rad)")

    pc1 = axs[1].pcolormesh(X, Y, omega.T)
    axs[1].set_title("Vitesse angulaire")
    axs[1].set_xlabel("Temps (s)")
    axs[1].set_ylabel(y_label)
    cbar1 = fig.colorbar(pc1, ax=axs[1])
    cbar1.set_label(r"$\omega$ (rad/s)")

    plt.subplots_adjust(hspace=1, left=0.05, right=0.95)
    plt.show()


def plot_bifurcation():
    def interesting_time_indexes(dt, ang_freq, max_t):
        first_index = 20 / dt  # Commencer 20 secondes après le début pour laisser le temps de stabiliser
        n_t_per_period = round(2 * np.pi / (dt * ang_freq))
        n_period = max_t * ang_freq / (2 * np.pi)
        indexes = [i * n_t_per_period for i in range(int(n_period+1)) if max_t / dt > i * n_t_per_period > first_index]
        return indexes

    gamma = [of.round_to_precision(g, 8) for g in np.linspace(1.06, 1.53, 10000)]
    driving_ang_freq = 2 * np.pi

    path = "bifurcation_log.csv"
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

    plt.title(r"Diagramme de bifurcation pour $\gamma$ allant de 1,06 à 1,53")
    plt.xlabel(r"$\gamma$")
    plt.ylabel(r"$\theta$ (rad)")
    plt.show()


def plot_espace_phase():
    t_max = 50  # Afficher les données jusqu'à ce temps
    dt = 0.005
    line_width = 0.5

    index_max = int(t_max/dt) + 1

    time_stamp = "phase_g1p1"
    sim_path = os.path.join(param.data_path, time_stamp + ".csv")
    data_file = pd.read_csv(sim_path)

    teta = data_file["teta"][:index_max + 1]
    omega = data_file["omega"][:index_max + 1]

    plt.plot(teta, omega, linewidth=line_width)

    plt.title("Espace des phases du pendule")
    plt.xlabel(r"$\theta$ (rad)")
    plt.ylabel(r"$\omega$ (rad/s)")
    plt.axhline(0, color="gray", linewidth=1)
    plt.axvline(0, color="gray", linewidth=1)
    plt.show()


def plot_fft_simple():
    time_stamp = "2022_12_14_16_54_50_256710"
    n_tps = 20001
    dt = 0.005
    signal_x_max = 20  # Temps maximal du signal à afficher
    fft_x_max = 10  # Fréquence maximale à afficher

    sim_path = os.path.join(param.data_path, time_stamp + ".csv")
    data_file = pd.read_csv(sim_path)

    temps = np.arange(0, n_tps*dt, dt)
    teta = data_file["teta"].tolist()
    xfft = rfftfreq(n_tps, dt)
    yfft = rfft(teta) / n_tps * 2  # 2/n_tps est pour normaliser le spectre

    fig, axs = plt.subplots(1, 2)
    fig.suptitle("Transformée de Fourier de l'angle du pendule avec la verticale", fontsize=20)

    axs[0].set_title("Angle avec la verticale")
    axs[0].set_xlabel("Temps (s)")
    axs[0].set_ylabel(r"$\theta$ (rad/s)")
    axs[0].plot(temps, teta)
    if signal_x_max is not None:
        axs[0].set_xlim(xmin=-1, xmax=signal_x_max)

    axs[1].set_title("Transformée de Fourier")
    axs[1].set_xlabel("Fréquence (Hz)")
    axs[1].set_ylabel("Amplitude")
    axs[1].plot(xfft[1:], np.abs(yfft)[1:])
    axs[1].set_yscale("log")
    if fft_x_max is not None:
        axs[1].set_xlim(xmin=0, xmax=fft_x_max)

    plt.show()


def plot_fft_multiple():
    variable = [of.round_to_precision(gam, 8) for gam in np.linspace(1.06, 1.53, 10000)]
    variable = [variable[i*10] for i in range(1000)]
    variable_name = "gamma"
    ajout_dans_le_titre = "l'amplitude de la force externe"
    y_label = r"$\gamma$"
    temps = [of.round_to_precision(t, 8) for t in np.arange(0, 100.0005, 0.005)]

    log_path = "bifurcation_log.csv"

    n_iter = len(temps)
    dt = temps[1] - temps[0]
    params = {variable_name: variable, "dt": [dt], "n_iter": [n_iter]}
    paths = of.get_sim_names(log_path, params)  # , variable_name)

    log_file = pd.read_csv(log_path)
    ordered_paths = log_file[log_file["time_stamp"].isin(paths)].sort_values(variable_name)["time_stamp"]

    print("Getting data...")
    x = rfftfreq(n_iter, dt)
    y = variable
    z = np.zeros((len(x), len(y)))
    for i, path in enumerate(ordered_paths):
        data_path = os.path.join(param.data_path, path+".csv")
        data = pd.read_csv(data_path)
        z[:, i] = abs(rfft(data["teta"].tolist())) / n_iter * 2

    X, Y = np.meshgrid(x, y)
    fig, ax = plt.subplots()
    ax.set_title(f"Transformée de Fourier de l'angle du pendule en fonction de {ajout_dans_le_titre}")
    ax.set_xlabel("Fréquence (Hz)")
    ax.set_ylabel(y_label)
    ax.set_xlim(xmin=0, xmax=10)
    pc = ax.pcolormesh(X, Y, z.T, norm=colors.LogNorm(vmin=1e-3))
    cbar = fig.colorbar(pc)
    cbar.set_label("Amplitude")
    plt.show()


plot_fft_simple()
