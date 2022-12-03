from Pendule_class import Pendulum
import numpy as np

teta = 0
omega = 0
t_range = np.arange(0, 100, 0.1)
driving_force = 0.1
driving_ang_freq = 3
driving_delta = 0
l = 1
m = 1
damping = 0.1
g = 9.8
log_path = "test_log.csv"

pendule = Pendulum(teta, omega, t_range, driving_force, driving_ang_freq, driving_delta, l, m, damping, g, log_path)

pendule.evolute_to_end()
