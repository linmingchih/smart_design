HFSS 場值資料擷取與三向切片繪圖
---

這段程式碼的主要目的是從 Ansys HFSS 中擷取特定的電磁場強度（如電場的複數大小 `ComplexMag_E`），並將資料輸出為文字格式，接著用 Python 進行資料處理與視覺化，產生 XY、XZ、YZ 三個平面的切片影像，方便使用者觀察空間中場的分佈情形。

### 流程架構

1. **HFSS 場值資料擷取**

   * 使用 `ansys.aedt.core.Hfss` 來啟動 HFSS 並載入模型。
   * 透過 `get_model_bounding_box()` 取得模型邊界，作為場值擷取的範圍。
   * 使用 `fields_calculator.export()` 將指定場量以 Cartesian 網格格式匯出成 `.fld` 檔案。

2. **讀取與處理擷取的資料**

   * 手動解析 `.fld` 檔案，過濾出有效資料（XYZ 坐標與場值）。
   * 將資料轉為 Pandas 的 DataFrame 結構以利處理。
   * 可選擇是否轉為 dB 單位進行對數尺度的視覺化（避免 log(0) 問題以加入 `eps`）。

3. **視覺化場值切片**

   * 根據三個方向的 Z、Y、X 切片位置，依序畫出 XY、XZ、YZ 切片圖。
   * 使用 `pivot` 將 DataFrame 整理為矩陣格式，方便用 `imshow` 顯示熱圖。
   * 加入色彩條、標題與坐標標籤，並儲存成 PNG 檔案於指定目錄。

### 補充說明

* `field_name = 'ComplexMag_E'` 是 HFSS 中常用的場量名稱，代表電場的複數大小，可改成其他如 `Mag_H` 或 `Phase_E` 擷取不同物理量。
* `fields_calculator.export()` 是 Ansys AEDT Python API 的進階功能，能將模擬結果以網格方式輸出，方便進一步客製化處理。
* 這種作法的**最大優點**是速度快與彈性高：**只需一次從 HFSS 匯出整個空間的場值資料，之後所有切片、視覺化、統計分析都可在 Python 中離線處理**，大幅減少多次互動 HFSS 的開銷。
* `pivot()` 是 Pandas 中常用的資料重組方式，能將原始表格轉為以某兩欄為座標軸的矩陣格式，適合用來畫等高圖、熱圖。
* `np.log10` 計算 dB 值常會遇到資料為 0 的問題，因此加入 `eps`（極小值）來避免 `log(0)` 報錯。

這份程式整體設計清晰，適合用來自動化分析 HFSS 模擬後的場分佈結果，亦方便後續應用於多組模擬結果的批次處理與視覺比較。


```python
import os
from ansys.aedt.core import Hfss

output_dir = 'd:/demo2'     # 輸出資料夾
field_name = 'ComplexMag_E'              # 欲擷取的場值欄位
grid_step = 0.05                  # 場值擷取用的網格解析度
slice_step = 1.0                  # 切片位置的間距

hfss = Hfss(version='2025.1')
x0, y0, z0, x1, y1, z1 = hfss.modeler.get_model_bounding_box()

hfss.post.fields_calculator.export(
    field_name,
    grid_type='Cartesian',
    output_file=os.path.join(output_dir, 'data.fld'),
    grid_start=(x0, y0, z0),
    grid_stop=(x1, y1, z1),
    grid_step=(grid_step, grid_step, grid_step),
    is_vector = True
)

#%%
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ========== 設定 ==========
file_path = "d:/demo2/data.fld"
output_dir = "d:/demo2"
verbose = True
use_db = True  # <--- 是否轉換為 dB 模式
eps = 1e-20    # <--- 防止 log(0) 出錯

# ========== 讀取檔案 ==========
raw_data = []
field_name = "Field"
with open(file_path, "r") as f:
    for line in f:
        line = line.strip()
        if line.startswith("X,") or "Scalar data" in line:
            if "Scalar data" in line:
                field_name = line.split('"')[-2].strip()
                if verbose:
                    print(f"偵測物理量名稱：{field_name}")
            continue
        try:
            parts = list(map(float, line.split()))
            if len(parts) == 4:
                raw_data.append(parts)
        except ValueError:
            continue

# ========== 組成 DataFrame ==========
df = pd.DataFrame(raw_data, columns=["X", "Y", "Z", field_name])
df = df.astype(float)

# ========== 若啟用 dB 模式 ==========
if use_db:
    db_field_name = field_name + "_dB"
    df[db_field_name] = 20 * np.log10(df[field_name].abs() + eps)
    field_name = db_field_name  # 替換欄位名稱

# ========== 基本統計 ==========
vmin = df[field_name].min()
vmax = df[field_name].max()

x_vals = sorted(df["X"].unique())
y_vals = sorted(df["Y"].unique())
z_vals = sorted(df["Z"].unique())

if verbose:
    print(f"X steps: {len(x_vals)}, Y steps: {len(y_vals)}, Z steps: {len(z_vals)}")

# ========== 畫 XY 切片 ==========
for z in z_vals:
    slice_df = df[df["Z"] == z]
    if not slice_df.empty:
        pivot = slice_df.pivot(index="Y", columns="X", values=field_name)
        plt.imshow(pivot.values,
                   extent=[min(x_vals), max(x_vals), min(y_vals), max(y_vals)],
                   origin="lower", cmap="jet", vmin=vmin, vmax=vmax, aspect='equal')
        plt.colorbar(label=field_name)
        plt.xlabel("X (m)")
        plt.ylabel("Y (m)")
        plt.title(f"{field_name} XY @ Z={z*1e3:.2f} mm")
        plt.axis("equal")  # 強制坐標等比
        plt.savefig(f"{output_dir}/{field_name}_xy_z{z*1e3:.3f}mm.png", dpi=300)
        plt.close()

# ========== 畫 XZ 切片 ==========
for y in y_vals:
    slice_df = df[df["Y"] == y]
    if not slice_df.empty:
        pivot = slice_df.pivot(index="Z", columns="X", values=field_name)
        plt.imshow(pivot.values,
                   extent=[min(x_vals), max(x_vals), min(z_vals), max(z_vals)],
                   origin="lower", cmap="jet", vmin=vmin, vmax=vmax, aspect='equal')
        plt.colorbar(label=field_name)
        plt.xlabel("X (m)")
        plt.ylabel("Z (m)")
        plt.title(f"{field_name} XZ @ Y={y*1e3:.2f} mm")
        plt.axis("equal")
        plt.savefig(f"{output_dir}/{field_name}_xz_y{y*1e3:.3f}mm.png", dpi=300)
        plt.close()

# ========== 畫 YZ 切片 ==========
for x in x_vals:
    slice_df = df[df["X"] == x]
    if not slice_df.empty:
        pivot = slice_df.pivot(index="Z", columns="Y", values=field_name)
        plt.imshow(pivot.values,
                   extent=[min(y_vals), max(y_vals), min(z_vals), max(z_vals)],
                   origin="lower", cmap="jet", vmin=vmin, vmax=vmax, aspect='equal')
        plt.colorbar(label=field_name)
        plt.xlabel("Y (m)")
        plt.ylabel("Z (m)")
        plt.title(f"{field_name} YZ @ X={x*1e3:.2f} mm")
        plt.axis("equal")
        plt.savefig(f"{output_dir}/{field_name}_yz_x{x*1e3:.3f}mm.png", dpi=300)
        plt.close()
```

![2025-05-13_10-43-34](/assets/2025-05-13_10-43-34.png)