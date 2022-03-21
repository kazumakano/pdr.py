from __future__ import annotations
import os.path as path
from typing import Optional
import cv2
import numpy as np
import particle_filter.script.parameter as pf_param
import yaml
from particle_filter.script.map import Map as PfMap


class Map(PfMap):
    def __init__(self, result_dir: Optional[str] = None) -> None:
        self.plain_img: np.ndarray | None = cv2.imread(path.join(pf_param.ROOT_DIR, "map/", pf_param.IMG_FILE))
        if self.plain_img is None:
            raise Exception(f"map.py: map image file {pf_param.IMG_FILE} was not found")
        self.clear()

        with open(path.join(pf_param.ROOT_DIR, "map/", pf_param.CONF_FILE)) as f:
            self.resolution = np.float32(yaml.safe_load(f)["resolution"])
        if result_dir is not None:
            self.result_dir = result_dir

    def draw_pos(self, pos: np.ndarray) -> None:
        if pf_param.ENABLE_CLEAR:
            self.clear()
        self._draw_pos((0, 0, 255), False, pos)
