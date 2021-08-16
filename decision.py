#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from arena import Arena
from robot import Robot


class CDCIDecision(object):
    def __init__(self, arena: Arena):
        self.area = arena

    def make_decision(self):
        pass

    def get_neighbours(self, robot_idx: int):
        neighbours = [y for x, y in
                      zip(*np.where(self.area.robots_distances() <
                                    self.area.robots[robot_idx].communication_distance))
                      if x != y and x == robot_idx]

        if len(neighbours) != 0:
            return neighbours
        return None

    def communication(self, robot_idx_i, robot_idx_j):
        pass
