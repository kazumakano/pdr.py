from datetime import datetime, timedelta
from typing import Optional
import numpy as np
from matplotlib import pyplot as plt
from . import parameter as param

STOP_STATE = 0
BEGIN_STATE = 1
POS_PEAK_STATE = 2
NEG_PEEK_STATE = 3
END_STATE = 4
DETECT_STATE = 5

class SpeedEstimator:
    def __init__(self, acc: np.ndarray, ts: np.ndarray) -> None:
        self.ts = ts
        self.acc_norm = np.linalg.norm(acc, axis=1)
        self._estim()

    # update status and detect step with automaton
    def _detect_step(self, current_time_index: int, last_status_trans_time_index: int, last_step_time_index: int, status: int) -> tuple[bool, int, int]:
        is_detected = False

        if status == STOP_STATE:
            if self.acc_norm[current_time_index] > param.BEGIN_THRESH:
                status = BEGIN_STATE
                last_status_trans_time_index = current_time_index

        elif status == BEGIN_STATE:
            # if self.acc_norm[current_time_index] < param.BEGIN_THRESH:
            #     status = STOP_STATE
            #     last_status_trans_time_index = current_time_index
            if self.acc_norm[current_time_index] > param.POS_PEAK_THRESH:
                status = POS_PEAK_STATE
                last_status_trans_time_index = current_time_index

        elif status == POS_PEAK_STATE:
            if self.acc_norm[current_time_index] < param.NEG_PEAK_THRESH:
                status = NEG_PEEK_STATE
                last_status_trans_time_index = current_time_index

        elif status == NEG_PEEK_STATE:    
            if self.acc_norm[current_time_index] > param.NEG_PEAK_THRESH:
                status = END_STATE
                last_status_trans_time_index = current_time_index

        elif status == END_STATE:
            if self.acc_norm[current_time_index] < param.NEG_PEAK_THRESH:
                status = NEG_PEEK_STATE
                last_status_trans_time_index = current_time_index
            elif self.acc_norm[current_time_index] > param.END_THRESH:
                status = DETECT_STATE
                last_status_trans_time_index = current_time_index

        elif status == DETECT_STATE:
            if self.acc_norm[current_time_index] < param.END_THRESH:
                status = END_STATE
                last_status_trans_time_index = current_time_index
            elif self.acc_norm[current_time_index] > param.BEGIN_THRESH and self.ts[current_time_index] - self.ts[last_step_time_index] > timedelta(seconds=param.MIN_STEP_INTERVAL):
                status = BEGIN_STATE
                last_status_trans_time_index = current_time_index
                is_detected = True

        if (self.ts[current_time_index] - self.ts[last_status_trans_time_index] > timedelta(seconds=param.MAX_STATUS_INTERVAL)):
            status = STOP_STATE    # reset status if status unchanged for long time
            last_status_trans_time_index = current_time_index
        
        return is_detected, last_status_trans_time_index, status

    # estimate speed by step detection algorithm
    def _estim(self) -> None:
        self.speed = np.empty(len(self.ts), dtype=np.float64)
        self.step_is_detected = np.empty(len(self.ts), dtype=bool)

        last_status_trans_time_index = 0                  # index of time when status transitioned last
        last_step_time_index = 0                          # index of time when step was detected last
        status = STOP_STATE                               # status of automaton
        step_len = param.STEP_LEN_COEF * param.STATURE    # length of 1 step [m]
        self.speed[0] = 0
        self.step_is_detected[0] = False
        for i in range(1, len(self.ts)):
            self.step_is_detected[i], last_status_trans_time_index, status = self._detect_step(i, last_status_trans_time_index, last_step_time_index, status)

            if status == STOP_STATE:
                self.speed[i] = 0
                last_step_time_index = 0

            elif self.step_is_detected[i]:
                if last_step_time_index == 0:    # first step
                    self.speed[i] = param.DEFAULT_SPEED
                else:                                 # second step or later
                    interval: timedelta = self.ts[i] - self.ts[last_step_time_index]
                    self.speed[i] = step_len / (interval.seconds + interval.microseconds / 1000000)
                last_step_time_index = i

            else:
                self.speed[i] = self.speed[i - 1]

        print("speed_estimator.py: estimation completed")

    def init_vis(self) -> None:
        self.vis_dist = np.empty(len(self.ts), dtype=np.float64)

        self.vis_dist[0] = 0
        for i in range(1, len(self.ts)):
            self.vis_dist[i] = self.vis_dist[i - 1] + self.speed[i - 1] / param.FREQ

        print("speed_estimator.py: speed visualizer has been initialized")

    def run_vis(self, begin: Optional[datetime] = None, end: Optional[datetime] = None) -> None:
        if not hasattr(self, "vis_dist"):
            raise Exception("speed_estimator.py: speed visualizer hasn't been initialized yet")

        if begin is None:
            begin = self.ts[0]
        if end is None:
            end = self.ts[-1]

        axes: np.ndarray = plt.subplots(nrows=3, figsize=(16, 12))[1]
        axes[0].set_title("step")
        axes[0].set_xlim(left=begin, right=end)
        axes[0].plot(self.ts, self.step_is_detected)
        axes[1].set_title("speed")
        axes[1].set_xlim(left=begin, right=end)
        axes[1].plot(self.ts, self.speed)
        axes[2].set_title("distance")
        axes[2].set_xlim(left=begin, right=end)
        axes[2].plot(self.ts, self.vis_dist)

        plt.show()
        plt.close()
