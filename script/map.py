import cv2
import numpy as np
import particle_filter.script.parameter as pf_param
import particle_filter.script.utility as pf_util
import yaml
from particle_filter.script.map import Map as PfMap


class Map(PfMap):
    def __init__(self) -> None:
        self.plain_img: np.ndarray = cv2.imread(pf_param.ROOT_DIR + "map/" + pf_param.IMG_FILE)
        self.img = self.plain_img.copy()    # deep copy
        with open(pf_param.ROOT_DIR + "map/" + pf_param.CONF_FILE) as f:
            self.resolution: float = yaml.safe_load(f)["resolution"]
        
        if pf_param.ENABLE_SAVE_VIDEO or pf_param.ENABLE_SAVE_IMG:
            if pf_param.FILE_NAME is None:
                self.file_name = pf_util.gen_file_name()    # generate file name if unspecified
            else:
                self.file_name = pf_param.FILE_NAME
    
    def draw_any_pos(self, pos: np.ndarray) -> None:
        if pf_param.ENABLE_CLEAR:
            self.clear()
        try:
            super().draw_any_pos(pos, (0, 0, 255))
        except:
            print("map.py: error occurred when drawimg position")
            print(f"map.py: position is {pos}")
