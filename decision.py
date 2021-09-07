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
        r1 = robot[robot_idx_i]
        r2 = robot[robot_idx_j]

        if np.random.rand() < r1.interaction_prob():
            return

        if r1.comm_state != Robot.COMMIT:
            if r2.comm_state == Robot.COMMIT:
                r1.op = r2.op
                r1.comm_state = Robot.COMMIT
            return

        if r2.comm_state == Robot.COMMIT:
            # print("COMM STATE")
            if r1.op == r2.op:
                pass
            else:
                r1.comm_state = Robot.NOT_COMMIT
                r2.comm_state = Robot.NOT_COMMIT
                r1.op = -1
                r2.op = -1
        else:
            r2.op = r1.op
            r2.comm_state = Robot.COMMIT
