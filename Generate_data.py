from Pendule_class import Pendulum
import numpy as np
import pathos.multiprocessing as mp


nb_process = 6

teta = 0
omega = 1
t_range = np.arange(0, 1000.005, 0.01)
driving_force = 2
driving_ang_freq = 3
driving_delta = 0
l = 1
m = 1
damping = np.linspace(1.060, 1.087, 1000)
g = 9.8
log_path = "test_log.csv"

if __name__ == "__main__":
    def caller(obj):
        obj.evolute_to_end()


    pendules = [None] * len(damping)
    for i, damp in enumerate(damping):
        pendules[i] = Pendulum(teta, omega, t_range, driving_force, driving_ang_freq, driving_delta, l, m,
                               damp, g, log_path)

    print("Working...")
    with mp.Pool(nb_process) as p:
        results = p.map(caller, pendules)
