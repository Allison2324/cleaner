import numpy as np


SIZE = (32, 32)
CLEANER = 64
NONE = 0
DUST = 1
WALL = 255
"""
DIRECTIONS:
    0: UP
    1: RIGHT
    2: DOWN
    3: LEFT
"""
DIRECTIONS = [np.array([0, 1]),
              np.array([-1, 0]),
              np.array([0, -1]),
              np.array([1, 0])]
