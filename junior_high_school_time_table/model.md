# 中学校時間割最適化問題の定式化

## 集合

- $D = \{\text{月}, \text{火}, \text{水}, \text{木}, \text{金}\}$：曜日の集合
- $P = \{1, 2, 3, 4, 5, 6\}$：時限の集合
- $C$：クラスの集合（$|C| = 12$，各学年4クラス）
- $T$：教師の集合（$|T| \geq 24$）
- $T_{\mathrm{new}} \subset T$：新任教師の集合
- $S = \{\text{国語}, \text{社会}, \text{数学}, \text{理科}, \text{英語}, \text{音楽}, \text{美術}, \text{家庭}, \text{体育}, \text{道徳}\}$：科目の集合
- $S_{\mathrm{cont}} = \{\text{音楽}, \text{美術}, \text{家庭}\}$：連続時限で行われる科目の集合
- $G = \{1, 2, 3\}$：学年の集合

### 補助的な集合

同一曜日内の連続2時限のペア（昼休みをまたぐ4限–5限を除外）：

$$
\begin{equation}
Q_2 = \{(p, p+1) \mid p \in \{1, 2, 3, 5\}\}
\end{equation}
$$

同一曜日内の連続4時限の組（昼休みをまたぐものも含む）：

$$
\begin{equation}
Q_4 = \{(p, p+1, p+2, p+3) \mid p \in \{1, 2, 3\}\}
\end{equation}
$$

## パラメータ

- $r_{g,s} \in \mathbb{Z}_{\geq 0}$：学年 $g$ における科目 $s$ の週あたり時限数（$\sum_{s \in S} r_{g,s} = 30,\ \forall g \in G$）
- $g(c) \in G$：クラス $c$ の所属学年
- $\sigma(t) \in S$：教師 $t$ の担当科目
- $h_1(c) \in T$：クラス $c$ の担任
- $h_2(c) \in T$：クラス $c$ の副担任

## 仮定

1. 各教師の担当科目は1つのみ．
2. 各クラスの担任と副担任は異なる科目を担当する：$\sigma(h_1(c)) \neq \sigma(h_2(c)),\ \forall c \in C$．

## 決定変数

- $x_{s,d,p,c} \in \{0, 1\}$：科目 $s$ がクラス $c$ にて曜日 $d$ の $p$ 限に行われるとき1
- $y_{t,c} \in \{0, 1\}$：教師 $t$ がクラス $c$ の授業を担当するとき1
- $z_{t,d,p,c} \in \{0, 1\}$：教師 $t$ が曜日 $d$ の $p$ 限にクラス $c$ で授業を行うとき1
- $\tilde{y}_{t,g} \in \{0, 1\}$：教師 $t$ が学年 $g$ の授業を担当するとき1
- $w_{s,d,p,c} \in \{0, 1\}$：クラス $c$ の科目 $s \in S_{\mathrm{cont}}$ が曜日 $d$ の $(p, p\!+\!1)$ 限に配置されるとき1

## 制約

### 授業の基本制約

**(1)** 各時限・各クラスで行われる授業は高々1科目：

$$
\begin{equation}
\sum_{s \in S} x_{s,d,p,c} \leq 1, \quad \forall d \in D,\ p \in P,\ c \in C
\end{equation}
$$

**(2)** 各クラス・各科目に対して担当教師をちょうど1人割り当てる：

$$
\begin{align}
\sum_{\substack{t \in T \\ \sigma(t) = s}} y_{t,c} &= 1, \quad \forall c \in C,\ \forall s \in S \, r_{g(c),\,s} > 0 \\
\sum_{\substack{t \in T \\ \sigma(t) = s}} y_{t,c} &= 0, \quad \forall c \in C,\ \forall s \in S \, r_{g(c),\,s} = 0
\end{align}
$$

**(3)** 各クラス・各科目について必要時限数を充足する：

$$
\begin{equation}
\sum_{d \in D} \sum_{p \in P} x_{s,d,p,c} = r_{g(c),\,s}, \quad \forall s \in S,\ c \in C
\end{equation}
$$

### 担任・副担任

**(4)** 担任は自クラスの授業を担当する：

$$
\begin{equation}
y_{h_1(c),\,c} = 1, \quad \forall c \in C, \, r_{g(c),\,\sigma(h_1(c))} > 0
\end{equation}
$$

**(5)** 副担任は自クラスの授業を担当する：

$$
\begin{equation}
y_{h_2(c),\,c} = 1, \quad \forall c \in C, \, r_{g(c),\,\sigma(h_2(c))} > 0
\end{equation}
$$

### 1日あたりの授業配置

**(6)** 連続時限で行われない科目を除き，各科目は1日1時限以下：

$$
\begin{equation}
\sum_{p \in P} x_{s,d,p,c} \leq 1, \quad \forall s \in S \setminus S_{\mathrm{cont}},\ d \in D,\ c \in C
\end{equation}
$$

### 連続時限制約

$r_{g(c),\,s} = 2,\ \forall c \in C,\ \forall s \in S_{\mathrm{cont}}$ を仮定する．

**(7a)** 各クラスについて連続2時限の枠をちょうど1つ選択：

$$
\begin{equation}
\sum_{d \in D} \sum_{(p,\,p+1) \in Q_2} w_{s,d,p,c} = 1, \quad \forall c \in C,\ \forall s \in S_{\mathrm{cont}}
\end{equation}
$$

**(7b)** 選択された枠の両時限に連続科目を配置：

$$
\begin{equation}
\begin{aligned}
x_{s,\,d,\,p,\,c} &\geq w_{s,d,p,c}, \\
x_{s,\,d,\,p+1,\,c} &\geq w_{s,d,p,c},
\end{aligned}
\quad \forall d \in D,\ (p, p\!+\!1) \in Q_2,\ c \in C
\end{equation}
$$

### 教師と授業の紐付け（$z$ の線形化）

$z_{t,d,p,c}$ は $x_{\sigma(t),d,p,c} \cdot y_{t,c}$ の線形化である．

**(8a)** 下界：

$$
\begin{equation}
z_{t,d,p,c} \geq x_{\sigma(t),\,d,\,p,\,c} + y_{t,c} - 1, \quad \forall t \in T,\ d \in D,\ p \in P,\ c \in C
\end{equation}
$$

**(8b)** 上界：

$$
\begin{align}
z_{t,d,p,c} &\leq x_{\sigma(t),\,d,\,p,\,c}, \quad \forall t \in T,\ d \in D,\ p \in P,\ c \in C \\
z_{t,d,p,c} &\leq y_{t,c}, \quad \forall t \in T,\ d \in D,\ p \in P,\ c \in C
\end{align}
$$

### 教師のスケジュール制約

**(9)** 各時限で教師は高々1クラスを担当：

$$
\begin{equation}
\sum_{c \in C} z_{t,d,p,c} \leq 1, \quad \forall t \in T,\ d \in D,\ p \in P
\end{equation}
$$

**(10)** 教師は毎日少なくとも1時限授業を行う：

$$
\begin{equation}
\sum_{c \in C} \sum_{p \in P} z_{t,d,p,c} \geq 1, \quad \forall t \in T,\ d \in D
\end{equation}
$$

**(11)** 4時限連続授業の禁止：

$$
\begin{equation}
\sum_{p' \in q}\ \sum_{c \in C} z_{t,d,p',c} \leq 3, \quad \forall t \in T,\ d \in D,\ q \in Q_4
\end{equation}
$$

### 学年集約と新任教師の制約

**(12)** 教師の学年担当フラグ：

$$
\begin{equation}
\tilde{y}_{t,g} \geq y_{t,c}, \quad \forall t \in T,\ \forall c \in C : g(c) = g
\end{equation}
$$

**(13)** 新任教師は1学年のみ担当：

$$
\begin{equation}
\sum_{g \in G} \tilde{y}_{t,g} = 1, \quad \forall t \in T_{\mathrm{new}}
\end{equation}
$$

## 目的関数

$$
\begin{equation}
\sum_{t \in T} \sum_{g \in G} \tilde{y}_{t,g}
\end{equation}
$$
