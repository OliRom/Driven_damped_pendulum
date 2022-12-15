import os

import pandas as pd

import Pendule_class as pc
import Other_functions as of
import numpy as np
import Parameters as param


# log_file = "bifurcation_log.csv"
# log_file = pd.read_csv(log_file)["time_stamp"]
# for f in log_file:
#     try:
#         path = os.path.join(param.data_path, f+".csv")
#         os.remove(path)
#     except:
#         print(f)

exit()

teta = -np.pi / 2
omega = 0
t_range = [of.round_to_precision(t, 8) for t in np.arange(0, 30.0005, 0.005)]
gamma = [of.round_to_precision(gam, 8) for gam in np.linspace(0.5, 2, 500)]
driving_ang_freq = np.pi*2
driving_delta = 0
l = 9.8/9/np.pi**2
m = 1  #
g = 9.8
damping = m / 2 * np.sqrt(g/l)
log_path = "test_log.csv"

for i in [1.065]:
    gamma = i

    pendule = pc.Pendulum(teta, omega, t_range, gamma, driving_ang_freq, driving_delta, l, m, damping, g, "test_log.csv", True)
    pendule.evolute_to_end()
    pendule.plot_teta_t()

