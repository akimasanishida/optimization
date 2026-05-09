# https://www.salesanalytics.co.jp/datascience/datascience137/

import numpy as np
import pyomo.environ as pyo
from pyomo.opt import SolverFactory

# min. f(x) = (75, 125) * (x1, x2)^\top
# s.t. [[6, 3], [5, 21]] * (x1, x2)^\top >= (38, 29)^\top

I = 2

a_data = np.array([75, 125])
t_data = np.array([[6, 3], [5, 21]])
t0_data = np.array([38, 29])

# dictに変換
a = {i: a_data[i] for i in range(I)}
t = {(i, j): t_data[i, j] for i in range(I) for j in range(I)}
t0 = {i: t0_data[i] for i in range(I)}

# モデルの定義
model = pyo.ConcreteModel()
model.I = pyo.Set(initialize=range(I))
model.x = pyo.Var(model.I, within=pyo.Reals)

# 目的関数の定義
def obj_rule(model):
    return sum(a[i] * model.x[i] for i in model.I)
model.obj = pyo.Objective(rule=obj_rule, sense=pyo.minimize)

# 制約条件の定義
def constraint_rule(model, i):
    return sum(t[i, j] * model.x[j] for j in model.I) >= t0[i]
model.constraints = pyo.Constraint(model.I, rule=constraint_rule)

# 最適化
opt = SolverFactory("glpk")
results = opt.solve(model)

# 結果の表示
print(model.display())
print("\n")
print("optimum value = ", pyo.value(model.obj))
print("x = ", [pyo.value(model.x[i]) for i in model.I])
