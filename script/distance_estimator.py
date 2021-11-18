from datetime import datetime, timedelta
from typing import Tuple, Union
import numpy as np
from matplotlib import pyplot as plt
import script.parameter as param

STOP_STATE = np.int8(0)
BEGIN_STATE = np.int8(1)
POS_PEAK_STATE = np.int8(2)
NEG_PEEK_STATE = np.int8(3)
END_STATE = np.int8(4)
DETECT_STATE = np.int8(5)
FREQ = np.uint8(100)

class DistEstimator:
    def __init__(self, ts: np.ndarray, acc: np.ndarray) -> None:
        global STEP_LEN

        STEP_LEN = param.STEP_LEN_COEF * param.STATURE    # length of 1 step [meter]

        self.ts = ts
        self.acc = np.hstack((acc, np.linalg.norm(acc, axis=1)[:, np.newaxis]))

        self.state: np.int8 = STOP_STATE               # state at automaton
        self.last_state_trans_time_index: int = 0      # index of last time when state transitioned
        self.last_step_time_index: int = 0             # index of last time when step was detected
        self.last_speed = np.float64(0)                # speed at last time [meter/second]
        self.last_dist = np.float64(0)                 # cumulative movement distance until last time [meter]

    # update state and detect step with automaton
    def _detect_step(self, current_time_index: int) -> bool:
        is_detected: bool = False

        if self.state == STOP_STATE:
            if self.acc[current_time_index, 3] > param.BEGIN_THRESH:
                self.state = BEGIN_STATE
                self.last_state_trans_time_index = current_time_index

        elif self.state == BEGIN_STATE:
            if self.acc[current_time_index, 3] < param.BEGIN_THRESH:
                self.state = STOP_STATE
                self.last_state_trans_time_index = current_time_index                
            elif self.acc[current_time_index, 3] > param.POS_PEAK_THRESH:
                self.state = POS_PEAK_STATE
                self.last_state_trans_time_index = current_time_index

        elif self.state == POS_PEAK_STATE:
            if self.acc[current_time_index, 3] < param.NEG_PEAK_THRESH:
                self.state = NEG_PEEK_STATE
                self.last_state_trans_time_index = current_time_index

        elif self.state == NEG_PEEK_STATE:    
            if self.acc[current_time_index, 3] > param.NEG_PEAK_THRESH:
                self.state = END_STATE
                self.last_state_trans_time_index = current_time_index

        elif self.state == END_STATE:
            if self.acc[current_time_index, 3] < param.NEG_PEAK_THRESH:
                self.state = NEG_PEEK_STATE
                self.last_state_trans_time_index = current_time_index
            elif self.acc[current_time_index, 3] > param.END_THRESH:
                self.state = DETECT_STATE
                self.last_state_trans_time_index = current_time_index

        elif self.state == DETECT_STATE:
            if self.acc[current_time_index, 3] < param.END_THRESH:
                self.state = END_STATE
                self.last_state_trans_time_index = current_time_index
            elif self.acc[current_time_index, 3] > param.BEGIN_THRESH and self.ts[current_time_index] - self.ts[self.last_step_time_index] > timedelta(seconds=param.MIN_STEP_INTERVAL):
                self.state = BEGIN_STATE
                self.last_state_trans_time_index = current_time_index
                is_detected = True

        if self.state != STOP_STATE:
            if (self.ts[current_time_index] - self.ts[self.last_state_trans_time_index] > timedelta(seconds=param.MAX_STATE_INTERVAL)):
                self.state = STOP_STATE    # reset state if state unchanged for long time
                self.last_state_trans_time_index = current_time_index
        
        return is_detected

    # estimate movement distance by step detection
    def estim(self, current_time_index: int) -> Tuple[np.float64, bool]:
        step_is_detected = self._detect_step(current_time_index)

        if self.state == STOP_STATE:
            self.last_speed = np.float64(0)

        elif step_is_detected:
            if self.last_step_time_index == 0:    # first step
                self.last_speed = param.DEFAULT_SPEED
            else:                                 # second step or later
                interval: timedelta = self.ts[current_time_index] - self.ts[self.last_step_time_index]
                self.last_speed: np.float64 = STEP_LEN / (interval.seconds + interval.microseconds / 1000000)
            self.last_step_time_index = current_time_index    # update last_step_time_index

        self.last_dist += self.last_speed / FREQ

        return self.last_dist, self.last_speed, step_is_detected

    def init_vis(self) -> None:
        self.step = np.empty(len(self.ts), dtype=bool)
        self.speed = np.empty(len(self.ts), dtype=np.float64)
        self.dist = np.empty(len(self.ts), dtype=np.float64)

        for i in range(len(self.ts)):
            self.dist[i], self.speed[i], self.step[i] = self.estim(i)

        print("distance_estimator.py: distance visualizer has been initialized")

    def run_vis(self, begin: Union[datetime, None] = None, end: Union[datetime, None] = None) -> None:
        if not hasattr(self, "dist"):
            raise Exception("distance_estimator.py: distance visualizer has not been initialized yet")

        if begin is None:
            begin = self.ts[0]
        if end is None:
            end = self.ts[-1]

        axes: np.ndarray = plt.subplots(nrows=3, figsize=(16, 12))[1]
        vis_dict = {"step": self.step, "speed": self.speed, "distance": self.dist}
        for i, k in enumerate(vis_dict):
            axes[i].set_title(k)
            axes[i].set_xlim((begin, end))
            axes[i].plot(self.ts, vis_dict[k])

        plt.show()
