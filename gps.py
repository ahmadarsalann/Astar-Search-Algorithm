#!/usr/bin/env python3
 
'''
CPSC 415 -- Homework #2 template
Arsalan Ahmad, University of Mary Washington, fall 2021
'''
 
from math import dist, fabs, inf
from os import terminal_size
 
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
    first_node = 0
    Visited = []
    goal = atlas.get_num_cities() - 1
    total_cities = atlas.get_num_cities()
    for i in range(total_cities):
        first_node = atlas.get_road_dist(0, i)
        
        if first_node != inf and first_node != 0:

            hero = atlas.get_crow_flies_dist(i, goal)
            Visited.append([0, i, first_node, hero])
    b = 0
    i = 0
    reached = False
    track_nodes = []
    while True:
        next = find_the_next_path(Visited)
        track_nodes.append(next)

        if next[1] == total_cities - 1:
            break
        extend = extend_combo(next[1], Visited, total_cities, atlas, goal, track_nodes)
        i = i + 1   
    remove(track_nodes, atlas)
    #time to find the path
    path = []
    for i in range(len(track_nodes)):
        if i == 0:
            path.append(track_nodes[i][0])
            path.append(track_nodes[i][1])
        else:
            if path[i] == track_nodes[i][0]:
                path.append(track_nodes[i][1])
    #time to get the distance
    cost = total_path_cost(path, atlas)
    
    return (path,cost)
 
def remove(track_nodes, atlas):
    count = []
    number = 0
    temp_track = track_nodes.copy()
    for i in range(len(track_nodes)):
        for j in range(len(track_nodes)):
            if j == len(track_nodes):
                number = 0
            if track_nodes[j][0] == temp_track[i][0]:
                number = number + 1
        if number > 1:
            count.append([i, track_nodes[i][0]])
            number = 0
        number = 0
    a = 0
    check = 0
    increment = 0
    goes_to_if = False
    i = 0
    c = a
    while i < len(track_nodes):
        if a == len(count):
            break
        if i is len(track_nodes):
            break
        if count[a][0] == i:
            goes_to_if = True
            check = track_nodes[i][1]
            a = a + 1
            c = a
            for j in range(len(track_nodes)):
                if check == track_nodes[j][0]:
                    if j > i:
                        increment = increment + 1
        
        if increment == 0 and goes_to_if:
            track_nodes.pop(i)
            if a == len(count):
                break
            while c < len(count):
                count[c][0] = count[c][0] - 1
                c = c + 1
            i = i - 1
            goes_to_if = False
        else:
            increment = 0
            i = i + 1
            goes_to_if = False
 
    count3 = 0
    j = 1
    combos = []
    for i in range(len(track_nodes)):
        while j < len(track_nodes):
            if track_nodes[i][0] == track_nodes[j][0]:
                combos.append(track_nodes[i])
                combos.append(track_nodes[j])
            j = j + 1
 
    #Execute a path
    path = [[]]
    v = 0
    goal = atlas.get_num_cities() - 1
    for i in range(len(track_nodes)):
        if v == len(combos):
            break
        if combos[v] == track_nodes[i]:
            for j in range(len(track_nodes)):
                if j == len(track_nodes) - 1 and path[v] == []:
                    path[v].append(track_nodes[i][1])
                if track_nodes[i][1] == track_nodes[j][0]:
                    path[v].append(track_nodes[j][0])
                
                if track_nodes[j][0] in path[v]:
                    path[v].append(track_nodes[j][1])
            v = v + 1
            path.extend([[]])
    for i in range(len(path)):
        if i >= len(path):
            break
        if path[i] == []:
            path.pop(i)
    
    if len(path) > 1:
        unwanted = []
        for i in range(len(path)):
            if i == len(path):
                break
            if path[i][len(path[i])-1] != goal:
                unwanted.extend(path[i])
                path.remove(path[i])
 
        for i in range(len(unwanted)):
            for j in range(len(track_nodes)):
                if j == len(track_nodes):
                    break
                if track_nodes[j][0] == unwanted[i] or track_nodes[j][1] == unwanted[i]:
                    track_nodes.pop(j)
 
 
 
def find_the_next_path(Visited):
    lowest_path_plus_hero = Visited[0]
    i = 0
    while i < len(Visited):
        if Visited[i][3] + Visited[i][2] < lowest_path_plus_hero[3] + lowest_path_plus_hero[2]:
            lowest_path_plus_hero = Visited[i]
        i = i + 1
    
    Visited.remove(lowest_path_plus_hero)
 
    next_path = lowest_path_plus_hero

    return next_path
    
def extend_combo(next, Visited, total_cities, atlas, goal, track_nodes):
    prev_node = 0
    a = 0
    track2 = False
    for i in range(total_cities):
        next_node = atlas.get_road_dist(next, i)
       

        if a == 0:
 
 
            for i in range(len(track_nodes)):
 
                if track_nodes[i][1] == next:
                    prev_node = prev_node + atlas.get_road_dist(track_nodes[i][0], next)
 

 
                    
                    if track_nodes[i][1] > 0:
                        track2 = True
                if track2 == True:
                    for j in range(len(track_nodes)):

                        if track_nodes[i][0] == track_nodes[j][1]:
                            prev_node = prev_node + atlas.get_road_dist(track_nodes[j][0], track_nodes[j][1])

        a = a + 1
        if next_node != inf and next_node != 0 and i != track_nodes[0][0] and i != next:
            hero = atlas.get_crow_flies_dist(i, goal)
            Visited.append([next, i, next_node + prev_node, hero])

 
        if i == total_cities - 1:
            for i in range(len(Visited)):
                if i == len(Visited):
                    break
                if Visited[i][1] == next:
                    Visited.pop(i)
        
def total_path_cost(path, atlas):
    j = 1
    totalcost = 0
    for i in range(len(path)):
        totalcost = totalcost + atlas.get_road_dist(path[i], path[j])
        j = j + 1 
        if i == len(path) - 2:
            break
    return totalcost
 
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
 
 

