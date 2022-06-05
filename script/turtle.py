import math
import numpy as np


class Turtle:
    def __init__(self, init_pos: np.ndarray, init_heading: np.float32) -> None:
        self.pos = init_pos.astype(np.float64)
        self.heading = init_heading

    def forward(self, dist: np.float64) -> None:
        radian_heading = math.radians(self.heading)
        self.pos += dist * np.array((math.cos(radian_heading), math.sin(radian_heading)), dtype=np.float64)

    def setheading(self, to_angle: np.float64) -> None:
        self.heading = to_angle
