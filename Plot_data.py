import pandas as pd
import os
import Parameters as param
import Other_functions as of
import numpy as np
import matplotlib.pyplot as plt

if __name__ == "__main__":
    path = "test_log.csv"
    temps = np.arange(0, 10.005, 0.01)
    teta0 = [of.round_to_precision(x, 5) for x in np.linspace(0, np.pi / 4, 100)]
    omega0 = [of.round_to_precision(x, 5) for x in np.linspace(0, 2, 100)]

    params = {"teta0": teta0, "omega0": omega0}
    paths = of.get_sim_names(path, params)

    x = temps
    y = teta0
    z = np.zeros((len(x), len(y)))
    for path in paths:
        full_path = os.path.join(param.data_path, path + ".csv")
        data = pd.read_csv(full_path)["teta"]
        first_teta = of.round_to_precision(data[0], 5)
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
