from constants import *
import numpy as np
from cleaner import Cleaner
import pygame as pg


class World(object):
    def __init__(self, probability):
        self.count_of_steps = 0
        self.size = SIZE
        self.probability = probability
        self.map = np.zeros(self.size, dtype=int)
        self.map[:, self.size[1] - 1] = WALL
        self.map[:, 0] = WALL
        self.map[self.size[0] - 1, :] = WALL
        self.map[0, :] = WALL
        self.init_dusts()
        # self.init_inner_walls()
        self.cleaner = Cleaner(self.init_cleaner())
        self.zoom_factor = 20
        self.renderer = None

    def init_dusts(self):
        for i in range(1, self.size[0] - 1):
            for j in range(1, self.size[1] - 1):
                r_number = np.random.randint(self.size[0])
                if r_number < self.probability * self.size[0]:
                    self.map[i][j] = DUST

    def init_cleaner(self):
        r_number_x = np.random.randint(self.size[0] - 2) + 1
        r_number_y = np.random.randint(self.size[1] - 2) + 1
        start_position = (r_number_x, r_number_y)
        self.map[start_position] = CLEANER
        return start_position

    def init_inner_walls(self):
        self.map[6][5:8] = WALL
        self.map[4][5:10] = WALL

    def count_of_dusts(self):
        return np.count_nonzero(self.map == 1)

    def get_dusts(self):
        list_of_dusts = []
        for i in range(self.size[0]):
            for j in range(self.size[1]):
                if self.map[i][j] == 1:
                    list_of_dusts.append((i, j))
        return list_of_dusts

    def get_colors(self):
        colors = [[0] * self.size[0] for _ in range(self.size[1])]

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                # Wall = BLACK
                if self.map[i][j] == 255:
                    colors[i][j] = [0, 0, 0]
                # None = WHITE
                elif self.map[i][j] == 0:
                    colors[i][j] = [255, 255, 255]
                # Dust = YELLOW
                elif self.map[i][j] == 1:
                    colors[i][j] = [255, 255, 0]
                # Cleaner = RED
                elif self.map[i][j] == 64:
                    colors[i][j] = [255, 0, 0]
        return colors

    def move(self, direction):
        dir = 0
        if direction == "UP":
            dir = DIRECTIONS[0]
        elif direction == "RIGHT":
            dir = DIRECTIONS[1]
        elif direction == "DOWN":
            dir = DIRECTIONS[2]
        elif direction == "LEFT":
            dir = DIRECTIONS[3]
        pos = list(self.cleaner.pos - dir)
        if self.map[pos[0]][pos[1]] == 255:
            print("Wall on " + direction)
        else:
            self.map[self.cleaner.pos[0]][self.cleaner.pos[1]] = 0
            self.cleaner.pos = pos
            self.map[pos[0]][pos[1]] = 64
            self.count_of_steps += 1
