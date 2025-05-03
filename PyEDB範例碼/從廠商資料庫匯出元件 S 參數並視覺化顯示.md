從廠商資料庫匯出元件 S 參數並視覺化顯示
---

這段程式碼的目的是從 Ansys 提供的 EDB（Electronic Database）中，讀取特定品牌與型號的電容（這裡是 Murata 的 GRM15 系列），取得其 S 參數（Scattering Parameters），並將其匯出為 Touchstone 檔案（`.s2p`），同時繪製出 S11 和 S21 的頻率響應圖，以便進行元件性能分析。


### 流程架構

1. **初始化與載入資料庫**：透過 `Edb()` 初始化電子元件資料庫。
2. **取得元件庫資料**：從 `components.get_vendor_libraries()` 取得支援的電容廠牌與型號。
3. **選取特定電容資料**：挑出 Murata 品牌下 GRM15 系列的每個元件。
4. **處理每個電容模型**：

   * 讀取 S 參數資料。
   * 匯出為 `.s2p` 檔案至指定路徑（`d:/demo/`）。
   * 繪製並顯示 S11（輸入反射）與 S21（前向傳輸）的 dB 曲線圖。



### 補充說明

* **S 參數（Scattering Parameters）**：是高頻電路中用來描述輸入輸出關係的重要參數，S11 表示反射係數，S21 表示傳輸係數。
* **Touchstone 檔案（.s2p）**：是一種常用格式來儲存二埠元件的 S 參數，可供電路模擬工具使用。
* **`plot_s_db(m, n)` 函式**：這個函式用來畫出第 `m` 輸入埠到第 `n` 輸出埠之間的 S 參數的 magnitude（以 dB 表示）。
* **`dir(comp_lib.capacitors)`**：這一行只是用來觀察 capacitor 的結構，實際上沒有影響主程式流程。

```python
import os
import matplotlib.pyplot as plt
from ansys.aedt.core import Hfss, Hfss3dLayout, Edb

# 初始化 EDB 物件
edb = Edb()

# 取得元件庫中的廠商元件資料
comp_lib = edb.components.get_vendor_libraries()

# 針對 Murata 品牌下的 GRM15 系列電容元件進行處理
for name, model in comp_lib.capacitors["Murata"]['GRM15'].items():
    # 取得該元件的 S 參數資料
    network = model.s_parameters

    # 將 S 參數以 Touchstone 格式輸出至指定資料夾
    network.write_touchstone(os.path.join(f"d:/demo/{name}.s2p"))

    # 畫出 S11 與 S21 的 magnitude (dB)
    network.plot_s_db(m=0, n=0)  # S11
    network.plot_s_db(m=1, n=0)  # S21
    plt.title("S11 & S21 (dB)")
    plt.grid(True)
    plt.show()
```

![2025-05-03_11-49-24](/assets/2025-05-03_11-49-24.png)