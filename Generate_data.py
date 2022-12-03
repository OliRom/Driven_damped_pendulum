from Pendule_class import Pendulum
import numpy as np

teta = np.linspace(0, np.pi/4, 100)
omega = 2
t_range = np.arange(0, 10.005, 0.01)
driving_force = np.linspace(0, 2, 100)
driving_ang_freq = 3
driving_delta = 0
l = 1
m = 1
damping = 0.1
g = 9.8
log_path = "test_log.csv"

for t, force in zip(teta, driving_force):
    print(t, force)
    pendule = Pendulum(t, omega, t_range, force, driving_ang_freq, driving_delta, l, m, damping, g, log_path)
    if not pendule.already_simulated:
        pendule.evolute_to_end()
