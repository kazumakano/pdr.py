import math
import numpy as np


class Turtle:
    def __init__(self, init_pos: np.ndarray, init_heading: np.float32) -> None:
        self.pos = init_pos.astype(np.float64)
        self.heading = init_heading

    def forward(self, dist: np.float64) -> None:
        self.pos += (dist * np.array((math.cos(math.radians(self.heading)), math.sin(math.radians(self.heading))))).astype(np.float64)

    def setheading(self, to_angle: np.float64) -> None:
        self.heading = to_angle
