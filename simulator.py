#!/usr/bin/env python
# -*- coding: utf-8 -*-
from arena import Arena
from decision import CDCIDecision
import numpy as np
import matplotlib.pyplot as plt


def run_random_work_and_plot(arena: Arena):
    fig, axis = plt.subplots(1, 2, figsize=(15, 7))
    fig.show()
    for idx in range(300000):
        arena.random_walk(idx)
        if idx % 20 == 0:
            arena.plot(fig, axis)
        res_idx, res_value = arena.get_dominate()
        if res_value >= 9 and res_idx != -1:
            print(f"Result: {res_idx}, After time: {idx}")
            break


def get_hypo():
    vec = np.array([round(0.05 * x, 2) for x in range(1, 20, 2)])
    return np.array([vec, 1 - vec]).transpose()


if __name__ == "__main__":
    decision = CDCIDecision(hypo=get_hypo())
    arena = Arena(decision)

    run_random_work_and_plot(arena)
