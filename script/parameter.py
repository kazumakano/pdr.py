import os.path as path
from typing import Any, Union
import numpy as np
from particle_filter.script.parameter import set_params as set_pf_params


def _set_direct_params(conf: dict[str, Any]) -> None:
    global DRIFT, ROTATE_AX

    DRIFT = np.float16(conf["gyro_drift"])
    ROTATE_AX = np.int8(conf["rotate_ax"])

def _set_dist_params(conf: dict[str, Any]) -> None:
    global DEFAULT_SPEED, MAX_STATUS_INTERVAL, MIN_STEP_INTERVAL, STATURE, STEP_LEN_COEF, BEGIN_THRESH, POS_PEAK_THRESH, NEG_PEAK_THRESH, END_THRESH

    DEFAULT_SPEED = np.float16(conf["default_speed"])
    MAX_STATUS_INTERVAL = float(conf["max_status_interval"])
    MIN_STEP_INTERVAL = float(conf["min_step_interval"])
    STATURE = np.float16(conf["stature"])
    STEP_LEN_COEF = np.float16(conf["step_len_coef"])
    BEGIN_THRESH = np.float16(conf["step_begin_acc_thresh"])
    POS_PEAK_THRESH = np.float16(conf["pos_peak_acc_thresh"])
    NEG_PEAK_THRESH = np.float16(conf["neg_peak_acc_thresh"])
    END_THRESH = np.float16(conf["step_end_acc_thresh"])

def _set_log_params(conf: dict[str, Any]) -> None:
    global FREQ, WIN_SIZE

    FREQ = np.float16(conf["freq"])
    WIN_SIZE = float(conf["win_size"])

def set_params(conf_file: Union[str, None] = None) -> dict[str, Any]:
    global ROOT_DIR

    ROOT_DIR = path.join(path.dirname(__file__), "../")

    if conf_file is None:
        conf_file = path.join(ROOT_DIR, "config/default.yaml")

    conf = set_pf_params(conf_file)
    _set_direct_params(conf)
    _set_dist_params(conf)
    _set_log_params(conf)

    return conf
