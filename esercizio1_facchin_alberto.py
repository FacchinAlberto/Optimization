import gurobipy as gp
from gurobipy import GRB
import numpy as np

model = gp.Model()

n_vars = 4
x = model.addMVar(n_vars, lb = [0] * n_vars, ub = GRB.INFINITY)
model.update()

A =  np.array([[24, 27, 23, 0], 
               [1, 0, 0, 0],
               [0, 1, 0, 0],
               [0, 0, 1, 0],
               [20, 30, 25, 0],
               [10, 15, 10, 0],
               [8, 12, 15, 0],
               [0, 0, 0, 1]])
               
b = np.array([800, 4, 5, 6, 1200, 1080, 1320, 275])

if len(A) != len(b):
  print("Il numero di termini noti non corrisponde al numero di vincoli")

ct1 = model.addConstr(A[0]@x <= b[0])
ct2 = model.addConstr(A[1]@x >= b[1])
ct3 = model.addConstr(A[2]@x >= b[2])
ct4 = model.addConstr(A[3]@x >= b[3])
ct5 = model.addConstr(A[4]@x <= b[4])
ct6 = model.addConstr(A[5]@x <= b[5])
ct7 = model.addConstr(A[6]@x <= b[6])
ct8 = model.addConstr(A[7]@x == b[7])

model.update()

obj_coefs = np.array([2500, 5000, 3000, -1])
model.setObjective(obj_coefs @ x, GRB.MAXIMIZE) # MAXIMIZE OR MINIMIZE

model.optimize()

# stampa dello status del problema
status_dict = {GRB.OPTIMAL: "OPTIMAL", GRB.INFEASIBLE: "INFEASIBLE", GRB.UNBOUNDED: "UNBOUNDED", GRB.INF_OR_UNBD: "INFEASIBLE OR UNBOUNDED"}
status = model.getAttr('Status')
print(f"Model is {status_dict[status]}")

# stampa della soluzione ottima
for v in model.getVars():
  print('%s %g' % (v.VarName, v.X))

# stampa del valore ottimo
print('Obj: %g' % model.ObjVal)