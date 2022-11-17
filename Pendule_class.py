import numpy as np


class Pendulum:
    def __init__(self, teta, omega, t_range, driving_force, data_saving_path):
        """
        Initialisation des paramètres du pendule
        :param teta: Angle initial du pendule
        :param omega: Vitesse angulaire initiale du pendule
        :param t_range: Temps sur lesquels intégrer
        :param driving_force: Fonction qui drive le pendule
        :param data_saving_path: Path du fichier où enregistrer les données à la fin d'une simulation
        """
        self.n_iter = len(t_range)  # Nombre total d'itération d'intégrations à effectuer
        self.iteration = 0  # Iteration d'intégration à laquelle le programme est rendu

        self.temps = np.array(t_range)
        self.dt = self.temps[0] - self.temps[1]

        self.teta = np.empty(self.n_iter)
        self.omega = np.empty(self.n_iter)

        self.driving_force = driving_force
        self.teta[0] = teta
        self.omega[0] = omega
        self.data_saving_path = data_saving_path

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

    def save_data(self, file_path=None, overwrite=False):
        """
        Enregistre les données sur l'évolution du pendule dans un fichier .csv .
        :param file_path: Chemin d'accès au fichier où les données seront enregistrées
        :param overwrite: Remplacer le fichier de données s'il existe déjà
        :return: None
        """
        pass
