import os.path as path
from datetime import datetime
from typing import Any
import numpy as np
import particle_filter.script.parameter as pf_param
import particle_filter.script.utility as pf_util
import script.parameter as param
import script.utility as util
from script.direction_estimator import DirectEstimator
from script.log import Log
from script.map import Map
from script.speed_estimator import SpeedEstimator
from script.turtle import Turtle


def _set_main_params(conf: dict) -> None:
    global BEGIN, END, LOG_FILE, INIT_DIRECT, INIT_POS, RESULT_DIR_NAME

    BEGIN = datetime.strptime(conf["begin"], "%Y-%m-%d %H:%M:%S")
    END = datetime.strptime(conf["end"], "%Y-%m-%d %H:%M:%S")
    LOG_FILE = str(conf["log_file"])
    INIT_DIRECT = np.float32(conf["init_direct"])
    INIT_POS = np.array(conf["init_pos"], dtype=np.float32)
    RESULT_DIR_NAME = None if conf["result_dir_name"] is None else str(conf["result_dir_name"])

def pdr(conf: dict[str, Any], enable_show: bool = False) -> None:
    log = Log(BEGIN, END, path.join(param.ROOT_DIR, "log/", LOG_FILE))
    map = Map(result_dir)
    direct = -1 * DirectEstimator(log.val[:, 3:6], log.ts).direct + INIT_DIRECT
    stride = util.meter2pixel(SpeedEstimator(log.val[:, 0:3], log.ts).speed / param.FREQ, map.resolution)
    result_dir = pf_util.make_result_dir(RESULT_DIR_NAME)
    turtle = Turtle(INIT_POS, INIT_DIRECT)

    if pf_param.ENABLE_SAVE_VIDEO:
        map.init_recorder()

    t: datetime
    for i, t in enumerate(log.ts):
        print(f"main.py: {t.time()}")

        turtle.forward(stride[i])
        turtle.set_heading(direct[i])

        map.draw_pos(turtle.pos)

        if pf_param.ENABLE_SAVE_VIDEO:
            map.record()
        if enable_show:
            map.show()

    print("main.py: reached end of log")
    if pf_param.ENABLE_SAVE_IMG:
        map.save_img()
    if pf_param.ENABLE_SAVE_VIDEO:
        map.save_video()
    if pf_param.ENABLE_WRITE_CONF:
        pf_util.write_conf(conf, result_dir)
    if enable_show:
        map.show(0)

if __name__ == "__main__":
    import argparse
    from script.parameter import set_params

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf_file", help="specify config file", metavar="PATH_TO_CONF_FILE")
    parser.add_argument("--no_display", action="store_true", help="run without display")
    args = parser.parse_args()

    conf = set_params(args.conf_file)
    _set_main_params(conf)

    pdr(conf, not args.no_display)
