from datetime import datetime
import pandas as pd
import numpy as np


def get_saving_name():
    """
    Retourne le nom du fichier de données à enregistrer. C'est un time stamp.
    :return: Le nom du fichier de données
    """
    now = datetime.now()
    path = str(now).replace("-", "_").replace(".", "_").replace(" ", "_").replace(":", "_")
    return path


def round_to_precision(number, precision):
    """
    Arrondi un nombre à "precision" chiffres significatifs.
    :param number: Le nombre à arrondir
    :param precision: Le nombre de chiffres significatifs à garder
    :return: Le nombre arrondi
    """
    if number == 0:
        return number

    higher = int(np.log10(abs(number)))
    if number >= 1:
        higher += 1
    return round(number, -(higher - precision))


def get_sim_names(path, params):
    """
    Retourne tous les time stamp des fichiers avec les paramètres spécifiées qui sont dans le fichier de log spécifié
    par path.
    :param path: Le path du fichier de log
    :param params: Les paramètres voulus (sous forme d'un dictionnaire)
    :return: Une list des time_stamp retenus
    """
    simulations = pd.read_csv(path, usecols=list(params.keys())+["time_stamp"])
    for key, val in params.items():
        simulations = simulations[simulations[key].isin(val)]

    return simulations["time_stamp"]

