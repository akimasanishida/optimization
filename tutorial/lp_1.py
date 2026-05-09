# https://www.salesanalytics.co.jp/datascience/datascience117/

import pyomo.environ as pyo
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

model.x1 = pyo.Var(bounds=(-5, 5), domain=pyo.Integers)
model.x2 = pyo.Var(bounds=(0, 10), domain=pyo.Integers)


def obj_rule(model):
    return 75 * model.x1 + 125 * model.x2


model.obj = pyo.Objective(rule=obj_rule, sense=pyo.minimize)


def c1_rule(model):
    return 6 * model.x1 + 3 * model.x2 >= 38


def c2_rule(model):
    return 5 * model.x1 + 21 * model.x2 >= 29


model.eq1 = pyo.Constraint(rule=c1_rule)
model.eq2 = pyo.Constraint(rule=c2_rule)

opt = SolverFactory("glpk")

results = opt.solve(model)

print(model.display())
print("\n")
print("optimum value = ", pyo.value(model.obj))
print("x1 = ", pyo.value(model.x1))
print("x2 = ", pyo.value(model.x2))