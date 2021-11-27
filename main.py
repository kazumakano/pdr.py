import argparse
import os.path as path
from datetime import datetime
import numpy as np
import particle_filter.script.parameter as pf_param
import particle_filter.script.utility as pf_util
import script.parameter as param
from script.direction_estimator import DirectEstimator
from script.distance_estimator import DistEstimator
from script.log import FREQ, Log
from script.map import Map
from script.parameter import set_params
from script.turtle import Turtle


def _set_main_params(conf: dict) -> None:
    global FILE_RANGE_POLICY, LOG_FILE, BEGIN, END, INIT_POS, INIT_DIRECT

    FILE_RANGE_POLICY = np.int8(conf["file_range_policy"])           # 1: set log by file name
                                                                     # 2: set log by file name and slice by range
                                                                     # 3: set log by range
    LOG_FILE = conf["log_file"]                                      # log file name
    BEGIN = datetime.strptime(conf["begin"], "%Y-%m-%d %H:%M:%S")    # log range
    END = datetime.strptime(conf["end"], "%Y-%m-%d %H:%M:%S")
    INIT_POS = np.array(conf["init_pos"], np.float64)                # initial position [pixel]
    INIT_DIRECT = np.float64(conf["init_direct"])                    # initial direction [degree]

def pdr() -> None:
    if FILE_RANGE_POLICY in (1, 2):    # file name
        log = Log(file_name=path.join(param.ROOT_DIR, "log/", LOG_FILE))
        if FILE_RANGE_POLICY == 2:
            log.slice_self(BEGIN, END)
    elif FILE_RANGE_POLICY == 3:       # range
        log = Log(begin=BEGIN, end=END)
    map = Map()
    turtle = Turtle(INIT_POS, INIT_DIRECT)
    distor = DistEstimator(log.ts, log.val[:, 0:3])
    director = DirectEstimator(log.ts, log.val[:, 3:6])

    if pf_param.ENABLE_SAVE_VIDEO:
        map.init_recorder()

    if param.WIN_SIZE == 0:     # window disabled
        for i, t in enumerate(log.ts):
            print(f"main.py: {t.time()}")

            speed =  pf_util.conv_from_meter_to_pixel(distor.estim(i)[1], map.resolution)
            turtle.forward(speed / FREQ)

            angular_vel = director.estim(i)[1]
            turtle.right(angular_vel / FREQ)

            map.draw_pos(turtle.pos)
            map.show()
            if pf_param.ENABLE_SAVE_VIDEO:
                map.record()
    
    elif param.WIN_SIZE > 0:    # window is enabled
        win_len = int(param.WIN_SIZE * FREQ)
        for i in range(win_len - 1, len(log.ts), win_len):
            print(f"main.py: {log.ts[i].time()}")

            speed = pf_util.conv_from_meter_to_pixel(distor.get_win_speed(i), map.resolution)
            turtle.forward(speed * param.WIN_SIZE)

            angular_vel = director.get_win_angular_vel(i)
            turtle.right((angular_vel - director.sign * param.DRIFT) * param.WIN_SIZE)

            map.draw_pos(turtle.pos)
            map.show()
            if pf_param.ENABLE_SAVE_VIDEO:
                map.record()

    print("main.py: reached end of log")
    if pf_param.ENABLE_SAVE_IMG:
        map.save_img()
    if pf_param.ENABLE_SAVE_VIDEO:
        map.save_video()
    map.show(0)    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--config", help="specify your config file", metavar="PATH_TO_CONFIG_FILE")

    conf = set_params(parser.parse_args().config)
    _set_main_params(conf)

    pdr()
