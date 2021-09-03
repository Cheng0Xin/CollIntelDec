#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np


class Robot(object):

    # Constance
    COMMIT = True
    NOT_COMMIT = False

    # Decision ways
    EXPLOIT = True
    NOT_EXPLOIT = False

    def __init__(
            self,
            foot_step,
            body_size=1,
            timer_scale=5,
            communication_distance=5):
        # constance
        self.foot_step = foot_step
        self.body_size = body_size
        self.communication_distance = communication_distance
        self.timer_scale = timer_scale

        # movement
        self.direction = 0
        self.direction_vector = np.zeros(2)

        # internal state
        self.opn = np.ones(10) * 0.1
        self.exploit_state = Robot.EXPLOIT
        self.comm_state = Robot.NOT_COMMIT
        self.renew_timer()

    def renew_timer(self):
        self.timer = np.random.exponential() * self.timer_scale

    def gen_opinion(self):
        if self.commit and self.state:
            self.opinion = 0
        if self.commit and not self.state:
            pass

    def random_orientation(self):
        self.direction = np.random.rand() * 2 * np.pi
        self.direction_vector = np.array(
            [np.cos(self.direction), np.sin(self.direction)]
        )

    def __str__(self):
        return f"Direction: ({self.direction_vector[0]}, {self.direction_vector[1]})"

    def next_step(self, loc):
        return loc + self.direction_vector * self.foot_step
