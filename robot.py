#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


class Robot(object):

    # Constance
    COMMIT = True
    NOT_COMMIT = False

    def __init__(self, foot_step, body_size=1, communication_distance=5):
        # constance
        self.foot_step = foot_step
        self.body_size = body_size
        self.communication_distance = communication_distance

        # movement
        self.direction = 0
        self.direction_vector = np.zeros(2)

        # internal state
        self.state = Robot.NOT_COMMIT

    def random_orientation(self):
        self.direction = np.random.rand() * 2 * np.pi
        self.direction_vector = np.array([np.cos(self.direction), np.sin(self.direction)])

    def __str__(self):
        return f"Direction: ({self.direction_vector[0]}, {self.direction_vector[1]})"

    def next_step(self, loc):
        return loc + self.direction_vector * self.foot_step
