import gym
from gym import error, spaces, utils
from gym import spaces, logger
from gym.utils import seeding

from itertools import combinations
import numpy as np


class CametEnv(gym.Env):
    metadata = {
        'render.modes': ['human', 'rgb_array'],
        'video.frames_per_second': 50
    }

    def __init__(self):
        self.hood = [i for i in set(combinations([-1, 0, 1] * 2, 2)) if i != (0, 0)]
        self.rule = {True: (2, 3), False: (3, 3)}
        self.board_dim = (5, 5)

        self.history = []
        self.action_space = spaces.Discrete(np.product(self.board_dim))
        self.observation_space = spaces.MultiBinary(np.product(self.board_dim))

        self.seed()
        self.viewer = None
        self.state = None

        self.steps_beyond_done = None

    def seed(self, seed=None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

    def get_next_state(self, state):

        hood_state = np.zeros(self.board_dim)
        next_state = np.zeros(self.board_dim)
        dim_state = len(self.board_dim)
        dim_state_tuple = tuple([i for i in range(dim_state)])

        for h in self.hood:
            hood_state += np.roll(state, h, dim_state_tuple)

        for key in self.rule:
            next_state[(state == key) & (hood_state >= self.rule[key][0]) & (hood_state <= self.rule[key][1])] = 1

        return next_state

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        state = self.state

        if state[action] == 1:
            state[action] = 0
        else:
            state[action] = 1

        # row = int(action / self.board_dim[0])
        # col = int(action % self.board_dim[1])

        # if state[row][col] == 1:
        #     state[row][col] = 0
        # else:
        #     state[row][col] = 1

        self.state = self.get_next_state(state.reshape(self.board_dim)).reshape(np.product(self.board_dim))

        done = any((self.state == x).all() for x in self.history)

        if not done:
            reward = 1
            self.history.append(self.state)
        elif self.steps_beyond_done is None:
            self.steps_beyond_done = 0
            reward = 1
        else:
            if self.steps_beyond_done == 0:
                logger.warn("You are calling 'step()' even though this environment has already returned done = True. "
                            "You should always call 'reset()' once you receive 'done = True' "
                            "-- any further steps are undefined behavior.")
            self.steps_beyond_done += 1
            reward = 0

        return self.state, reward, done, {}

    def reset(self):
        self.state = self.np_random.randint(0, 1+1, np.product(self.board_dim))
        self.history.append(self.state)
        self.steps_beyond_done = None
        return self.state

    def render(self, mode='human', close=False):

        box_length = 20

        screen_width = self.board_dim[1] * box_length
        screen_height = self.board_dim[0] * box_length

        if self.viewer is None:
            from gym_camet.envs import rendering
            self.viewer = rendering.Viewer(screen_width, screen_height)

            for n in range(self.board_dim[0]):
                for m in range(self.board_dim[1]):
                    i = m*box_length
                    j = screen_height - n*box_length
                    v = [(i, j), (i, j-box_length), (i+box_length, j-box_length), (i+box_length, j)]
                    cell = rendering.make_polygon(v)

                    if self.state.reshape(self.board_dim)[n][m] == 1:
                        cell.set_color(0, 0, 0)
                    else:
                        cell.set_color(1, 1, 1)

                    self.viewer.add_geom(cell)

            if self.state is None: return None

        return self.viewer.render(return_rgb_array=mode == 'rgb_array')

    def print_state(self):
        print(self.state)
        print(self.state.reshape(self.board_dim))

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None

