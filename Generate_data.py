from Pendule_class import Pendulum
import numpy as np
import multiprocessing as mp
import Other_functions as of
import time
import Parameters as param


def caller(obj):
    # delay = np.random.rand()
    # time.sleep(delay / 10)
    obj.evolute_to_end()


nb_process = 6

t_range = [of.round_to_precision(t, 8) for t in np.arange(0, 100.0005, 0.005)]
teta = -np.pi / 4
omega = 0
gamma = 0
# gamma = [of.round_to_precision(gam, 8) for gam in np.linspace(1.06, 1.53, 10000)]
driving_ang_freq = 2 * np.pi
driving_delta = 0
l = 9.8/9/np.pi**2
m = 1  #
g = 9.8
damping = m / 2 * np.sqrt(g/l) * 0
log_path = "sim_simple.csv"

# variable = [of.round_to_precision(var, 8) for var in np.linspace(1.06, 1.087, 1000)]
variable = [1.5]

# gamma = [1.073]
# l = 1
# damping = 0
# t_range = np.arange(0, 100, 0.01)


if __name__ == "__main__":
    pendules = [None] * len(variable)
    for i, var in enumerate(variable):
        pendules[i] = Pendulum(teta, omega, t_range, var, driving_ang_freq, driving_delta, l, m,
                               damping, g, log_path)

    print("Working...")
    with mp.Pool(nb_process) as p:
        results = p.map(caller, pendules)

    print("Cleaning simulations...")
    of.delete_bad_sims(log_path, param.data_path)
