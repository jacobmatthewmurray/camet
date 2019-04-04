import numpy as np
from itertools import combinations
import matplotlib.pyplot as plt
from matplotlib import colors


class Camet:

    def __init__(self, x, y):

        self.hood = [i for i in set(combinations([-1, 0, 1] * 2, 2)) if i != (0, 0)]
        self.rule = {True: (2, 3), False: (3, 3)}
        self.dimensions = (x, y)
        self.history = []

        self.state = None

    def seed(self, pattern='random'):

        if pattern == 'random':

            return np.random.choice(2, np.product(self.dimensions), p=[0.5, 0.5])

    def get_next_generation(self, state):

        state = state.reshape(self.dimensions)

        hood_state = np.zeros(self.dimensions)
        next_state = np.zeros(self.dimensions)
        dim_state = len(self.dimensions)
        dim_state_tuple = tuple([i for i in range(dim_state)])

        for h in self.hood:
            hood_state += np.roll(state, h, dim_state_tuple)

        for key in self.rule:
            next_state[(state == key) & (hood_state >= self.rule[key][0]) & (hood_state <= self.rule[key][1])] = 1

        return next_state.reshape(np.product(self.dimensions))

    def reset(self, pattern='random'):
        self.history = []
        self.state = self.seed(pattern)

    def check_game_over(self):

        if (list(self.state) in [list(i) for i in self.history]) or (sum(self.state) <= self.rule[True][0]):
            return True
        else:
            return False

    def plot_state(self, state):

        state = state.reshape(self.dimensions)

        cmap = colors.ListedColormap(['white', 'black'])

        fig, ax = plt.subplots(figsize=(4, 4))
        ax.set_xticks([])
        ax.set_yticks([])

        ax.imshow(state, cmap=cmap)

        plt.show()

    def make_random_move(self):

        move = np.random.randint(np.product(self.dimensions))

        if self.state[move] == 1:
            self.state[move] = 0
        else:
            self.state[move] = 1

    def make_move(self, move_index):

        if self.state[move_index] == 1:
            self.state[move_index] = 0
        else:
            self.state[move_index] = 1
