# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 21:43:19 2020

@author: jfb2444
"""

######################### Imports #########################
import json
import math
from datetime import datetime
import gurobipy as gp
from gurobipy import GRB

# Pseudoclear console
for i in range(25):
    print("")
dateTimeObj = datetime.now()
print("New run @", dateTimeObj)

######################### Functions #########################
# Function to merge words and return the overlap length
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
#words = ['orca', 'arc', 'car']
#words = ['area', 'code', 'dear', 'deco', 'odec', 'rear']
words = ['SGALWDV', 'GALWDVP', 'ALWDVPS', 'LWDVPSP', 'WDVPSPV']
nbWords = len(words)
nodes =  ['S']
nodes.extend(words)
nbNodes = len(nodes)

arcs = []
cost = {}
for w1 in words:
    for w2 in words:
        if w1 != w2:
            tmpMergedWord, tmpOverlapLength = mergeWords(w1,w2)
            if(tmpOverlapLength>0):
                tmpCost = len(w2) - tmpOverlapLength
                tmpArc = (w1,w2)
                arcs.append(tmpArc)
                tmpDict = {tmpArc: tmpCost}
                cost.update(tmpDict)
                print('\"',w1, '\" + \"', w2, '\" = \"', tmpMergedWord, '\" with cost', tmpCost)
            else:
                print('\"',w1, '\" + \"', w2, '\" cannot be merged in that order' )    
    # Add arc from dummy source to each word node
    tmpArc = ('S',w1)
    arcs.append(tmpArc)
    tmpCost = len(w1)
    tmpDict = {tmpArc: tmpCost}
    cost.update(tmpDict)
    # Add arc from each word node to the dummy source
    tmpArc = (w1,'S')
    arcs.append(tmpArc)
    tmpCost = 0
    tmpDict = {tmpArc: tmpCost}
    cost.update(tmpDict)
    
        
######################### Optimization Model #########################
# Create model
print("\nBuilding Wordchain TSP Model:\n")
model = gp.Model("WordChain_TSP")

# Variables: can we go from word i to word j?
#vars = model.addVars(arcs, obj=cost, vtype=GRB.BINARY, name='arc')
vars_arc = model.addVars(arcs, obj=cost, vtype=GRB.BINARY, name='var_arc' )
vars_seq = model.addVars(nodes, obj=0, vtype=GRB.INTEGER, name='var_seq')

# Constraints: 
# Visit each node and leave each node
model.addConstrs(vars_arc.sum('*', i) == 1 for i in nodes)
model.addConstrs(vars_arc.sum(i, '*') == 1 for i in nodes)
#Miller-Tucker-Zemlin Subtour Elimination
model.addConstrs(vars_seq[arc[0]] - vars_seq[arc[1]] + nbNodes*vars_arc[arc] <= nbNodes-1 for arc in arcs if arc[0]!='S' and arc[1]!='S' and arc[0]!=arc[1])


# Optimize the model
model.write('WordChain_TSP.lp')
model.optimize()

######################### Post-Processing #########################
# Retrieve solution
status=model.status
if status != GRB.INF_OR_UNBD and status != GRB.INFEASIBLE:
    print('\nSolution:')
    curr = 'S'
    count = 0
    shortestMergedWord = ''
    while(count < nbWords):
        for arc in arcs:
            if( arc[0] == curr and vars_arc[arc].x > 0):
                if( arc[0] == 'S'): 
                    shortestMergedWord = arc[1]
                elif(arc[0] != 'S' and arc[1] != 'S'):
                        shortestMergedWord, tmpOverlapLength = mergeWords(shortestMergedWord,arc[1])
                curr = arc[1]
                count = count + 1
                print(count, ':', shortestMergedWord)
                break
    print('The shortest merged word is \"', shortestMergedWord, '\"')       
else: 
    print('\nNo solution found!')
