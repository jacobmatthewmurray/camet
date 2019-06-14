import math
import random
import numpy as np
from scipy import sparse

"""
dimensions = tuple(x,y,z,...) 
radius = float

"""


def make_voronoi_seeds(dimensions, radius):

    check_matrix = np.zeros([i//radius for i in dimensions] + [len(dimensions)])
    hood_size = 2

    # choose random

    random_seed = [random.uniform(0, i) for i in dimensions]
    random_seed_idx = [int(i) for i in random_seed]

    # no looping boundary

    for i in range(hood_size):





