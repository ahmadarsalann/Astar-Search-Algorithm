#!/usr/bin/env python3

'''
CPSC 415 -- Homework #2 template
Arsalan Ahmad, University of Mary Washington, fall 2021
'''

from math import inf

from numpy.random.mtrand import rand
from atlas import Atlas
import numpy as np
import logging
import sys


def find_best_path(atlas):
    '''Finds the best path from src to dest, based on costs from atlas.
    Returns a tuple of two elements. The first is a list of city numbers,
    starting with 0 and ending with atlas.num_cities-1, that gives the
    optimal path between those two cities. The second is the total cost
    of that path.'''

    # THIS IS WHERE YOUR AMAZING CODE GOES
    full_list = atlas._adj_mat
    x = atlas._adj_mat[0]
    y = [i[0] for i in full_list]
    track_combos = []
    history = []
    for a in range(len(x)):
        for b in range(len(y)):
                if full_list[a][b] != 0 and full_list[a][b] != inf:
                    track_combos.append([a, b, full_list[a][b]])
    
    history = track_combos.copy()
    print(track_combos)
    l = 0
    for i in range(len(history)):
        if i == len(history):
            break
        for f in range(len(track_combos)):
            if track_combos[f][0] == history[i][0] and track_combos[f][1] == history[i][1] or track_combos[f][0] == history[i][1] and track_combos[f][1] == history[i][0]:
                l = l + 1
            if l == 2:
                history.pop(f)
                track_combos.pop(f)
                l = 0
                break
    
    # to set a heroistic
    for i in range(len(history)):
        heroistic = atlas.get_crow_flies_dist(history[i][0], history[i][1])
        history[i].append(heroistic)

    print(history)
    
    

    # Here's a (bogus) example return value:
    return ([0,3,2,4],970)



if __name__ == '__main__':

    if len(sys.argv) not in [2,3]:
        print("Usage: gps.py numCities|atlasFile [debugLevel].")
        sys.exit(1)

    if len(sys.argv) > 2:
        if sys.argv[2] not in ['DEBUG','INFO','WARNING','ERROR']:
            print('Debug level must be one of: DEBUG, INFO, WARNING, ERROR.')
            sys.exit(2)
        logging.getLogger().setLevel(sys.argv[2])
    else:
        logging.getLogger().setLevel('INFO')

    try:
        num_cities = int(sys.argv[1])
        logging.info('Building random atlas with {} cities...'.format(
            num_cities))
        usa = Atlas(num_cities)
        logging.info('...built.')
    except:
        logging.info('Loading atlas from file {}...'.format(sys.argv[1]))
        usa = Atlas.from_filename(sys.argv[1])
        logging.info('...loaded.')

    path, cost = find_best_path(usa)
    print('Best path from {} to {} costs {}: {}.'.format(0,
        usa.get_num_cities()-1, cost, path))
    print('You expanded {} nodes: {}'.format(len(usa._nodes_expanded),
        usa._nodes_expanded))

