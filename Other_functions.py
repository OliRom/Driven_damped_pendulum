from datetime import datetime


def get_saving_name():
    now = datetime.now()
    path = str(now).replace("-", "_").replace(".", "_").replace(" ", "_").replace(":", "_")
    return path
