import math
from datetime import datetime
from typing import Union
import numpy as np
from matplotlib import pyplot as plt
import script.parameter as param

FREQ = np.uint8(100)

class DirectEstimator:
    def __init__(self, ts: np.ndarray, gyro: np.ndarray) -> None:
        self.ts = ts
        self.gyro = np.hstack((gyro, np.linalg.norm(gyro, axis=1)[:, np.newaxis]))

        self.last_direct = np.float64(0)

    def estim(self, current_time_index) -> np.float64:
        self.last_direct += math.degrees(self.gyro[current_time_index, 1]) / FREQ - param.DRIFT    # integrate values of y axis

        return self.last_direct

    def init_vis(self) -> None:
        self.direct = np.empty(len(self.ts), dtype=np.float64)

        for i in range(len(self.ts)):
            self.direct[i] = self.estim(i)

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
