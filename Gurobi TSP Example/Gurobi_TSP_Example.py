# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 21:43:19 2020

@author: jfb2444
"""

######################### Imports #########################
import json
import math
from itertools import combinations,product
import folium		# for mapping the solution tour
import gurobipy as gp
from gurobipy import GRB


######################### Data #########################
# Read capital names and coordinates from json file
capitals_json = json.load(open('capitals.json'))
capitals = []
coordinates = {}
for state in capitals_json:
    if state not in ['AK', 'HI']:           # Exclude Alaska and Hawaii from the tour
      capital = capitals_json[state]['capital']
      capitals.append(capital)
      coordinates[capital] = (float(capitals_json[state]['lat']), float(capitals_json[state]['long']))

# Compute pairwise distance matrix
def distance(city1, city2):
    c1 = coordinates[city1]
    c2 = coordinates[city2]
    diff = (c1[0]-c2[0], c1[1]-c2[1])
    return math.sqrt(diff[0]*diff[0]+diff[1]*diff[1])

dist = {(c1, c2): distance(c1, c2) for c1, c2 in product(capitals, capitals) if c1 != c2}

######################### Functions #########################
# Callback - use lazy constraints to eliminate sub-tours
def subtourelim(model, where):
    if where == GRB.Callback.MIPSOL:
        # make a list of edges selected in the solution
        vals = model.cbGetSolution(model._vars)
        selected = gp.tuplelist((i, j) for i, j in model._vars.keys()
                             if vals[i, j] > 0.5)
        # find the shortest cycle in the selected edge list
        tour = subtour(selected)
        if len(tour) < len(capitals):
            # add subtour elimination constr. for every pair of cities in subtour
            model.cbLazy(gp.quicksum(model._vars[i, j] for i, j in combinations(tour, 2))
                         <= len(tour)-1)


# Given a tuplelist of edges, find the shortest subtour
def subtour(edges):
    unvisited = capitals[:]
    cycle = capitals[:] # Dummy - guaranteed to be replaced
    while unvisited:  # true if list is non-empty
        thiscycle = []
        neighbors = unvisited
        while neighbors:
            current = neighbors[0]
            thiscycle.append(current)
            unvisited.remove(current)
            neighbors = [j for i, j in edges.select(current, '*')
                         if j in unvisited]
        if len(thiscycle) <= len(cycle):
            cycle = thiscycle # New shortest subtour
    return cycle


######################### Optimization Model #########################
# Create model
m = gp.Model()

# Variables: is city 'i' adjacent to city 'j' on the tour?
vars = m.addVars(dist.keys(), obj=dist, vtype=GRB.BINARY, name='e')
for i, j in vars.keys():
    m.addConstr(vars[j, i] == vars[i, j])  # edge in opposite direction

# Constraints: two edges incident to each city
m.addConstrs(vars.sum(c, '*') == 2 for c in capitals)

# Optimize the model
m._vars = vars
m.Params.lazyConstraints = 1
m.optimize(subtourelim)

######################### Post-Processing #########################
# Retrieve solution
vals = m.getAttr('x', vars)
selected = gp.tuplelist((i, j) for i, j in vals.keys() if vals[i, j] > 0.5)
tour = subtour(selected)
assert len(tour) == len(capitals)

# Map the solution
map = folium.Map(location=[40,-95], zoom_start = 4)
points = []
for city in tour:
  points.append(coordinates[city])
points.append(points[0])

folium.PolyLine(points).add_to(map)
map
