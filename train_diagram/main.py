import pathlib
import numpy as np
import pyomo.environ as pyo

# 駅データ（1-indexed）
stations = [
    "渋谷", "神泉", "駒場東大前", "池ノ上", "下北沢", "新代田", "東松原",
    "明大前", "永福町", "西永福", "浜田山", "高井戸", "富士見ヶ丘",
    "久我山", "三鷹台", "井の頭公園", "吉祥寺"
]

N = len(stations)  # 17
i_t = 9            # 永福町（1-indexed）

# 駅間移動時間 r[k]：駅 k から k+1 への各駅停車移動時間（秒）
r = {
    1: 60, 2: 60, 3: 120, 4: 120, 5: 120,
    6: 60, 7: 120, 8: 120, 9: 120, 10: 60,
    11: 120, 12: 120, 13: 120, 14: 120, 15: 60, 16: 120,
}

# 駅 k 通過時の時間短縮量 s[k]（秒）
s = {
    1: 0, 2: 60, 3: 60, 4: 60, 5: 60,
    6: 60, 7: 60, 8: 60, 9: 60, 10: 45,
    11: 45, 12: 45, 13: 45, 14: 60, 15: 30, 16: 30,
}

# n'_ij：calc_n.py が生成した n_prime.npy を読み込む
_n_prime_arr = np.load(pathlib.Path(__file__).parent / "n_prime.npy")
n_prime = {}
for i in range(1, i_t):
    for j in range(i + 1, i_t + 1):
        n_prime[i, j] = int(_n_prime_arr[i - 1, j - 1])
for i in range(i_t, N):
    for j in range(i + 1, N + 1):
        n_prime[i, j] = int(_n_prime_arr[i - 1, j - 1])

# z_{kij} の有効なインデックス集合
# 小問題 1: i < j <= i_t，小問題 2: i_t <= i < j，k in {i,...,j-1}
kij_pairs = []
for i in range(1, i_t):
    for j in range(i + 1, i_t + 1):
        for k in range(i, j):
            kij_pairs.append((k, i, j))
for i in range(i_t, N):
    for j in range(i + 1, N + 1):
        for k in range(i, j):
            kij_pairs.append((k, i, j))

# モデル構築
model = pyo.ConcreteModel()

model.I = pyo.RangeSet(1, N)
model.KIJ = pyo.Set(initialize=kij_pairs, dimen=3)

model.x = pyo.Var(model.I, domain=pyo.Binary)
model.z = pyo.Var(model.KIJ, domain=pyo.Binary)

# 目的関数
def obj_rule(m):
    total = 0
    for i in range(1, i_t):
        for j in range(i + 1, i_t + 1):
            for k in range(i, j):
                total += n_prime[i, j] * (r[k] - s[k] * m.z[k, i, j])
    for i in range(i_t, N):
        for j in range(i + 1, N + 1):
            for k in range(i, j):
                total += n_prime[i, j] * (r[k] - s[k] * m.z[k, i, j])
    return total

model.obj = pyo.Objective(rule=obj_rule, sense=pyo.minimize)

# 固定駅の制約
model.fix_shibuya    = pyo.Constraint(expr=model.x[1]   == 1)
model.fix_eifukucho  = pyo.Constraint(expr=model.x[i_t] == 1)
model.fix_kichijoji  = pyo.Constraint(expr=model.x[N]   == 1)

# 議論にて追加してみる制約：永福町駅と吉祥寺駅の間に 1 つ以上の急行停車駅を設ける
# \sum_{i = i_t + 1}^{N - 1} x_i \ge 1
# model.min_express_stops = pyo.Constraint(expr=sum(model.x[i] for i in range(i_t + 1, N)) >= 1)

# 線形化制約: z_{kij} = (1 - x_k) x_i x_j
model.z_ub_k = pyo.ConstraintList()
model.z_ub_i = pyo.ConstraintList()
model.z_ub_j = pyo.ConstraintList()
model.z_lb   = pyo.ConstraintList()

for (k, i, j) in kij_pairs:
    model.z_ub_k.add(model.z[k, i, j] <= 1 - model.x[k])
    model.z_ub_i.add(model.z[k, i, j] <= model.x[i])
    model.z_ub_j.add(model.z[k, i, j] <= model.x[j])
    model.z_lb.add(  model.z[k, i, j] >= 1 - model.x[k] + model.x[i] + model.x[j] - 2)

# 求解
solver = pyo.SolverFactory('glpk')
result = solver.solve(model, tee=True)

# 結果表示
print("\n=== 結果 ===")
print(f"ステータス       : {result.solver.status}")
print(f"終了条件         : {result.solver.termination_condition}")
print(f"目的関数値       : {pyo.value(model.obj):.4f}")
print("\n急行停車駅:")
for i in model.I:
    mark = "●" if pyo.value(model.x[i]) > 0.5 else "○"
    print(f"  {mark} {stations[i - 1]}")
