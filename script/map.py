import os.path as path
import cv2
import numpy as np
import particle_filter.script.parameter as pf_param
import particle_filter.script.utility as pf_util
import yaml
from particle_filter.script.map import Map as PfMap


class Map(PfMap):
    def __init__(self) -> None:
        self.plain_img: np.ndarray = cv2.imread(path.join(pf_param.ROOT_DIR, "map/", pf_param.IMG_FILE))
        self.img = self.plain_img.copy()
        with open(path.join(pf_param.ROOT_DIR, "map/", pf_param.CONF_FILE)) as f:
            self.resolution = np.float16(yaml.safe_load(f)["resolution"])

        if pf_param.ENABLE_SAVE_IMG or pf_param.ENABLE_SAVE_VIDEO:
            if pf_param.RESULT_FILE_NAME is None:
                self.result_file_name = pf_util.gen_file_name()
            else:
                self.result_file_name = pf_param.RESULT_FILE_NAME

    def draw_pos(self, pos: np.ndarray) -> None:
        if pf_param.ENABLE_CLEAR:
            self.clear()
        self._draw_pos((0, 0, 255), False, pos)
