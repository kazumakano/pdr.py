import math
from datetime import datetime
from typing import Tuple, Union
import numpy as np
from matplotlib import pyplot as plt
from . import parameter as param
from .log import FREQ


class DirectEstimator:
    def __init__(self, ts: np.ndarray, gyro: np.ndarray) -> None:
        global AX_INDEX

        AX_INDEX = (param.ROTATE_AX - 1) // 2

        self.ts = ts
        self.gyro = np.hstack((gyro, np.linalg.norm(gyro, axis=1)[:, np.newaxis]))

        if param.ROTATE_AX // 2 == 1:
            self.sign = 1     # positive
        else:
            self.sign = -1    # negative
        self.last_direct = np.float64(0)

    def estim(self, current_time_index: int) -> Tuple[np.float64, np.float64]:
        angular_vel = self.sign * np.float64(math.degrees(self.gyro[current_time_index, AX_INDEX]))
        self.last_direct += (angular_vel - self.sign * param.DRIFT) / FREQ    # integrate

        return self.last_direct, angular_vel
    
    def get_win_angular_vel(self, current_time_index: int) -> np.float64:
        win_len = int(param.WIN_SIZE * FREQ)
        angular_vel = np.empty(win_len, dtype=np.float64)
        
        for i in reversed(range(win_len)):
            angular_vel[i] = self.estim(current_time_index - i)[1]
        
        return angular_vel.mean()
    
    def init_vis(self) -> None:
        self.direct = np.empty(len(self.ts), dtype=np.float64)

        for i in range(len(self.ts)):
            self.direct[i] = self.estim(i)[0]

        print("direction_estimator.py: direction visualizer has been initialized")

    def run_vis(self, begin: Union[datetime, None] = None, end: Union[datetime, None] = None) -> None:
        if not hasattr(self, "direct"):
            raise Exception("direction_estimator.py: direction visualizer has not been initialized yet")

        if begin is None:
            begin = self.ts[0]
        if end is None:
            end = self.ts[-1]

        ax: np.ndarray = plt.subplots(figsize=(16, 4))[1]
        ax.set_title("direction")
        ax.set_xlim((begin, end))
        ax.plot(self.ts, self.direct)

        plt.show()
