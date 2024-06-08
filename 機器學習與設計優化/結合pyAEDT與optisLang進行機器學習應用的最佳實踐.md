結合pyAEDT與optisLang進行機器學習應用的最佳實踐
---
隨著機器學習技術的快速發展，越來越多的工具和軟件被開發出來，以幫助研究者和工程師在不同領域進行應用。本文旨在探討如何有效結合pyAEDT與optisLang，並在機器學習項目中實施這些工具，以提高效率和結果的準確性。本文將介紹這兩款工具的基本功能、結合使用的優勢以及在實際應用中的最佳實踐。

### 流程說明

在optisLang建模中，主要使用AMOP模塊，並連接Python模塊。該Python模塊可以透過pyAEDT連接AEDT進行建模、設置、模擬並抓取數據。以下是具體操作和注意事項：

1. **AMOP模塊設置** ：
- 使用AMOP模塊作為主模塊，允許使用者定義參數輸入範圍和機器學習算法設置。
- 執行時，AMOP從所有參數構成的參數空間產生樣本點，這些樣本點將饋入Python模塊。並從Python方塊抓取資料以作機器學習。
2. **Python模塊設置** ：
- 連接Python腳本，在Python腳本中，使用pyAEDT進行模型設置、模擬並提取數據。 
- 配置Python模塊的參數（左側欄位）和響應（右側欄位）。

3. **數據處理與優化** ：
- AMOP模塊迭代運行，不斷送入參數樣本點，並通過Python模塊獲取模擬結果。
- 使用這些結果訓練機器學習模型，評估模型預測能力，直到達到所需的準確度。
- 完成之後生成AMOP.omdb檔案，使用者可以將參數輸入到模型當中並快速得到計算結果。

![2024-06-08_11-47-52](/assets/2024-06-08_11-47-52.png)

### 注意事項
1. 在pyAEDT腳本中，參數定義通常放在以下模塊當中：

```python
if not 'OSL_REGULAR_EXECUTION' in locals(): 
    OSL_REGULAR_EXECUTION = False

if not OSL_REGULAR_EXECUTION:
    pcb_w = 30 # 30
    pcb_l = 30 # 30
    ws = 28.5 # (15, 35)
    ls = 10 # [10, 11, 12]
    dd = 1.5 # (1, 3)
    w1 = 2.5 # (1, 4)
    w2 = 1.5 # (1, 4)
    gap1 = 2 # (1, 5)
    gap2 = 1 # (1, 3)
    wf = 3 # (-4, 4)
    lf = 13 # (13, 16)
    t = 1 # 1
```

響應定義方式
```python
    s11_2p4 = y[14]  # response
    s11_5p8 = y[48]  # response
```

此代碼段確保參數開發及調試階段可以被初始化，但在optisLang模型訓練階段不會被執行，如此AMOP傳遞進Python模塊便不會被覆蓋。參數定義後面並以註解方式設置了參數的範圍和類型（連續或離散）。

2. 在pyAEDT腳本中進行例外處理，這可以確保在某組參數無法成功建模時，程式能夠正確地關閉並返回optisLang，繼續處理下一組參數。以下是腳本示例：

``` python
import pyaedt
import time
from pyaedt import Hfss

# 禁用錯誤處理器
pyaedt.settings.enable_error_handler = False

try:
    # 初始化Hfss
    hfss = Hfss(specified_version='2024.1', non_graphical=False)
    
    # 前處理程式碼
    # （在這裡設置您的模型和參數）

    # 驗證設計
    if not hfss.validate_full_design()[-1]:
        raise ValueError("Failed Validation.")

    # 執行模擬
    hfss.analyze_nominal(num_cores=20)
    
    # 後處理程式碼
    # （在這裡處理模擬結果）

except Exception as e:
    print(f"An error occurred: {e}")
    pass

finally:
    # 關閉專案且不保存
    hfss.close_project(save_project=False)
    time.sleep(5)

```

3. 使用PyOptisLang腳本建立新的optisLang檔案(.opf)，該腳本可以讀取Python參數定義及響應定義並自動添加到python模塊及AMOP模塊當中，大大節省手動設置時間



4. optisLang一旦完成機器模型訓練，會輸出omdb檔案。我們便可以用Python程式碼調用該機器模型，輸入參數並迅速得到結果。

```python
from mopsolver import MOPSolver
osl_install_path = r'C:\Program Files\ANSYS Inc\v241\optiSLang'
omdb_file = r"D:/OneDrive - ANSYS, Inc/GitHub/generate_opf/assets/dual_band_antenna.opd/AMOP/AMOP.omdb"

solver = MOPSolver(osl_install_path, omdb_file)

print(solver)
print(solver.run([[15.1, 10.0, 1.01, 1.015, 1.015, 1.0199999999999998, 1.01, 2.01, 13.015], 
                  [34.9, 12.0, 2.99, 3.9850000000000003, 3.985, 4.98, 2.99, 3.99, 15.985]]))
```