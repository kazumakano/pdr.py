import math
from datetime import datetime
from typing import Union
import numpy as np
import particle_filter.script.parameter as pf_param
from matplotlib import pyplot as plt
from . import parameter as param


class DirectEstimator:
    def __init__(self, gyro: np.ndarray, ts: np.ndarray) -> None:
        global AX_INDEX

        AX_INDEX = np.int8((param.ROTATE_AX - 1) // 2)    # 0: x, 1: y, 2: z

        self.ts = ts
        self.gyro = np.hstack((gyro, np.linalg.norm(gyro, axis=1)[:, np.newaxis]))

        self.last_direct = 0
        if param.ROTATE_AX % 2 == 1:    # positive
            self.sign = -1
        else:                           # negative
            self.sign = 1

    # estimate direction by integral
    def estim(self, current_time_index: int) -> tuple[np.float64, np.float64]:
        angular_vel = self.sign * math.degrees(self.gyro[current_time_index, AX_INDEX])
        self.last_direct += (angular_vel - self.sign * param.DRIFT) / param.FREQ    # integrate

        return self.last_direct, angular_vel
    
    def get_win_angular_vel(self, current_time_index: int) -> np.float64:
        win_len = np.int16(pf_param.WIN_STRIDE * param.FREQ)
        angular_vel = np.empty(win_len, dtype=np.float64)
        
        for i in reversed(range(win_len)):
            angular_vel[i] = self.estim(current_time_index - i)[1]
        
        return angular_vel.mean()
    
    def init_vis(self) -> None:
        self.vis_direct = np.empty(len(self.ts), dtype=np.float64)

        for i in range(len(self.ts)):
            self.vis_direct[i] = self.estim(i)[0]

        print("direction_estimator.py: direction visualizer has been initialized")

    def run_vis(self, begin: Union[datetime, None] = None, end: Union[datetime, None] = None) -> None:
        if not hasattr(self, "vis_direct"):
            raise Exception("direction_estimator.py: direction visualizer hasn't been initialized yet")

        if begin is None:
            begin = self.ts[0]
        if end is None:
            end = self.ts[-1]

        ax = plt.subplots(figsize=(16, 4))[1]
        ax.set_title("direction")
        ax.set_xlim((begin, end))
        ax.plot(self.ts, self.vis_direct)

        plt.show()
