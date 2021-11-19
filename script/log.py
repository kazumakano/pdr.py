import csv
import os.path as path
import pickle
from datetime import datetime, timedelta
from glob import iglob
from typing import Any, Union
import numpy as np
from matplotlib import pyplot as plt
from . import parameter as param

SENSOR_LIST = ("ACC", "GYRO")
FREQ = np.uint8(100)

class Log:
    def __init__(self, file_name: Union[str, None] = None, begin: Union[datetime, None] = None , end: Union[datetime, None] = None) -> None:
        if not ((file_name is not None and begin is None and end is None) or (file_name is None and begin is not None and end is not None)):
            raise Exception("log.py: specify either log file name or log range")
        if file_name is None and begin > end:
            raise Exception("log.py: log range is wrong")

        self.ts = np.empty(0, dtype=datetime)                               # timestamp
        self.val = np.empty((0, 3 * len(SENSOR_LIST)), dtype=np.float64)    # values of SENSOR_LIST * (x, y, z)

        if file_name is not None:    # file name is specified
            if file_name[-4:] == ".csv":
                with open(file_name) as f:
                    reader = csv.reader(f)
                    for row in reader:
                        self.ts = np.hstack((self.ts, datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")))
                        self.val = np.vstack((self.val, [np.float64(column) for column in row[1:]]))
            
            elif file_name[-4:] == ".pkl":
                with open(file_name, "rb") as f:
                    self.ts, self.val = pickle.load(f)

            print(f"log.py: {path.basename(file_name)} has been loaded")

        else:                   # log range is specified
            for file_name in iglob(param.ROOT_DIR + "log/*.csv"):
                log_date = datetime.strptime(path.basename(file_name).split("_")[0], "%Y-%m-%d").date()

                if begin.date() <= log_date <= end.date():
                    is_loaded = False
                    with open(file_name) as f:
                        reader = csv.reader(f)
                        for row in reader:
                            log_datetime = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S.%f")
                            if log_datetime < begin - timedelta(seconds=param.WIN_SIZE):
                                continue
                            elif log_datetime > end:
                                break
                            self.ts = np.hstack((self.ts, log_datetime))
                            self.val = np.vstack((self.val, [np.float64(column) for column in row[1:]]))
                            is_loaded = True

                    if is_loaded:
                        print(f"log.py: {path.basename(file_name)} has been loaded")

            self._sort()

        print(f"log.py: log length is {len(self.ts)}")

    # sort by timestamp
    def _sort(self) -> None:
        sorted_indexes = self.ts.argsort()

        self.ts = self.ts[sorted_indexes]
        self.val = self.val[sorted_indexes]
    
    def slice_self(self, begin: Union[datetime, None] = None, end: Union[datetime, None] = None) -> None:
        if begin is None and end is None:
            raise Warning("log.py: specify range in order to slice log")
        elif begin is not None and end is not None and begin > end:
            raise Exception("log.py: log range is wrong")

        if begin is not None:
            slice_time_index = len(self.ts)
            for i, t in enumerate(self.ts):
                if t >= begin - timedelta(seconds=(param.WIN_SIZE - 1 / FREQ)):    # WIN_SIZE must be longer than 1 / FREQ
                    slice_time_index = i
                    break
            self.ts = self.ts[slice_time_index:]
            self.val = self.val[slice_time_index:]

        if end is not None:
            slice_time_index = -1
            for i, t in enumerate(self.ts):
                if t > end:
                    slice_time_index = i
                    break
            self.ts = self.ts[:slice_time_index]
            self.val = self.val[:slice_time_index]

    def export_to_pkl(self, file_name) -> None:
        with open(file_name[:-4] + ".pkl", "wb") as f:
            pickle.dump((self.ts, self.val), f)

    def vis(self, begin: Union[datetime, None] = None, end: Union[datetime, None] = None, enable_lim: bool = False, component_lim: Any = (-1, 1), norm_lim: Any = (0, 2)) -> None:
        if begin is None:
            begin = self.ts[0]
        if end is None:
            end = self.ts[-1]

        titles = ("X", "Y", "Z")
        axes: np.ndarray = plt.subplots(nrows=4 * len(SENSOR_LIST), figsize=(16, 16 * len(SENSOR_LIST)))[1]
        for i, s in enumerate(SENSOR_LIST):
            for j in range(3):
                axes[4*i+j].set_title(s + "_" + titles[j])
                axes[4*i+j].set_xlim((begin, end))
                if enable_lim:
                    axes[4*i+j].set_ylim(component_lim)
                axes[4*i+j].plot(self.ts, self.val[:, 3*i+j])
            axes[4*i+3].set_title(s + "_" + "NORM")
            axes[4*i+3].set_xlim((begin, end))
            if enable_lim:
                axes[4*i+3].set_ylim(norm_lim)
            axes[4*i+3].plot(self.ts, np.linalg.norm(self.val[:, 3*i:3*i+3], axis=1))
