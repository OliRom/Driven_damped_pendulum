import numpy as np
import Other_functions as of
import pandas as pd
import Parameters as param
import os
import matplotlib.pyplot as plt


class Pendulum:
    def __init__(self, teta, omega, t_range, gamma, driving_ang_freq, driving_delta, l, m, damping, g, log_path,
                 ignore_simulated=False):
        """
        Initialisation des paramètres du pendule
        :param teta: Angle initial du pendule
        :param omega: Vitesse angulaire initiale du pendule
        :param t_range: Temps sur lesquels intégrer
        :param gamma: Grandeur de la force qui drive le pendule (F0 = gamma m g)
        :param driving_ang_freq: Fréquence (rad/s) de la force qui drive le pendule
        :param driving_delta: Décalage (rad) de la force qui drive le pendule
        :param l: Longueur du pendule
        :param m: Masse du pendule
        :param damping: Amortissement du pendule (multiple de g)
        :param g: Accélération gravitationnelle
        :param log_path: Path du fichier où enregistrer les données à la fin d'une simulation
        :param ignore_simulated: True s'il faut ignorer un pendule qui a déjà été simulé avec les mêmes paramètres
        """
        self.n_iter = len(t_range)  # Nombre total d'itération d'intégrations à effectuer
        self.iteration = 1  # Iteration d'intégration à laquelle le programme est rendu

        self.temps = np.array(t_range)
        self.dt = self.temps[1] - self.temps[0]

        self.teta = np.empty(self.n_iter)
        self.omega = np.empty(self.n_iter)

        self.gamma = gamma
        self.driving_force = gamma * m * g
        self.driving_ang_freq = driving_ang_freq
        self.driving_delta = driving_delta

        self.l = l
        self.m = m
        self.g = g
        self.damping = damping

        self.teta[0] = teta
        self.omega[0] = omega

        self.log_path = log_path
        self.ignore_simulated = ignore_simulated
        self.already_simulated = self.is_already_simulated()

    def driving_function(self, t):
        """
        Méthode qui retourne la fonction qui modélise la force qui drive le pendule.
        :return: La fonction qui modélise la force qui drive le pendule.
        """
        return self.driving_force * np.cos(self.driving_ang_freq * t + self.driving_delta)

    def evolute_one_step(self):
        """
        Fait évoluer l'état du pendule d'un intervalle de temps.
        :return: None
        """
        i = self.iteration
        t = self.temps[i]

        force = self.driving_function(t + self.dt/2)
        g = self.g
        beta = self.damping * g

        omega_prevu = self.omega[i-1]
        self.teta[i] = self.teta[i-1] + omega_prevu * self.dt

        # Intégration par saute-mouton pour éviter les erreurs de l'intégration numérique
        if i % 2 == 1:
            teta_prevu = 2 * self.teta[i] - self.teta[i-1]
        else:
            teta_prevu = self.teta[i-1]
        # self.omega[i] = self.omega[i-1] + ((force - beta * omega_prevu) / (self.m * self.l**2) - g * np.sin(teta_prevu) / self.l) * self.dt
        w0 = np.sqrt(self.g/self.l)
        self.omega[i] = self.omega[i-1] + (self.gamma * w0**2 * np.cos(self.driving_ang_freq*t)-self.damping/self.m*self.omega[i-1]-w0**2*np.sin(teta_prevu)) * self.dt

        self.iteration += 1

    def evolute_to_end(self):
        """
        Fait évoluer le pendule jusqu'à la fin du range de temps initialisé.
        :return: None
        """
        if self.already_simulated:
            return

        while self.iteration < self.n_iter:
            self.evolute_one_step()

        self.save_data()

    def save_data(self):
        """
        Enregistre les données sur l'évolution du pendule dans un fichier .csv et ajoute la simulation dans le fichier
        self.log_path .
        :return: None
        """
        if self.already_simulated:
            return

        params = self.get_params()
        # Ligne à ajouter dans le fichier de log pour garder une trace
        param_stamp = ",".join([str(of.round_to_precision(params[p], 8)) for p in param.log_file_column_names])
        time_stamp = of.get_saving_name()

        col_names = ["t", "teta", "omega"]
        data = [self.temps, self.teta, self.omega]

        df = pd.DataFrame({cn: dt for cn, dt in zip(col_names, data)})
        df.to_csv(os.path.join(param.data_path, time_stamp + ".csv"), sep=',', header=col_names, index=False)

        log_string = time_stamp + "," + param_stamp + "\n"
        with open(self.log_path, "a") as writer:
            writer.write(log_string)

    def get_params(self):
        """
        Méthode qui retourne un dictionnaire contenant les paramètres du pendule.
        :return: Dictionnaire qui contient les paramètres du pendule
        """
        dic = {
            "teta0": self.teta[0],
            "omega0": self.omega[0],
            "dt": self.dt,
            "n_iter": self.n_iter,
            "gamma": self.gamma,
            "driving_ang_freq": self.driving_ang_freq,
            "driving_delta": self.driving_delta,
            "l": self.l,
            "m": self.m,
            "damping": self.damping,
            "g": self.g,
        }

        return dic

    def is_already_simulated(self):
        """
        Fonction qui vérifie si la simulation a déjà été effectuée avec les paramètres initiaux.
        :return: True si déjà simulée, False sinon
        """
        if self.ignore_simulated:
            return False

        params = self.get_params()
        # Ligne ajoutée dans le fichier de log pour garder une trace
        param_stamp = ",".join([str(of.round_to_precision(params[p], 8)) for p in param.log_file_column_names])

        with open(self.log_path, "r") as reader:
            for line in reader.readlines():
                if line.strip().endswith(param_stamp):
                    return True

        return False

    def plot_teta_t(self):
        plt.plot(self.temps, self.teta)

        w0 = np.sqrt(self.g/self.l)
        force = [self.gamma * w0**2 * np.cos(self.driving_ang_freq*t) for t in self.temps]
        # plt.plot(self.temps, force)

        plt.show()
