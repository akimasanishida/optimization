import numpy as np

# 駅データ（1-indexed）
stations = [
    "渋谷", "神泉", "駒場東大前", "池ノ上", "下北沢", "新代田", "東松原",
    "明大前", "永福町", "西永福", "浜田山", "高井戸", "富士見ヶ丘",
    "久我山", "三鷹台", "井の頭公園", "吉祥寺"
]

N = len(stations)  # 17
i_t = 9            # 永福町（1-indexed）

# 利用者数 u[i]（0-indexed）
u = np.array([286940, 10963, 35206, 9179, 107602, 8765, 15426,
              189779, 30039, 17596, 27565, 37789, 13091, 38168,
              19570, 6657, 127213], dtype=float)

# 隣接駅間距離 delta[k]：駅 k と k+1 の間（0-indexed, km）
delta = np.array([0.5, 0.9, 1.0, 0.6, 0.5, 0.5, 0.9, 1.1,
                  0.7, 0.8, 1.2, 0.7, 0.8, 1.0, 0.9, 0.6])

# 駅 i と j の距離 d[i, j]（0-indexed）
d = np.zeros((N, N))
for i in range(N):
    for j in range(i + 1, N):
        d[i, j] = np.sum(delta[i:j])
        d[j, i] = d[i, j]

# 距離減衰パラメータ
beta = 0.1

# exp(-beta * d)（対角成分は 0 = 自駅への移動なし）
E = np.exp(-beta * d)
np.fill_diagonal(E, 0.0)

# 反復法で A, B を計算
# A[i] = 1 / sum_{j != i} B[j] * u[j] * exp(-beta * d[i,j])
# B[j] = 1 / sum_{i != j} A[i] * u[i] * exp(-beta * d[i,j])
A = np.ones(N)
B = np.ones(N)

for iteration in range(10000):
    A_new = 0.5 / (E @ (B * u))
    B_new = 0.5 / (E.T @ (A_new * u))
    if np.allclose(A, A_new, rtol=1e-10) and np.allclose(B, B_new, rtol=1e-10):
        print(f"収束（{iteration + 1} 回）")
        break
    A, B = A_new, B_new

# n[i, j] = A[i] * B[j] * u[i] * u[j] * exp(-beta * d[i,j])（0-indexed）
n = np.outer(A * u, B * u) * E

# 収束の確認：各駅の乗車人数合計が u[i] に等しいか
row_sum = n.sum(axis=1)
col_sum = n.sum(axis=0)
print("乗車人数の誤差（最大）:", np.max(np.abs(row_sum - u / 2)))
print("降車人数の誤差（最大）:", np.max(np.abs(col_sum - u / 2)))

# n'[i, j] の計算（0-indexed, it = 永福町の 0-indexed インデックス）
# i < it, j == it: n'[i, it] = sum_{k >= it} n[i, k]
# i == it, j > it: n'[it, j] = sum_{k <= it} n[k, j]
# otherwise:       n'[i, j] = n[i, j]
it = i_t - 1  # 0-indexed の永福町（= 8）

n_prime_arr = n.copy()
for i in range(it):
    n_prime_arr[i, it] = np.sum(n[i, it:])
for j in range(it + 1, N):
    n_prime_arr[it, j] = np.sum(n[:it + 1, j])
n_prime_arr = np.round(n_prime_arr).astype(int)

# main.py で使う 1-indexed の dict に変換
n_prime = {}
for i in range(1, i_t):          # 小問題 1: i < j <= i_t
    for j in range(i + 1, i_t + 1):
        n_prime[i, j] = n_prime_arr[i - 1, j - 1]
for i in range(i_t, N):          # 小問題 2: i_t <= i < j
    for j in range(i + 1, N + 1):
        n_prime[i, j] = n_prime_arr[i - 1, j - 1]

# 結果を numpy ファイルに保存
import pathlib
out_dir = pathlib.Path(__file__).parent
np.save(out_dir / "n_prime.npy", n_prime_arr)
np.save(out_dir / "n.npy", n)
print(f"保存完了: {out_dir / 'n.npy'}, {out_dir / 'n_prime.npy'}")

# n_ij の表示
print(f"\n| {'i':>4} | {'j':>4} | {'駅i':>10} | {'駅j':>10} | {'n':>12} |")
print("| ---- | ---- | ---------- | ---------- | ------------: |")
for i in range(N):
    for j in range(i + 1, N):
        val = int(round(n[i, j]))
        if val >= 1000:
            print(f"| {i+1:>4} | {j+1:>4} | {stations[i]:>10} | {stations[j]:>10} | {val:>12} |")
