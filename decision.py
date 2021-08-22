#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np

from arena import Arena
from robot import Robot


class CDCIDecision(object):
    def __init__(self, arena: Arena):
        self.area = arena
        self.result = np.zeros(self.area.num_of_agents)

    def make_decision(self):
        locations = self.area.robots_locations
# self.area.environment[loc[0]][loc[1]]
        robot_tmp_result = [self.area.environment[int(loc[0])][int(loc[1])] 
                  for loc in locations]
        self.result += robot_tmp_result
        print(f"Debug: {self.result}")

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
