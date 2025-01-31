S參數因果性(Causality)檢查與可視化
---

該程式使用 **ANSYS HFSS**  進行 **S 參數矩陣的因果性檢查** ，並將結果視覺化呈現。首先，`check_causality` 函式透過 **HFSS NdExplorer 工具** ，對指定的 `.snp` 文件執行 **因果性驗證** ，使用者可調整 **誤差容忍度**  和 **CPU 核心數**  來優化計算效能。接著，`load_causality_matrix` 函式讀取 **檢查結果文件** ，解析成 **數值矩陣**  以便後續處理。最後，`plot_causality_matrix` 函式利用 **Matplotlib**  繪製 **因果性矩陣圖** ，其中 **黃色代表 -1（非因果性警告）、綠色代表 0（通過檢查）、紅色則表示異常值** 。該程式採用 **模組化設計** ，確保各功能獨立運作，提升可維護性，並適用於 **自動化因果性分析**  的工程應用場景。![2025-01-31_11-08-43](/assets/2025-01-31_11-08-43.png)

```python
import os
import numpy as np
import matplotlib.pyplot as plt
from ansys.aedt.core import Hfss

def check_causality(snp_path, error_tolerance, cores):
    """使用 HFSS 進行因果性檢查。"""
    hfss = Hfss(version='2024.2', non_graphical=True)
    oTool = hfss.odesktop.GetTool("NdExplorer")
    oTool.CheckCausality(
        "",  # 設計名稱（若從文件載入可留空）
        True,  # 是否從文件載入
        snp_path,  # S 參數矩陣的文件路徑
        "",  # 變數組合名稱（若無可留空）
        error_tolerance / 100,  # 檢查因果性的容許誤差
        True,  # 是否使用多核心
        cores  # 指定要使用的 CPU 核心數
    )

def load_causality_matrix(file_path):
    """讀取因果性檢查結果矩陣。"""
    with open(file_path, "r") as file:
        lines = file.readlines()
    
    rows, cols = map(int, lines[0].split())
    matrix_data = [list(map(float, line.split())) for line in lines[1:] if line.strip()]
    matrix = np.array(matrix_data)
    
    if matrix.shape != (rows, cols):
        raise ValueError("矩陣數據與指定大小不匹配")
    
    return matrix, rows, cols

def plot_causality_matrix(matrix, rows, cols):
    """繪製因果性矩陣圖。"""
    color_map = {-1: 'yellow', 0: 'green'}
    colors = np.array([[color_map.get(val, 'red') for val in row] for row in matrix], dtype=object)
    
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.set_xticks(np.arange(cols) + 0.5, minor=False)
    ax.set_yticks(np.arange(rows) + 0.5, minor=False)
    ax.set_xticklabels([f'P{i+1}' for i in range(cols)])
    ax.set_yticklabels([f'P{i+1}' for i in range(rows)])
    
    for i in range(rows):
        for j in range(cols):
            ax.add_patch(plt.Rectangle((j, rows - 1 - i), 1, 1, color=colors[i, j], ec="black"))
    
    ax.set_xlim(0, cols)
    ax.set_ylim(0, rows)
    ax.set_xticks(np.arange(cols+1), minor=True)
    ax.set_yticks(np.arange(rows+1), minor=True)
    ax.grid(which="minor", color="black", linestyle='-', linewidth=2)
    ax.tick_params(axis='x', bottom=False, top=False)
    ax.tick_params(axis='y', left=False, right=False)
    
    plt.show()


snp_path = r"D:\demo\aiigx_pkg_hssi.s4p"
error_tolerance_in_percentage = 0.1
cores = 10
snp_dir = os.path.dirname(snp_path)

check_causality(snp_path, error_tolerance_in_percentage, cores)

file_path = os.path.join(snp_dir, "check_causality_causality.txt")
matrix, rows, cols = load_causality_matrix(file_path)
plot_causality_matrix(matrix, rows, cols)


```
### 比較結果
上方HFSS，下方Python輸出

![2025-01-31_10-52-15](/assets/2025-01-31_10-52-15.png)

![2025-01-31_11-08-43](/assets/2025-01-31_11-08-43_9g7qjptqi.png)