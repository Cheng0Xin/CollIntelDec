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
            communication_distance=5,
            h=8,
            k=20
    ):
        # constance
        self.foot_step = foot_step
        self.body_size = body_size
        self.communication_distance = communication_distance
        self.timer_scale = timer_scale
        self.h = h
        self.k = k
        self.delta = 50 * 31 * 0.000594

        # movement
        self.direction = 0
        self.direction_vector = np.zeros(2)

        # internal state
        self.opn = np.ones(10) * 0.1
        self.op = -1
        self.v0 = 0.1
        self.exploit_state = Robot.EXPLOIT
        self.comm_state = Robot.NOT_COMMIT
        self.renew_timer()

    def renew_timer(self):
        self.timer = np.random.exponential() * self.timer_scale

    def random_orientation(self):
        self.direction = np.random.rand() * 2 * np.pi
        self.direction_vector = np.array(
            [np.cos(self.direction), np.sin(self.direction)]
        )

    def comm_prob(self):
        return self.k * self.v0

    def abandon_prob(self):
        return self.k * (1 - self.v0)

    def interaction_prob(self):
        return self.h * self.v0

    def think(self):
        rg = [sum(self.opn[: idx]) for idx in range(1, len(self.opn))]
        rg.reverse()
        rg = np.array(rg)
        count = np.count_nonzero(rg < np.random.rand())
        self.op = len(self.opn) - 1 - count
        self.v0 = self.opn[self.op]

    def __str__(self):
        return f"Direction: ({self.direction_vector[0]}, {self.direction_vector[1]})"

    def next_step(self, loc):
        return loc + self.direction_vector * self.foot_step
