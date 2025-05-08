讀取Touchstone轉Z參數作圖
---

這段程式碼的主要目的是讀取一個 Touchstone 格式的 S 參數檔案（如 s7p 檔案），並將前三個 Port 的自阻抗（Zii）在不同頻率下的大小以對數座標圖形式呈現出來。這有助於工程師分析電路在不同頻率下的阻抗特性，特別是在電源完整性（PDN）設計上。

### 流程架構

1. **匯入必要的套件**：包含 `ansys.aedt` 的 Touchstone 解析工具、matplotlib 繪圖工具，以及 numpy 數值運算工具。
2. **讀取 Touchstone 檔案**：透過 `read_touchstone()` 函數載入位於指定路徑的 `.s7p` 檔案，並解析其頻率與阻抗矩陣資料。
3. **設定圖表**：建立圖形畫布並設置格線、標籤、對數刻度（x 軸與 y 軸）。
4. **繪製 Zii 曲線**：從阻抗矩陣中取出前三個 Port 的自阻抗（即對角線上的值），繪製對應頻率下的阻抗大小曲線。
5. **顯示圖表**：加入圖例並顯示圖形。

### 補充說明

* **Touchstone 檔案（如 .s7p）**：這是一種常見的射頻電路 S 參數檔案格式，其中數字代表 Port 數量，例如 s7p 表示有 7 個 Port。
* **自阻抗 Zii**：在阻抗矩陣中，Zii 表示第 i 個 Port 的輸入阻抗，自阻抗是觀察電源完整性時很重要的參數。
* **data.z\_mag\[:, i, i]**：這裡使用的是 NumPy 陣列切片語法，表示取出所有頻率下，第 i 個 Port 的自阻抗大小值。
* **對數座標軸**：x 軸與 y 軸皆使用對數刻度，這是觀察寬頻頻率響應圖常用的方式，有助於呈現高低頻變化。
* **`f'Z({i+1}, {i+1})'` 的用意**：雖然 Python 的陣列索引是從 0 開始，但在工程領域我們慣用從 1 開始編號的 Port 標示方式。因此這裡將程式中實際的索引值 `i` 加上 1，產生像是 `Z(1,1)`、`Z(2,2)` 的標籤，讓圖表更符合人類閱讀習慣與實務應用的編號方式。

這段程式對於進行 PDN 或高頻電路設計分析時，非常實用，可以快速幫助設計者找出阻抗過高或過低的頻段。


```python
from ansys.aedt.core.visualization.advanced.touchstone_parser import read_touchstone
import matplotlib.pyplot as plt
import numpy as np

data = read_touchstone(r"D:\demo\pdn.s7p")

plt.figure()
plt.grid()
plt.xlabel('Frequency (Hz)')
plt.ylabel('Zii (Ohm)')
plt.xscale("log")
plt.yscale("log")

for i in range(3):
    zself = data.z_mag[:, i, i]
    plt.plot(data.f, np.abs(zself), label=f'Z({i+1}, {i+1})')

plt.legend()
plt.show()
```
![2025-05-08_11-38-46](/assets/2025-05-08_11-38-46_5mgvty3rw.png)