import numpy as np
import Other_functions as of
import pandas as pd
import Parameters as param


class Pendulum:
    def __init__(self, teta, omega, t_range, driving_force, driving_ang_freq, driving_delta, l, m, damping, g, log_path):
        """
        Initialisation des paramètres du pendule
        :param teta: Angle initial du pendule
        :param omega: Vitesse angulaire initiale du pendule
        :param t_range: Temps sur lesquels intégrer
        :param driving_force: Grandeur de la force qui drive le pendule
        :param driving_ang_freq: Fréquence (rad/s) de la force qui drive le pendule
        :param driving_delta: Décalage (rad) de la force qui drive le pendule
        :param l: Longueur du pendule
        :param m: Masse du pendule
        :param damping: Amortissement du pendule (multiple de g)
        :param g: Accélération gravitationnelle
        :param log_path: Path du fichier où enregistrer les données à la fin d'une simulation
        """
        self.n_iter = len(t_range)  # Nombre total d'itération d'intégrations à effectuer
        self.iteration = 0  # Iteration d'intégration à laquelle le programme est rendu

        self.temps = np.array(t_range)
        self.dt = self.temps[0] - self.temps[1]

        self.teta = np.empty(self.n_iter)
        self.omega = np.empty(self.n_iter)

        self.driving_force = driving_force
        self.driving_ang_freq = driving_ang_freq
        self.driving_delta = driving_delta
        self.driving_function = self.get_driving_function()

        self.l = l
        self.m = m
        self.g = g
        self.damping = damping

        self.teta[0] = teta
        self.omega[0] = omega

        self.log_path = log_path

    def get_driving_function(self):
        """
        Méthode qui retourne la fonction qui modélise la force qui drive le pendule.
        :return: La fonction qui modélise la force qui drive le pendule.
        """
        def function(t):
            return self.driving_force * np.cos(self.driving_ang_freq * t + self.driving_delta)

        return function

    def evolute_one_step(self):
        """
        Fait évoluer l'état du pendule d'un intervalle de temps.
        :return: None
        """
        i = self.iteration

        force = self.driving_force(self.temps[i])

        self.teta[i] = 0  # Équation du mouvement à remplacer
        self.omega[i] = 0  # Équation du mouvement à remplacer

        self.iteration += 1

    def evolute_to_end(self):
        """
        Fait évoluer le pendule jusqu'à la fin du range de temps initialisé.
        :return: None
        """
        while self.iteration < self.n_iter:
            self.evolute_one_step()

        self.save_data()

    def save_data(self):
        """
        Enregistre les données sur l'évolution du pendule dans un fichier .csv et ajoute la simulation dans le fichier
        self.log_path .
        :return: None
        """
        params = self.get_params()
        # Ligne à ajouter dans le fichier de log pour garder une trace
        param_stamp = str([params[p] for p in param.log_file_column_names])
        time_stamp = of.get_saving_name()

        with open(self.log_path, "r") as reader:
            for line in reader.readlines():
                if line.startswith(param_stamp):
                    break

        col_names = ["t", "teta", "omega"]
        data = [self.temps, self.teta, self.omega]

        df = pd.DataFrame({cn: dt for cn, dt in zip(col_names, data)})
        df.to_csv(time_stamp, sep=',', header=col_names, index=False)

        log_string = param_stamp + time_stamp + "\n"
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
            "driving_force": self.driving_force,
            "driving_ang_freq": self.driving_ang_freq,
            "driving_delta": self.driving_delta,
            "l": self.l,
            "m": self.m,
            "damping": self.damping,
            "g": self.g,
        }

        return dic
