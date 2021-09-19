'''
CPSC 415 -- Homework #2 support file
Stephen Davies, University of Mary Washington, fall 2021
'''

import numpy as np
import math
import pickle

class Atlas():

    LONG_RANGE = (0,1000)
    LAT_RANGE = (0,1000)
    count = 0
    def __init__(self, num_cities=10):
        self._num_cities = num_cities
        self._longs = np.random.uniform(*Atlas.LONG_RANGE, self._num_cities)
        self._lats = np.random.uniform(*Atlas.LAT_RANGE, self._num_cities)
        self._adj_mat = gen_adj_mat(self._longs, self._lats)
        self._paths_expanded = []
        self._nodes_expanded = set()

    def find_the_next_heroistic(self, history, visited, reached):
        if not reached:
            track_heroistic = []
            for i in range(len(visited)):
                track_heroistic.append([visited[i][0], visited[i][1], visited[i][2], visited[i][3]])
            
            low_heroistic = track_heroistic[0]
            for i in range(len(track_heroistic)):
                if low_heroistic[2] > track_heroistic[i][2]:
                    low_heroistic = track_heroistic[i]

            expand_node = 0
            for i in range(len(visited)):
                if visited[i][3] == low_heroistic[3]:
                    expand_node = visited[i][1]

            expand_pair = []
            for i in range(len(history)):
                if history[i][0] == expand_node:
                    expand_pair.append(history[i])

            temp_list = low_heroistic.copy()
            if self.count > 0:
                low_heroistic[2] = low_heroistic[2] - low_heroistic[3]

            if not expand_pair:
                visited.remove(temp_list)
                self.count + 1
                return self.find_the_next_heroistic(history, visited, reached)
            else:
                for i in range(len(expand_pair)):
                    expand_pair[i][2] = low_heroistic[2] + expand_pair[i][2] + expand_pair[i][3]
                visited.extend(expand_pair)
                self.count = self.count + 1
                return expand_pair
        else:
            return reached
    
    def node_expansion(self, next, atlas, goal, reached):
        for i in range(len(next)):
            distance = atlas.get_road_dist(next[i][0], next[i][1])
            print(self._nodes_expanded)
            if goal == next[i][1]:
                reached = True
        return reached

    def get_road_dist(self, i, j):
        self._paths_expanded.append((i,j))
        self._nodes_expanded |= {i}
        return self._adj_mat[i,j]

    def get_crow_flies_dist(self, i, j):
        return math.hypot(self._longs[i]-self._longs[j],
                                                self._lats[i]-self._lats[j])

    def get_num_cities(self):
        return self._num_cities

    def __str__(self):
        return 'an atlas of {} cities'.format(self._num_cities)

    def __repr__(self):
        return self._adj_mat.__repr__()

    @classmethod
    def from_filename(cls, filename):
        with open(filename,'rb') as f:
            return pickle.load(f)


def gen_adj_mat(longs, lats, prob_edge=.2,
                        additional_length=lambda: np.random.exponential(20,1)):
    '''Get an adjacency matrix for the cities whose longitudes and latitudes
    are passed. Each entry will either be a number somewhat greater than the
    crow-flies distance between the two cities (with probability prob_edge),
    or math.inf. The matrix will consist of floats, and be symmetric. The
    diagonal will be all zeroes. The "somewhat greater" is controlled by the
    additional_length parameter, a function returning a random amount.'''

    # Generate full nxn Bernoulli's, even though we'll only use the upper
    # triangle.
    edges = np.random.binomial(1, prob_edge, size=(len(longs),len(longs)))
    am = np.zeros((len(longs),len(longs)))
    for i in range(len(longs)):
        for j in range(len(longs)):
            if i==j:
                am[i,i] = 0
            elif i < j:
                if edges[i,j] == 1:
                    am[i,j] = (math.hypot(longs[i]-longs[j],lats[i]-lats[j])
                        + additional_length())
                    am[j,i] = am[i,j]
                else:
                    am[i,j] = am[j,i] = math.inf
    return np.around(am,1)

