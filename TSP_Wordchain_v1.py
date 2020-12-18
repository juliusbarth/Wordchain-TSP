# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 21:43:19 2020

@author: jfb2444
"""

######################### Imports #########################
import json
import math
from datetime import datetime
from itertools import combinations,product
import folium		# for mapping the solution tour
import gurobipy as gp
from gurobipy import GRB

# Pseudoclear console
for i in range(25):
    print("")
dateTimeObj = datetime.now()
print("New run @", dateTimeObj)

######################### Functions #########################
# Function to merge words and return the overlap length (https://stackoverflow.com/questions/47333771/how-can-i-merge-overlapping-strings-in-python)
def mergeWords(w1, w2):
    overlapLength = 0
    mergedWord = []
    for i in range(min(len(w1),len(w2))):
        if(w1.endswith(w2[:i+1])):
            overlapLength = i+1
            mergedWord = w1+w2[i+1:]          
    return mergedWord, overlapLength

######################### Data #########################
print("\nDefining Data:")    
words = ['orca', 'arc', 'car']
nbWords = len(words)
nodes =  ['S']
nodes.extend(words)

for w1 in words:
    for w2 in words:
        if w1 != w2:
            tmpMergedWord, tmpOverlapLength = mergeWords(w1,w2)
            if(tmpOverlapLength>0):
                tmpCost = len(w2) - tmpOverlapLength
                print('\"',w1, '\" + \"', w2, '\" = \"', tmpMergedWord, '\" with cost_GB', tmpCost)
            else:
                print('\"',w1, '\" + \"', w2, '\" cannot be merged in that order' )    


# TODO: Make cost_GB definition generic based on mergeWords method
arcs_GB, cost_GB = gp.multidict({
    ('S', 'orca'): 4,
    ('S', 'arc'): 3,
    ('S', 'car'): 3,
    ('arc', 'car'): 2,
    ('car', 'arc'): 1,
    ('orca', 'car'): 1,
    ('orca', 'arc'): 2,
    ('arc', 'S'): 0,
    ('car', 'S'): 0,
    ('orca', 'S'): 0
})
    
        
######################### Optimization Model #########################
# Create model
print("\nBuilding Wordchain TSP Model:\n")
model = gp.Model("WordChain_TSP")

# Variables: can we go from word i to word j?
vars = model.addVars(arcs_GB, obj=cost_GB, vtype=GRB.BINARY, name='arc')

# Constraints: 
# Visit each node and leave each node
model.addConstrs(vars.sum(i, '*') == 1 for i in nodes)
model.addConstrs(vars.sum('*', i) == 1 for i in nodes)

# Optimize the model
model._vars = vars
model.optimize()

######################### Post-Processing #########################
# Retrieve solution
print('\nSolution:')
vals = model.getAttr('x', vars)
curr = 'S'
count = 0
shortestMergedWord = ''
while(count < nbWords):
    for arc in arcs_GB:
        if( arc[0] == curr and vals[arc] > 0):
            if( arc[0] == 'S'): 
                shortestMergedWord = arc[1]
            elif(arc[0] != 'S' and arc[1] != 'S'):
                    shortestMergedWord, tmpOverlapLength = mergeWords(shortestMergedWord,arc[1])
            curr = arc[1]
            count = count + 1
            print(count, ':', shortestMergedWord)
            break

print('The shortest merged word is \"', shortestMergedWord, '\"')       
        
