from datetime import datetime
import pandas as pd
import numpy as np
import os


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


def get_sim_names(path, params, sorting=None):
    """
    Retourne tous les time stamp des fichiers avec les paramètres spécifiées qui sont dans le fichier de log spécifié
    par path.
    :param path: Le path du fichier de log
    :param params: Les paramètres voulus (sous forme d'un dictionnaire)
    :param sorting: Nom de la colonne selon laquelle trier les données
    :return: Une list des time_stamp retenus
    """
    simulations = pd.read_csv(path, usecols=list(params.keys()) + ["time_stamp"])
    for key, val in params.items():
        simulations = simulations[simulations[key].isin(val)]

    if sorting is not None:
        simulations.sort_values(sorting)

    return simulations["time_stamp"]


def split_time(time, form=":"):
    # time in (s)
    # format:
    # -> ":" hh:mm:ss
    # -> "dict" dict([('h', hh), ('m', mm), ('s', ss)])
    # -> "str" {hh} hours {mm} minutes {ss} seconds

    tm = dict()

    tm["h"] = int(time / 3600)
    tm["m"] = int((time % 3600) / 60)
    tm["s"] = int(time % 60)

    if form == "dict":
        return tm
    elif form == "str":
        return f"{tm['h']} hours {tm['m']} minutes {tm['s']} seconds"
    elif form == ":":
        return f"{tm['h']}:{tm['m']}:{tm['s']}"
    else:
        return f"{form} is an unrecognised return format"


def delete_doubles(log_path):
    log_file = pd.read_csv(log_path)
    duplicates = log_file["time_stamp"].duplicated()

    dup_indexes = [d + 1 for d in log_file.index[duplicates].tolist()]

    with open("temp_" + log_path, "w") as temp_file:
        with open(log_path, "r") as old_file:
            for nb, line in enumerate(old_file.readlines()):
                if nb not in dup_indexes and line != "\n":
                    temp_file.write(line)

    os.remove(log_path)
    os.rename("temp_" + log_path, log_path)


def test_sim_data(sim_path):
    try:
        pd.read_csv(sim_path)
    except:
        try:
            os.remove(sim_path)
        except:
            pass

        return sim_path


def delete_unreadeable(log_path, data_path):
    log_file = pd.read_csv(log_path)
    sim_names = log_file["time_stamp"]
    bad_indexes = list()
    for index, name in enumerate(sim_names):
        to_remove = False
        try:
            data = pd.read_csv(os.path.join(data_path, name + ".csv"))
            if len(data.index) != log_file.loc[log_file["time_stamp"] == name]["n_iter"].tolist()[0]:
                bad_indexes.append(index+1)
                to_remove = True
        except:
            bad_indexes.append(index+1)
            to_remove = True

        if to_remove:
            try:
                print(f"Removed \"{name}\".")
                os.remove(os.path.join(data_path, name + ".csv"))
            except:
                pass

    with open("temp_" + log_path, "w") as temp_file:
        with open(log_path, "r") as old_file:
            for nb, line in enumerate(old_file.readlines()):
                if nb not in bad_indexes and line != "\n":
                    temp_file.write(line)

    os.remove(log_path)
    os.rename("temp_" + log_path, log_path)


def delete_bad_sims(log_path, data_path):
    delete_doubles(log_path)
    delete_unreadeable(log_path, data_path)
