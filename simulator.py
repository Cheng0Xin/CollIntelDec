#!/usr/bin/env python
# -*- coding: utf-8 -*-
from arena import Arena
from decision import CDCIDecision
import matplotlib.pyplot as plt


def run_random_work_and_plot(decision: CDCIDecision):
    decision.area.random_walk()
    for idx in range(300000):
        decision.area.random_walk()

        if idx % 5 == 0:
            # decision.area.plot(plt)
            decision.make_decision()
        # print(f"No. {idx}")


if __name__ == "__main__":
    arena = Arena()
    decision = CDCIDecision(arena)
    run_random_work_and_plot(decision)

