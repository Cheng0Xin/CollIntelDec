#!/usr/bin/env python
# -*- coding: utf-8 -*-
from arena import Arena
from decision import CDCIDecision
import matplotlib.pyplot as plt


def run_random_work_and_plot(arena: Arena):
    arena.random_walk()
    for idx in range(300000):
        arena.random_walk()
        if idx % 5 == 0:
            arena.plot(plt)
        print(f"No. {idx}")


if __name__ == "__main__":
    a = Arena()
    run_random_work_and_plot(a)
    b = CDCIDecision(a)
    b.get_neighbours(2)

