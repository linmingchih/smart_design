Maxwell3D 自動輸出磁場模擬圖片
---

這段程式碼的目的是從 Ansys Maxwell3D 的模擬結果中，依據時間步長自動生成磁場分佈圖，並以 PNG 圖檔方式儲存至指定資料夾，方便後續分析或報告使用。

### 功能

* 載入 Ansys Maxwell3D 模型並讀取模擬結果
* 取得主要掃描變數（如時間）
* 產生磁通密度（Mag\_B）的表面場圖
* 按照不同時間點輸出等角投影的磁場圖片
* 釋放 Maxwell Desktop 資源

### 流程架構

1. **初始化 Maxwell3d 環境**：透過 `Maxwell3d(version='2025.1')` 啟動指定版本。
2. **讀取模擬資料**：用 `get_solution_data_per_variation()` 取得模擬變數（如時間）對應的結果。
3. **建立場圖（Field Plot）**：針對第一個時間點，產生一個名為 `magB_plot` 的磁通密度圖。
4. **逐時間點輸出圖片**：

   * 使用 `SetPlotsViewSolutionContext` 設定場圖對應的時間上下文。
   * 使用 `export_model_picture` 將目前視角和場圖輸出為圖片。
5. **結束模擬環境**：用 `release_desktop()` 釋放資源。

### 補充說明

* `get_solution_data_per_variation()` 是用來取得變化參數（如時間）與對應的模擬數據。
* `create_fieldplot_surface` 是建立某部件（例如 Stator）的磁場圖，其中 `intrinsics` 可設定時間點。
* `SetPlotsViewSolutionContext` 是指定目前圖像要根據哪個時間點來顯示模擬結果。
* `export_model_picture` 可將目前場圖以指定視角（例如 isometric）輸出成圖片。

### 範例程式

```python
import os
from ansys.aedt.core import Maxwell3d

# 初始化 Maxwell3D 環境
maxwell = Maxwell3d(version='2025.1')

# 取得模擬數據（依據不同變數，如時間）
data = maxwell.post.get_solution_data_per_variation(expression='', solution_type='Fields')
ts = data.primary_sweep_values

# 建立磁通密度場圖（取第一個時間點）
maxwell.post.create_fieldplot_surface('Stator', 'Mag_B', intrinsics={'Time':ts[0]}, plot_name='magB_plot')

# 指定輸出資料夾
output_directory = 'd:/demo2'

# 依據每個時間點輸出磁場圖
for t in ts:
    maxwell.ofieldsreporter.SetPlotsViewSolutionContext(['magB_plot'], "Setup1 : Transient", f'Time="{t}"')
    png_path = os.path.join(output_directory, f'{t}.png')
    maxwell.post.export_model_picture(png_path, field_selections='all', orientation="isometric")

# 釋放資源
maxwell.release_desktop()
```

![2025-06-05_09-29-12](/assets/2025-06-05_09-29-12.png)