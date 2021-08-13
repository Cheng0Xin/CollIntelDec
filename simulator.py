#!/usr/bin/env python
# -*- coding: utf-8 -*-
from arena import *
import matplotlib.pyplot as plt


if __name__ == "__main__":
    a = Arena(None)
    for idx in range(300000):
        a.random_walk()
        if idx % 5 == 0:
            a.plot(plt)
        print(f"No. {idx}")

