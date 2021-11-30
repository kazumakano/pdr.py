from datetime import datetime, timedelta
from typing import Tuple, Union
import numpy as np
from matplotlib import pyplot as plt
from . import parameter as param
from .log import FREQ

STOP_STATE = 0
BEGIN_STATE = 1
POS_PEAK_STATE = 2
NEG_PEEK_STATE = 3
END_STATE = 4
DETECT_STATE = 5

class DistEstimator:
    def __init__(self, ts: np.ndarray, acc: np.ndarray) -> None:
        global STEP_LEN

        STEP_LEN = param.STEP_LEN_COEF * param.STATURE    # length of 1 step [meter]

        self.ts = ts
        self.acc = np.hstack((acc, np.linalg.norm(acc, axis=1)[:, np.newaxis]))

        self.status = STOP_STATE                # status at automaton
        self.last_status_trans_time_index = 0    # index of last time when status transitioned
        self.last_step_time_index = 0           # index of last time when step was detected
        self.last_speed = 0                     # speed at last time [meter/second]
        self.last_dist = 0                      # cumulative movement distance until last time [meter]

    # update status and detect step with automaton
    def _detect_step(self, current_time_index: int) -> bool:
        is_detected = False

        if self.status == STOP_STATE:
            if self.acc[current_time_index, 3] > param.BEGIN_THRESH:
                self.status = BEGIN_STATE
                self.last_status_trans_time_index = current_time_index

        elif self.status == BEGIN_STATE:
            if self.acc[current_time_index, 3] < param.BEGIN_THRESH:
                self.status = STOP_STATE
                self.last_status_trans_time_index = current_time_index                
            elif self.acc[current_time_index, 3] > param.POS_PEAK_THRESH:
                self.status = POS_PEAK_STATE
                self.last_status_trans_time_index = current_time_index

        elif self.status == POS_PEAK_STATE:
            if self.acc[current_time_index, 3] < param.NEG_PEAK_THRESH:
                self.status = NEG_PEEK_STATE
                self.last_status_trans_time_index = current_time_index

        elif self.status == NEG_PEEK_STATE:    
            if self.acc[current_time_index, 3] > param.NEG_PEAK_THRESH:
                self.status = END_STATE
                self.last_status_trans_time_index = current_time_index

        elif self.status == END_STATE:
            if self.acc[current_time_index, 3] < param.NEG_PEAK_THRESH:
                self.status = NEG_PEEK_STATE
                self.last_status_trans_time_index = current_time_index
            elif self.acc[current_time_index, 3] > param.END_THRESH:
                self.status = DETECT_STATE
                self.last_status_trans_time_index = current_time_index

        elif self.status == DETECT_STATE:
            if self.acc[current_time_index, 3] < param.END_THRESH:
                self.status = END_STATE
                self.last_status_trans_time_index = current_time_index
            elif self.acc[current_time_index, 3] > param.BEGIN_THRESH and self.ts[current_time_index] - self.ts[self.last_step_time_index] > timedelta(seconds=param.MIN_STEP_INTERVAL):
                self.status = BEGIN_STATE
                self.last_status_trans_time_index = current_time_index
                is_detected = True

        if self.status != STOP_STATE:
            if (self.ts[current_time_index] - self.ts[self.last_status_trans_time_index] > timedelta(seconds=param.MAX_STATUS_INTERVAL)):
                self.status = STOP_STATE    # reset status if status unchanged for long time
                self.last_status_trans_time_index = current_time_index
        
        return is_detected

    # estimate movement distance by step detection
    def estim(self, current_time_index: int) -> Tuple[np.float64, np.float64, bool]:
        step_is_detected = self._detect_step(current_time_index)

        if self.status == STOP_STATE:
            self.last_speed = 0

        elif step_is_detected:
            if self.last_step_time_index == 0:    # first step
                self.last_speed = param.DEFAULT_SPEED
            else:                                 # second step or later
                interval: timedelta = self.ts[current_time_index] - self.ts[self.last_step_time_index]
                self.last_speed = STEP_LEN / (interval.seconds + interval.microseconds / 1000000)
            self.last_step_time_index = current_time_index    # update last_step_time_index

        self.last_dist += self.last_speed / FREQ

        return self.last_dist, self.last_speed, step_is_detected

    def get_win_speed(self, current_time_index: int) -> np.float64:
        win_len = np.uint16(param.WIN_SIZE * FREQ)
        speed = np.empty(win_len, dtype=np.float64)

        for i in reversed(range(win_len)):
            speed[i] = self.estim(current_time_index - i)[1]
        
        return speed.mean()

    def init_vis(self) -> None:
        self.vis_step = np.empty(len(self.ts), dtype=bool)
        self.vis_speed = np.empty(len(self.ts), dtype=np.float64)
        self.vis_dist = np.empty(len(self.ts), dtype=np.float64)

        for i in range(len(self.ts)):
            self.vis_dist[i], self.vis_speed[i], self.vis_step[i] = self.estim(i)

        print("distance_estimator.py: distance visualizer has been initialized")

    def run_vis(self, begin: Union[datetime, None] = None, end: Union[datetime, None] = None) -> None:
        if not hasattr(self, "vis_dist"):
            raise Exception("distance_estimator.py: distance visualizer hasn't been initialized yet")

        if begin is None:
            begin = self.ts[0]
        if end is None:
            end = self.ts[-1]

        axes: np.ndarray = plt.subplots(nrows=3, figsize=(16, 12))[1]
        vis_ar_dict = {"step": self.vis_step, "speed": self.vis_speed, "distance": self.vis_dist}
        for i, k in enumerate(vis_ar_dict):
            axes[i].set_title(k)
            axes[i].set_xlim((begin, end))
            axes[i].plot(self.ts, vis_ar_dict[k])

        plt.show()
