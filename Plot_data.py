import pandas as pd
import os
import Parameters as param
import Other_functions as of
import numpy as np
import matplotlib.pyplot as plt
from scipy.fft import rfft, rfftfreq


def plot_teta_and_omega_vs_t():
    t_max = 30  # Afficher les données jusqu'à ce temps

    log_path = "test_log.csv"
    log_file = pd.read_csv(log_path)
    time_stamp = "2022_12_13_13_08_01_974951"
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
    variable_name = "teta0"
    ajout_dans_le_titre = "l'angle initial (rad)"
    y_label = r"$\theta_0$ (rad)"

    path = "test_log.csv"
    temps = np.arange(0, 10.005, 0.01)
    variable = [of.round_to_precision(x, 8) for x in np.linspace(0, np.pi / 4, 100)]
    # omega0 = [of.round_to_precision(x, 8) for x in np.linspace(0, 2, 100)]

    params = {variable_name: variable}
    paths = of.get_sim_names(path, params)

    x = temps
    y = variable
    teta = np.zeros((len(x), len(y)))
    omega = np.zeros((len(x), len(y)))
    for path in paths:
        full_path = os.path.join(param.data_path, path + ".csv")
        data = pd.read_csv(full_path)
        first_teta = of.round_to_precision(data[0], 8)
        teta[:, y.index(first_teta)] = data["teta"]
        omega[:, y.index(first_teta)] = data["omega"]

    # Projection en 3D
    X, Y = np.meshgrid(x, y)
    ax = plt.axes(projection="3d")
    ax.plot_surface(X, Y, teta.T)
    ax.set_xlabel("Temps (s)")
    ax.set_ylabel(y_label)
    ax.set_zlabel(r"$\theta$ (rad)")
    plt.title(f"Évolution du pendule en fonction de {ajout_dans_le_titre}")
    plt.show()

    # Affichage 3D avec de la couleur
    fig, axs = plt.subplots(1, 2)
    fig.suptitle(f"Évolution du pendule en fonction de {ajout_dans_le_titre}", fontsize=20)

    pc0 = axs[0].pcolormesh(X, Y, teta.T)
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

    gamma = [of.round_to_precision(g, 8) for g in np.linspace(1.06, 1.087, 200)]
    driving_ang_freq = 2 * np.pi

    path = "test_log.csv"
    log_file = pd.read_csv(path)

    params = {"gamma": gamma}
    paths = of.get_sim_names(path, params)

    time_indexes = interesting_time_indexes(0.005, driving_ang_freq, 1000.0005)
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

    plt.title(r"Diagramme de bifurcation pour $\gamma$ allant de 1.06 à ???")
    plt.xlabel(r"$\gamma$")
    plt.ylabel(r"$\theta$ (rad)")
    plt.show()


def plot_espace_phase():
    t_max = 50  # Afficher les données jusqu'à ce temps
    dt = 0.005
    line_width = 0.5

    index_max = int(t_max/dt) + 1

    time_stamp = "2022_12_13_13_08_01_974951"
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
    time_stamp = "2022_12_13_13_08_01_974951"
    n_tps = 200001
    dt = 0.005
    signal_x_max = 30  # Temps maximal du signal à afficher
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
    if fft_x_max is not None:
        axs[1].set_xlim(xmin=0, xmax=fft_x_max)

    plt.show()


def plot_fft_multiple():
    pass


plot_fft_simple()
