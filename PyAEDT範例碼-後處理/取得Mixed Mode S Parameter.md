取得Mixed Mode S Parameter
---

這段程式是在用 **PyAEDT 操作 HFSS 3D Layout**，定義 differential pair，並取出差分 S-parameter 來畫圖。核心流程如下：


## 1️⃣ 啟動 HFSS 3D Layout

```python
from ansys.aedt.core import Hfss3dLayout
hfss = Hfss3dLayout(version='2026.1')
```

* 建立一個 HFSS 3D Layout session（指定版本 2026.1）
* 會連接或開啟 AEDT



## 2️⃣ 定義 Differential Pair

```python
hfss.set_differential_pair('Port1', 'Port2', 'comm1', 'diff1')
hfss.set_differential_pair('Port3', 'Port4', 'comm2', 'diff2')
```

這裡做兩件事：

### 每一組 differential pair 包含：

* 正負端口：

  * `Port1`, `Port2`
  * `Port3`, `Port4`
* 自動建立：

  * **common mode**：`comm1`, `comm2`
  * **differential mode**：`diff1`, `diff2`

👉 等價於在 HFSS GUI 裡設定：

* Differential Pair excitation
* 自動產生 mixed-mode S-parameter



## 3️⃣ 取得差分 S-parameter

```python
data = hfss.post.get_solution_data(
    'dB(S(diff2,diff1))',
    context="Differential Pairs"
)
```

重點：

* `S(diff2, diff1)`
  → differential port 之間的 S-parameter
  → 類似 **Sdd21**

* `dB(...)`
  → 轉成 dB（log scale）

* `context="Differential Pairs"`
  → 指定用 mixed-mode（不是 single-ended）

👉 這一步是關鍵：
否則會拿到錯誤的 single-ended S-parameter



## 4️⃣ 取出資料

```python
x = data.primary_sweep_values
y = data.data_real()
```

* `x`：頻率（Hz）
* `y`：對應的 dB 值（實數）



## 5️⃣ 繪圖

```python
import matplotlib.pyplot as plt
plt.plot(x, y)
```

* 用 matplotlib 畫出：

  * x 軸：frequency
  * y 軸：Sdd21 (dB)



```python
from ansys.aedt.core import Hfss3dLayout

hfss = Hfss3dLayout(version='2026.1')

hfss.set_differential_pair('Port1', 'Port2', 'comm1', 'diff1')
hfss.set_differential_pair('Port3', 'Port4', 'comm2', 'diff2')

data = hfss.post.get_solution_data('dB(S(diff2,diff1))', context="Differential Pairs")

x = data.primary_sweep_values
y = data.data_real()

import matplotlib.pyplot as plt

plt.plot(x, y)
```

![](/assets/Figure%202026-04-20%20143257.png)