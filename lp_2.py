import pyomo.environ as pyo
from pyomo.opt import SolverFactory

model = pyo.ConcreteModel()

model.width = pyo.Var(domain=pyo.NonNegativeReals)
model.height = pyo.Var(domain=pyo.NonNegativeReals)


def obj_rule(model):
    return model.width * model.height


model.obj = pyo.Objective(rule=obj_rule, sense=pyo.maximize)


def c1_rule(model):
    return 2 * model.width + 2 * model.height == 20


model.eq1 = pyo.Constraint(rule=c1_rule)

opt = SolverFactory("ipopt")

results = opt.solve(model)
print(model.display())
print("\n")
print("optimum value = ", pyo.value(model.obj))
print("width = ", pyo.value(model.width))
print("height = ", pyo.value(model.height))
