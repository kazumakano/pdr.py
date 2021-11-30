import math
import numpy as np


class Turtle:
    def __init__(self, init_pos: np.ndarray, init_heading: np.float16) -> None:
        self.pos = init_pos.astype(np.float64)
        self.heading = init_heading
    
    # move forward
    def forward(self, dist: np.float64) -> None:
        self.pos += dist * np.array((math.cos(math.radians(self.heading)), math.sin(math.radians(self.heading))), dtype=np.float64)

    # turn right
    def right(self, angle: np.float64) -> None:
        self.heading += angle
