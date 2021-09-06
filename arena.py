# -*- coding: utf-8 -*-
import numpy as np
from robot import Robot
import matplotlib.pyplot as plt
import collections


class Arena(object):
    def __init__(self, decision_agent=None, foot_step=1.16,
                 body_size=1, num_of_agents=10,
                 pattern='random', ratio=0.75,
                 width=20, length=20,
                 hypothesis=None):
        # initialize class members
        self.foot_step = foot_step
        self.body_size = body_size
        self.num_of_agents = num_of_agents
        self.pattern = pattern
        self.ratio = ratio
        self.width = width
        self.length = length
        self.decision_agent = decision_agent

        # the plant field
        self.environment = None
        self.robots = None
        # the robots
        self.robots_locations = None

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

        self.robots = [Robot(self.foot_step)
                       for _ in range(self.num_of_agents)]
        self.robots_locations = np.random.rand(self.num_of_agents, 2) * \
            np.array([self.width, self.length])
        # self.robots_locations = np.zeros((10, 2))

        coll_s = self.collision_detection()
        while coll_s is not None:
            for robot in coll_s:
                self.robots_locations[robot] = new_location()
            coll_s = self.collision_detection()

    def __init_arena(self):
        if self.pattern == 'random':
            vf = np.vectorize(lambda x: 0 if x else 1)
            self.environment = vf(np.random.rand(
                self.length, self.width) > self.ratio)

    def check_border_collision(self):
        result = list()

        above_right = np.where(self.robots_locations + self.body_size >
                               np.array([self.width, self.length]))
        result.extend([x for x, _ in zip(*above_right)])

        below_left = np.where(self.robots_locations < self.body_size)
        # print(f"Debug (loc): {self.robots_locations}")
        # print(f"Debug (edge): {self.robots_locations < self.body_size}")
        # print(f"Debug (nodes): {below_left}")
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

    def random_walk(self, step: int):
        locations = self.robots_locations.copy()
        # print(f"Random start: {self.robots_locations}")
        for idx, robot in enumerate(self.robots):
            robot.random_orientation()
            self.robots_locations[idx] = robot.next_step(locations[idx])

        coll_s = self.collision_detection()

        while coll_s is not None:
            for robot_idx in coll_s:
                self.robots[robot_idx].random_orientation()
                self.robots_locations[robot_idx] = self.robots[robot_idx].next_step(locations[robot_idx])
            coll_s = self.collision_detection()
            # print(f"Coll_s: {self.robots_locations}")

        distances = self.robots_distances()
        # print(distances)

        for robot in self.robots:
            robot.timer -= 1
            if step % 20 == 0:
                robot.think()
            if robot.comm_state == Robot.NOT_COMMIT and \
               np.random.rand() < robot.comm_prob():
                robot.comm_state = Robot.COMMIT
            # print(f"COMM Prob: {robot.comm_prob()}, {robot.comm_state}")

            if robot.timer <= 0:
                robot.exploit_state = not robot.exploit_state
                robot.renew_timer()
                print(f"Timer: {robot.timer}")

        for robot_idx, robot in enumerate(self.robots):
            if robot.exploit_state == Robot.EXPLOIT:
                (loc_x, loc_y) = self.robots_locations[idx]

                if self.environment[int(loc_x)][int(loc_y)]:
                    loc = [1, 0]
                else:
                    loc = [0, 1]
                self.decision_agent.gen_opinion(robot, loc)
                # print(f"OP: {robot.v0}, {robot.op}")
            if robot.exploit_state == Robot.NOT_EXPLOIT:
                neibour_idx_list = [idx for idx, dis
                                    in enumerate(distances[robot_idx])
                                    if dis < robot.communication_distance and
                                    idx != robot_idx]
                for dst_idx in neibour_idx_list:
                    self.decision_agent.exchange_opinion(self.robots,
                                                         robot_idx, dst_idx)
        for robot in self.robots:
            if robot.comm_state == Robot.COMMIT and \
               np.random.rand() < robot.abandon_prob():
                robot.comm_state = Robot.NOT_COMMIT
                robot.op = -1

    def get_dominate(self):
        robot_ops = [robot.op for robot in self.robots]
        res = collections.Counter(robot_ops)
        m_value = 0
        m_idx = -1
        for k, v in res.items():
            if m_value < v:
                m_value = v
                m_idx = k
        print(m_idx)

    def plot(self, fig, axis):
        # re-draw arena
        axis[0, 0].cla()
        axis[0, 1].cla()
        axis[1, 0].cla()

        # Robot walking
        for idx, row in enumerate(self.environment):
            for idy, v in enumerate(row):
                if v == 1:
                    axis[0, 0].fill_between([idx, idx + 1],
                                            idy, idy + 1, fc='black')
        for idx, (x, y) in enumerate(self.robots_locations):
            axis[0, 0].scatter(x, y, marker="*")

        # Opinion
        robot_ops = [robot.op for robot in self.robots]
        axis[0, 1].plot(robot_ops, 'r+')
        plt.draw()
        plt.pause(0.5)
