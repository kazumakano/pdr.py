import csv
import os.path as path
import pickle
from datetime import datetime
from typing import Any, Optional
import numpy as np
from matplotlib import pyplot as plt


class Log:
    def __init__(self, begin: datetime, end: datetime, file: str) -> None:
        if begin > end:
            raise Exception("log.py: log range is wrong")

        self.ts = np.empty(0, dtype=datetime)            # timestamp
        self.val = np.empty((0, 6), dtype=np.float64)    # sensor values of accelerometer and gyroscope

        match path.splitext(file)[1]:
            case ".csv":
                self._load_csv(begin, end, file)
            case ".pkl":
                self._load_pkl(begin, end, file)
            case _:
                raise Exception("log.py: only CSV and pickle are supported")

        print(f"log.py: {path.basename(file)} has been loaded")
        print(f"log.py: log length is {len(self.ts)}")

    def _load_csv(self, begin: datetime, end: datetime, file: str) -> None:
        with open(file) as f:
            for row in csv.reader(f):
                log_datetime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
                if log_datetime < begin:
                    continue
                elif log_datetime > end:
                    break
                self.ts = np.hstack((self.ts, log_datetime))
                self.val = np.vstack((self.val, [np.float64(v) for v in row[1:7]]))

    def _slice(self, begin: datetime, end: datetime) -> None:
        slice_time_idx = len(self.ts)
        for i, t in enumerate(self.ts):
            if t >= begin:
                slice_time_idx = i
                break
        self.ts = self.ts[slice_time_idx:]
        self.val = self.val[slice_time_idx:]

        slice_time_idx = len(self.ts)
        for i, t in enumerate(self.ts):
            if t > end:
                slice_time_idx = i
                break
        self.ts = self.ts[:slice_time_idx]
        self.val = self.val[:slice_time_idx]

    def _load_pkl(self, begin: datetime, end: datetime, file: str) -> None:
        with open(file, mode="rb") as f:
            self.ts, self.val = pickle.load(f)
        self._slice(begin, end)

    def vis(self, begin: Optional[datetime] = None, end: Optional[datetime] = None, enable_lim: bool = False, components_lim: Any = (-1, 1), norm_lim: Any = (0, 2)) -> None:
        if begin is None:
            begin = self.ts[0]
        if end is None:
            end = self.ts[-1]

        axes = plt.subplots(nrows=8, figsize=(16, 32))[1]
        for i, s in enumerate(("accelerometer", "gyroscope")):
            for j in range(3):
                axes[4*i+j].set_title(f"{s} {('x', 'y', 'z')[j]}")
                axes[4*i+j].set_xlim(left=begin, right=end)
                if enable_lim:
                    axes[4*i+j].set_ylim(components_lim)
                axes[4*i+j].plot(self.ts, self.val[:, 3*i+j])
            axes[4*i+3].set_title(f"{s} norm")
            axes[4*i+3].set_xlim(left=begin, right=end)
            if enable_lim:
                axes[4*i+3].set_ylim(norm_lim)
            axes[4*i+3].plot(self.ts, np.linalg.norm(self.val[:, 3*i:3*i+3], axis=1))
        plt.show()
        plt.close()
