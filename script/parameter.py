import os.path as path
from typing import Union
import numpy as np
import yaml


def _set_log_params(conf: dict) -> None:
    global WIN_SIZE

    WIN_SIZE = int(conf["win_size"])                                # size of sliding window [second]

def set_params(conf_file: Union[str, None] = None) -> dict:
    global ROOT_DIR, IS_LOST

    ROOT_DIR = path.dirname(__file__) + "/../"                      # project root directory
    IS_LOST = False                                                 # subject is lost or not

    if conf_file is None:
        conf_file = ROOT_DIR + "config/default.yaml"    # load default config file if not specified
    else:
        conf_file = conf_file

    with open(conf_file) as f:
        conf: dict = yaml.safe_load(f)
    print(f"parameter.py: {path.basename(conf_file)} has been loaded")

    _set_log_params(conf)

    return conf
