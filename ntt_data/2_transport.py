# 問題：https://www.msi.co.jp/solution/nuopt/docs/examples/html/02-02-00.html
#
# ある配送業者は二つの工場1，2から三つの店舗a，b，cへの製品の輸送を請け負っているとします．各工場，店舗について，それぞれ供給可能量と需要量が決められており，それらを満たしつつ，最もコストがかからない製品の運び方をどのように決定すればよいでしょうか．各工場の供給可能量，各店舗の需要量，単位量あたりの輸送コストは以下の通りです．

# 工場	供給可能量	店舗	需要量
# 1	250	a	200
# 2	450	b	200
#  	 	c	200
#
# 単位量あたりの輸送コスト
#  	a	b	c
# 1	3.4	2.2	2.9
# 2	3.4	2.4	2.5


import numpy as np
import pyomo.environ as pyo
from pyomo.opt import SolverFactory

# 供給可能量
s_data = np.array([250, 450])
# 需要量
d_data = np.array([200, 200, 200])
# 単位量あたりの輸送コスト
c_data = np.array([[3.4, 2.2, 2.9], [3.4, 2.4, 2.5]])

I = 2
J = 3

s = {i: s_data[i] for i in range(I)}
d = {j: d_data[j] for j in range(J)}
c = {(i, j): c_data[i, j] for i in range(I) for j in range(J)}

# モデルの定義
model = pyo.ConcreteModel()
model.I = pyo.Set(initialize=range(I))
model.J = pyo.Set(initialize=range(J))
model.x = pyo.Var(model.I, model.J, within=pyo.NonNegativeReals)


# 目的関数の定義
# min. \sum_{i, j} c_{ij} x_{ij}
def obj_rule(model):
    return sum(c[i, j] * model.x[i, j] for i in model.I for j in model.J)


model.obj = pyo.Objective(rule=obj_rule, sense=pyo.minimize)


# 制約条件の定義
# \forall i, \sum_j x_{ij} <= s_i
def supply_constraint_rule(model, i):
    return sum(model.x[i, j] for j in model.J) <= s[i]


# \forall j, \sum_i x_{ij} = d_j
def demand_constraint_rule(model, j):
    return sum(model.x[i, j] for i in model.I) == d[j]


model.supply_constraints = pyo.Constraint(model.I, rule=supply_constraint_rule)
model.demand_constraints = pyo.Constraint(model.J, rule=demand_constraint_rule)

# 最適化
opt = SolverFactory("glpk")
results = opt.solve(model)

# 結果の表示
print(model.display())
print("\n")
print("optimum value = ", pyo.value(model.obj))
print("x = ", [[pyo.value(model.x[i, j]) for j in model.J] for i in model.I])
