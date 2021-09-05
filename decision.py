#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
from robot import Robot


class CDCIDecision(object):
    def __init__(self, hypo=None):
        self.hypo = hypo

    def gen_opinion(self, robot: Robot, obs: list):
        robot.opn = robot.opn * (self.hypo.dot(obs))
        robot.opn = robot.opn / np.sum(robot.opn)

    def exchange_opinion(self, robot: list[Robot], robot_idx_i, robot_idx_j):
        print(f"{robot_idx_i}, {robot_idx_j} exchange")
