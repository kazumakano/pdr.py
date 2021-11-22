from sys import path as sys_path
sys_path.append("..")

import os.path
from typing import Union
import numpy as np
from particle_filter.script.parameter import set_params as set_pf_params


def _set_direct_params(conf: dict) -> None:
    global ROTATE_AX, DRIFT

    ROTATE_AX = np.int8(conf["rotate_ax"])                       # 1: +x, 2: -x, 3: +y, 4: -y, 5: +z, 6: -z (+y is tipical)
    DRIFT = np.float16(conf["gyro_drift"])                       # drift value of gyroscope [degree/second]

def _set_dist_params(conf: dict) -> None:
    global STEP_LEN_COEF, STATURE, DEFAULT_SPEED, BEGIN_THRESH, POS_PEAK_THRESH, NEG_PEAK_THRESH, END_THRESH, MIN_STEP_INTERVAL, MAX_STATE_INTERVAL

    STEP_LEN_COEF = np.float16(conf["step_len_coef"])            # ratio of step length to stature
    STATURE = np.float16(conf["stature"])                        # subject's stature [meter]
    DEFAULT_SPEED = np.float64(conf["default_speed"])            # default subject's speed [meter/second]

    BEGIN_THRESH = np.float16(conf["step_begin_acc_thresh"])     # threshold values of acceleration [G]
    POS_PEAK_THRESH = np.float16(conf["pos_peak_acc_thresh"])
    NEG_PEAK_THRESH = np.float16(conf["neg_peak_acc_thresh"])
    END_THRESH = np.float16(conf["step_end_acc_thresh"])
    MIN_STEP_INTERVAL = float(conf["min_step_interval"])         # minimum interval from last step to detect new step [second]
    MAX_STATE_INTERVAL = float(conf["max_state_interval"])       # maximum interval from last state transition to recognize as moving [second]

def _set_log_params(conf: dict) -> None:
    global WIN_SIZE

    WIN_SIZE = float(conf["pdr_win_size"])                       # size of window for calculating speed and angular velocity [second]
                                                                 # the longer window size is, the faster calculation is
                                                                 # window disabled if 0

def set_params(conf_file: Union[str, None] = None) -> dict:
    global ROOT_DIR

    ROOT_DIR = os.path.dirname(__file__) + "/../"                   # project root directory

    if conf_file is None:
        conf_file = ROOT_DIR + "config/default.yaml"    # load default config file if not specified
    else:
        conf_file = conf_file

    conf = set_pf_params(conf_file)
    _set_direct_params(conf)
    _set_dist_params(conf)
    _set_log_params(conf)

    return conf
