#!/usr/bin/env python
# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt


class Robot(object):
    def __init__(self, foot_step, body_size=1):
        # constance
        self.foot_step = foot_step
        self.body_size = body_size

        # movement
        self.direction = 0
        self.direction_vector = np.zeros(2)

    def random_orientation(self):
        self.direction = np.random.rand() * 2 * np.pi
        self.direction_vector = np.array([np.cos(self.direction), np.sin(self.direction)])

    def __str__(self):
        return f"Direction: ({self.direction_vector[0]}, {self.direction_vector[1]})"

    def next_step(self, loc):
        return loc + self.direction_vector * self.foot_step


class Arena(object):
    def __init__(self, decision_engine, foot_step = 0.16, 
                 body_size = 1, num_of_agents=10, 
                 pattern='random', ratio=0.75, width=20, length=20):
        # initialize class members
        self.decision_engine = decision_engine
        self.foot_step = foot_step
        self.body_size = body_size
        self.num_of_agents = num_of_agents
        self.pattern = pattern
        self.ratio = 0.75
        self.width = width
        self.length = length

        self.environment = None # the plant field
        self.robots = None
        self.robots_locations = None # the robots

        # initialization
        self.__init_arena()
        self.__init_agent()

    def collision_detection(self):
        result = list()

        # Collision between robots
        coll_between_robots = np.where(self.robots_distances() < self.body_size)
        [result.extend([x, y]) for x, y in zip(*coll_between_robots) if x != y]

        coll_border = self.check_border_collision()
        if coll_border is not None:
            result.extend(coll_border)

        result = set(result)

        if len(result) != 0:
            return result
        return None

    def __init_agent(self):
        def new_location():
            return np.random.rand(2) * np.array([self.width, self.length])

        self.robots = [Robot(self.foot_step) for _ in range(self.num_of_agents)]
        self.robots_locations = np.random.rand(self.num_of_agents, 2) * \
            np.array([self.width, self.length])
        # self.robots_locations = np.zeros((10, 2))

        colls = self.collision_detection()
        while colls is not None:
            for robot in colls:
                self.robots_locations[robot] = new_location()
            colls = self.collision_detection()

    def __init_arena(self):
        if self.pattern == 'random':
            vf = np.vectorize(lambda x: 0 if x else 1)
            self.environment = vf(np.random.rand(self.length, self.width) > self.ratio)
            return
    
    def check_border_collision(self):
        result = list()

        above_right = np.where(self.robots_locations + self.body_size > np.array([self.width, self.length]))
        result.extend([x for x, _ in zip(*above_right)])

        below_left = np.where(self.robots_locations < self.body_size)
        print(f"Debug (loc): {self.robots_locations}")
        print(f"Debug (edge): {self.robots_locations < self.body_size}")
        print(f"Debug (nodes): {below_left}")
        result.extend([x for x, _ in zip(*below_left)])

        if len(result) != 0:
            return result

        return None

    def robots_distances(self):
        distance_mat = np.zeros((self.num_of_agents, self.num_of_agents))

        for i, x in enumerate(self.robots_locations):
            for j, y in enumerate(self.robots_locations):
                distance_mat[i][j] = np.sqrt(np.sum(np.power(x - y, 2)))
        return distance_mat

    def random_walk(self):
        locations = self.robots_locations.copy()
        print(f"Random start: {self.robots_locations}")
        for idx, robot in enumerate(self.robots):
            robot.random_orientation()
            self.robots_locations[idx] = robot.next_step(locations[idx])

        colls = self.collision_detection()

        while colls is not None:
            for robot_idx in colls:
                self.robots[robot_idx].random_orientation()
                self.robots_locations[robot_idx] = self.robots[robot_idx].next_step(locations[robot_idx])
            colls = self.collision_detection()
            print(f"Colls: {self.robots_locations}")
        print(f"Random end: {self.robots_locations}")

    def plot(self, plt):
        # re-draw arena
        plt.cla()

        for idx, row in enumerate(self.environment):
            for idy, v in enumerate(row):
                if v == 1:
                    plt.fill_between([idx, idx + 1], idy, idy + 1, fc='k')
        # plt.scattle()
        for idx, (x, y) in enumerate(self.robots_locations):
            plt.scatter(x, y, marker = "*")

        plt.draw()
        plt.pause(0.01)

