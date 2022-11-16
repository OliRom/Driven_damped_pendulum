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
        n_tps = len(t_range)
        self.temps = np.array(t_range)
        self.teta = np.empty(n_tps)
        self.omega = np.empty(n_tps)

        self.driving_force = driving_force
        self.teta[0] = teta
        self.omega[0] = omega
        self.data_saving_path = data_saving_path
        print('heyheyhey')
        print('youpi')

    def evolute_one_step(self):
        """
        Fait évoluer l'état du pendule d'un intervalle de temps.
        :return: None
        """
        pass

    def evolute_to_end(self):
        """
        Fait évoluer le pendule jusqu'à la fin du range de temps initialisé.
        :return: None
        """
        pass

    def save_data(self, file_path=None, overwrite=False):
        """
        Enregistre les données sur l'évolution du pendule dans un fichier .csv .
        :param file_path: Chemin d'accès au fichier où les données seront enregistrées
        :param overwrite: Remplacer le fichier de données s'il existe déjà
        :return: None
        """
        pass
