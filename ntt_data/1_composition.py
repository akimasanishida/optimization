# 問題：https://www.msi.co.jp/solution/nuopt/docs/examples/html/02-01-00.html
#
# 鉛，亜鉛，スズの構成比率が，それぞれ30%，30%，40%となるような合金を，市販の合金を混ぜ合わせ，できるだけ安いコストで生成することを考えます．現在手に入れることができる市販の合金は9種類で，それらの構成比率と単位量あたりのコストは以下の通りです．
# 市販の合金	1	2	3	4	5	6	7	8	9
# 鉛（%）	20	50	30	30	30	60	40	10	10
# 亜鉛（%）	30	40	20	40	30	30	50	30	10
# スズ（%）	50	10	50	30	40	10	10	60	80
# コスト（$/lb）	7.3	6.9	7.3	7.5	7.6	6.0	5.8	4.3	4.1
# 　所望の組成を持つ合金をコストを一番安く生成するには，市販の合金をどのように混ぜ合わせれば良いでしょうか．

import numpy as np
import pyomo.environ as pyo
from pyomo.opt import SolverFactory

a_data = np.array(
    [
        [0.2, 0.3, 0.5],
        [0.5, 0.4, 0.1],
        [0.3, 0.2, 0.5],
        [0.3, 0.4, 0.3],
        [0.3, 0.3, 0.4],
        [0.6, 0.3, 0.1],
        [0.4, 0.5, 0.1],
        [0.1, 0.3, 0.6],
        [0.1, 0.1, 0.8],
    ]
)
c_data = np.array([7.3, 6.9, 7.3, 7.5, 7.6, 6.0, 5.8, 4.3, 4.1])
r_data = np.array([0.3, 0.3, 0.4])

# dictに変換
I = 9
J = 3
a = {(i, j): a_data[i, j] for i in range(I) for j in range(J)}
c = {i: c_data[i] for i in range(I)}
r = {j: r_data[j] for j in range(J)}

# モデルの定義
model = pyo.ConcreteModel()
model.I = pyo.Set(initialize=range(I))
model.J = pyo.Set(initialize=range(J))
model.x = pyo.Var(model.I, within=pyo.NonNegativeReals)


# 目的関数の定義
# min. f(x) = \sum_i c_i x_i
def obj_rule(model):
    return sum(c[i] * model.x[i] for i in model.I)


model.obj = pyo.Objective(rule=obj_rule, sense=pyo.minimize)


# 制約条件の定義
# \sum_i x_i = 1
# \forall i, \sum_i a_{ij} x_i = r_j
def constraint_rule1(model):
    return sum(model.x[i] for i in model.I) == 1


def constraint_rule2(model, j):
    return sum(a[i, j] * model.x[i] for i in model.I) == r[j]


model.constraint1 = pyo.Constraint(rule=constraint_rule1)
model.constraint2 = pyo.Constraint(model.J, rule=constraint_rule2)

# 最適化
opt = SolverFactory("glpk")
results = opt.solve(model)

# 結果の表示
print(model.display())
print("\n")
print("optimum value = ", pyo.value(model.obj))
print("x = ", [pyo.value(model.x[i]) for i in model.I])
