from datetime import datetime
from typing import Optional
import numpy as np
from matplotlib import pyplot as plt
from . import parameter as param


class DirectEstimator:
    def __init__(self, gyro: np.ndarray, ts: np.ndarray, init_direct: np.float32 = 0) -> None:
        self.ts = ts
        self.angular_vel = (1 if param.ROTATE_AX % 2 == 0 else -1) * (np.degrees(gyro[:, (param.ROTATE_AX - 1) // 2]) - param.DRIFT)    # angular velocity around rotation axis [°/s]
        self._estim(init_direct)

    # estimate direction by simple integral
    def _estim(self, init_direct: np.float32) -> None:
        self.direct = np.empty(len(self.ts), dtype=np.float64)

        self.direct[0] = init_direct
        for i in range(1, len(self.ts)):
            self.direct[i] = self.direct[i - 1] + self.angular_vel[i - 1] / param.FREQ

        print("direction_estimator.py: estimation completed")

    def vis(self, begin: Optional[datetime] = None, end: Optional[datetime] = None) -> None:
        if begin is None:
            begin: datetime = self.ts[0]
        if end is None:
            end: datetime = self.ts[-1]

        axes: np.ndarray = plt.subplots(nrows=2, figsize=(16, 8))[1]
        axes[0].set_title("angular velocity")
        axes[0].set_xlim(left=begin, right=end)
        axes[0].plot(self.ts, self.angular_vel)
        axes[1].set_title("direction")
        axes[1].set_xlim(left=begin, right=end)
        axes[1].plot(self.ts, self.direct)

        plt.show()
        plt.close()
