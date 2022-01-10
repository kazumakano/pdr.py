import csv
import os.path as path
import pickle
from datetime import datetime, timedelta
from typing import Any, Union
import numpy as np
from matplotlib import pyplot as plt
from . import parameter as param

SENSORS = ("ACC", "GYRO")

class Log:
    def __init__(self, begin: datetime, end: datetime, file: str) -> None:
        if begin > end:
            raise Exception("log.py: log range is wrong")

        self.ts = np.empty(0, dtype=datetime)            # timestamp
        self.val = np.empty((0, 6), dtype=np.float64)    # sensor values of acceleration and gyroscope

        if file[-4:] == ".csv":
            self._load_csv(begin, end, file)
        elif file[-4:] == ".pkl":
            self._load_pkl(begin, end, file)
        else:
            raise Exception("log.py: only CSV and pickle are supported")

        print(f"log.py: {path.basename(file)} has been loaded")
        print(f"log.py: log length is {len(self.ts)}")

    def _load_csv(self, begin: datetime, end: datetime, file: str) -> None:
        with open(file) as f:
            reader = csv.reader(f)
            for row in reader:
                log_datetime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
                if log_datetime < begin - timedelta(seconds=param.WIN_SIZE - 1 / param.FREQ):
                    continue
                elif log_datetime > end:
                    break
                self.ts = np.hstack((self.ts, log_datetime))
                self.val = np.vstack((self.val, [np.float64(column) for column in row[1:7]]))

    def _slice(self, begin: datetime, end: datetime) -> None:
        slice_time_index = len(self.ts)
        for i, t in enumerate(self.ts):
            if t >= begin - timedelta(seconds=(param.WIN_SIZE - 1 / param.FREQ)):
                slice_time_index = i
                break
        self.ts = self.ts[slice_time_index:]
        self.val = self.val[slice_time_index:]

        slice_time_index = -1
        for i, t in enumerate(self.ts):
            if t > end:
                slice_time_index = i
                break
        self.ts = self.ts[:slice_time_index]
        self.val = self.val[:slice_time_index]
    
    def _load_pkl(self, begin: datetime, end: datetime, file: str) -> None:
        with open(file, "rb") as f:
            self.ts, self.val = pickle.load(f)
        self._slice(begin, end)

    def export_to_pkl(self, file: str) -> None:
        with open(file[:-4] + ".pkl", "wb") as f:
            pickle.dump((self.ts, self.val), f)

    def vis(self, begin: Union[datetime, None] = None, end: Union[datetime, None] = None, enable_lim: bool = False, components_lim: Any = (-1, 1), norm_lim: Any = (0, 2)) -> None:
        if begin is None:
            begin = self.ts[0]
        if end is None:
            end = self.ts[-1]

        titles = ("X", "Y", "Z")
        axes: np.ndarray = plt.subplots(nrows=4 * len(SENSORS), figsize=(16, 16 * len(SENSORS)))[1]
        for i, s in enumerate(SENSORS):
            for j in range(3):
                axes[4*i+j].set_title(s + "_" + titles[j])
                axes[4*i+j].set_xlim((begin, end))
                if enable_lim:
                    axes[4*i+j].set_ylim(components_lim)
                axes[4*i+j].plot(self.ts, self.val[:, 3*i+j])
            axes[4*i+3].set_title(s + "_" + "NORM")
            axes[4*i+3].set_xlim((begin, end))
            if enable_lim:
                axes[4*i+3].set_ylim(norm_lim)
            axes[4*i+3].plot(self.ts, np.linalg.norm(self.val[:, 3*i:3*i+3], axis=1))
