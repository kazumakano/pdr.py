import os.path as path
from typing import Union
import cv2
import numpy as np
import particle_filter.script.parameter as pf_param
import particle_filter.script.utility as pf_util
import yaml
from particle_filter.script.map import Map as PfMap


class Map(PfMap):
    def __init__(self, result_dir: Union[str, None]) -> None:
        self.plain_img: Union[np.ndarray, None] = cv2.imread(path.join(pf_param.ROOT_DIR, "map/", pf_param.IMG_FILE))
        if self.plain_img is None:
            raise Exception(f"map.py: map image file {pf_param.IMG_FILE} was not found")
        self.img = self.plain_img.copy()
        with open(path.join(pf_param.ROOT_DIR, "map/", pf_param.CONF_FILE)) as f:
            self.resolution = np.float16(yaml.safe_load(f)["resolution"])
        self.result_dir = result_dir

    def draw_pos(self, pos: np.ndarray) -> None:
        if pf_param.ENABLE_CLEAR:
            self.clear()
        self._draw_pos((0, 0, 255), False, pos)
