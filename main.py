import os.path as path
from datetime import datetime
import numpy as np
import particle_filter.script.parameter as pf_param
import particle_filter.script.utility as pf_util
import script.parameter as param
from script.direction_estimator import DirectEstimator
from script.distance_estimator import DistEstimator
from script.log import Log
from script.map import Map
from script.turtle import Turtle


def _set_main_params(conf: dict) -> None:
    global BEGIN, END, LOG_FILE, INIT_DIRECT, INIT_POS, RESULT_FILE_NAME

    BEGIN = datetime.strptime(conf["begin"], "%Y-%m-%d %H:%M:%S")
    END = datetime.strptime(conf["end"], "%Y-%m-%d %H:%M:%S")
    LOG_FILE = str(conf["log_file"])
    INIT_DIRECT = np.float16(conf["init_direct"])
    INIT_POS = np.array(conf["init_pos"], dtype=np.float16)
    RESULT_FILE_NAME = pf_util.gen_file_name() if conf["result_file_name"] is None else str(conf["result_file_name"])

def pdr() -> None:
    log = Log(BEGIN, END, path.join(param.ROOT_DIR, "log/", LOG_FILE))
    map = Map(RESULT_FILE_NAME)
    turtle = Turtle(INIT_POS, INIT_DIRECT)
    distor = DistEstimator(log.val[:, 0:3], log.ts)
    director = DirectEstimator(log.val[:, 3:6], log.ts)

    if pf_param.ENABLE_SAVE_VIDEO:
        map.init_recorder()

    if param.WIN_STRIDE == 0:    # sliding window is disabled
        t: datetime
        for i, t in enumerate(log.ts):
            print(f"main.py: {t.time()}")

            speed =  pf_util.conv_from_meter_to_pixel(distor.estim(i)[1], map.resolution)
            turtle.forward(speed / param.FREQ)

            angular_vel = director.estim(i)[1]
            turtle.right(angular_vel / param.FREQ)

            map.draw_pos(turtle.pos)
            map.show()
            if pf_param.ENABLE_SAVE_VIDEO:
                map.record()
    
    else:                           # sliding window is enabled
        win_len = np.int16(param.WIN_STRIDE * param.FREQ)
        for i in range(win_len - 1, len(log.ts), win_len):
            print(f"main.py: {log.ts[i].time()}")

            speed = pf_util.conv_from_meter_to_pixel(distor.get_win_speed(i, win_len), map.resolution)
            turtle.forward(speed * param.WIN_STRIDE)

            angular_vel = director.get_win_angular_vel(i, win_len)
            turtle.right((angular_vel - director.sign * param.DRIFT) * param.WIN_STRIDE)

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
    import argparse
    from script.parameter import set_params

    parser = argparse.ArgumentParser()
    parser.add_argument("-c", "--conf_file", help="specify config file", metavar="PATH_TO_CONF_FILE")

    _set_main_params(set_params(parser.parse_args().conf_file))

    pdr()
