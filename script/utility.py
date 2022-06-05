import numpy as np


def meter2pixel(dist: np.ndarray, resolution: np.float32) -> np.ndarray:
    return dist / resolution
