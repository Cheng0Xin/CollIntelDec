#!/usr/bin/env python
# -*- coding: utf-8 -*-
from arena import Arena
from decision import CDCIDecision
import numpy as np
# import matplotlib.pyplot as plt


def run_random_work_and_plot(arena: Arena):
    for idx in range(300000):
        arena.random_walk()


def get_hypo():
    vec = np.array([round(0.05 * x, 2) for x in range(1, 20, 2)])
    return np.array([vec, 1 - vec]).transpose()


if __name__ == "__main__":
    decision = CDCIDecision(hypo=get_hypo())
    arena = Arena(decision)

    run_random_work_and_plot(arena)
