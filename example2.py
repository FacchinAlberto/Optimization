import gurobipy as gp
from gurobipy import GRB
import numpy as np

months = ['1', '2', '3']
nodes = ['X', 'Y', 'Z', 'W', 'K']

# (stabilimento, negozio): capacità produttiva mensile in ore
arcs, capacity = gp.multidict({('A', 'X'): 420/1.5,
                                 ('A', 'Y'): 420/1.5,
                                 ('A', 'Z'): 420/1.5,
                                 ('A', 'W'): 420/1.5,
                                 ('A', 'K'): 420/1.5,
                                 ('B', 'X'): 330/2,
                                 ('B', 'Y'): 330/2,
                                 ('B', 'Z'): 330/2,
                                 ('B', 'W'): 330/2,
                                 ('B', 'K'): 330/2})
print(f'Arcs: {arcs}\n Capacities: {capacity}')

profitto = {
    ('1', 'A', 'X'): 55,
    ('1', 'A', 'Y'): 55.3,
    ('1', 'A', 'Z'): 56.2,
    ('1', 'A', 'W'): 57,
    ('1', 'A', 'K'): 56.1,
    ('2', 'A', 'X'): 55,
    ('2', 'A', 'Y'): 55.3,
    ('2', 'A', 'Z'): 56.2,
    ('2', 'A', 'W'): 57,
    ('2', 'A', 'K'): 56.1,
    ('3', 'A', 'X'): 55,
    ('3', 'A', 'Y'): 55.3,
    ('3', 'A', 'Z'): 56.2,
    ('3', 'A', 'W'): 57,
    ('3', 'A', 'K'): 56.1,
    ('1', 'B', 'X'): 60.4,
    ('1', 'B', 'Y'): 60.5,
    ('1', 'B', 'Z'): 62.6,
    ('1', 'B', 'W'): 62.5,
    ('1', 'B', 'K'): 62,
    ('2', 'B', 'X'): 60.4,
    ('2', 'B', 'Y'): 60.5,
    ('2', 'B', 'Z'): 62.6,
    ('2', 'B', 'W'): 62.5,
    ('2', 'B', 'K'): 62,
    ('3', 'B', 'X'): 60.4,
    ('3', 'B', 'Y'): 60.5,
    ('3', 'B', 'Z'): 62.6,
    ('3', 'B', 'W'): 62.5,
    ('3', 'B', 'K'): 62}

# domanda
inflow = {
    ('1', 'X'): 150,
    ('1', 'Y'): 90,
    ('1', 'Z'): 50,
    ('1', 'W'): 32,
    ('1', 'K'): 100,
    ('2', 'X'): 30,
    ('2', 'Y'): 50,
    ('2', 'Z'): 180,
    ('2', 'W'): 120,
    ('2', 'K'): 0,
    ('3', 'X'): 0,
    ('3', 'Y'): 100,
    ('3', 'Z'): 75,
    ('3', 'W'): 0,
    ('3', 'K'): 200}

m = gp.Model('netflow')
flow = m.addVars(months, arcs, obj = profitto, name = 'flow')
m.update()
print(f"Model variables: {m.getVars()}")

m.addConstrs((flow.sum('*', i, j) <= capacity[i, j] for i, j in arcs), "cap")

m.addConstrs((flow.sum(h, '*', j) == inflow[h, j] for h in months for j in nodes), "node")

m.optimize()

# Print solution
if m.Status == GRB.OPTIMAL:
    solution = m.getAttr('X', flow)
    for h in months:
        print('\nOptimal flows for %s:' % h)
        for i, j in arcs:
            if solution[h, i, j] > 0:
                print('%s -> %s: %g' % (i, j, solution[h, i, j]))
