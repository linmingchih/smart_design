PyEDB 與 Cadence 工具整合
---

本文檔說明如何使用 PyEDB 處理 Cadence Allegro 的 PCB 設計檔案，並介紹相關的匯入功能和工作流程。

## 簡介

**SKILL** 是 Cadence 系統公司開發的專屬程式語言，主要用於其 EDA 工具（如 Allegro、Virtuoso 等）的自動化與客製化。雖然 PyEDB 本身不直接執行 SKILL 程式碼，但它提供了強大的功能來匯入和處理 Cadence Allegro 產生的 `.brd` 檔案，使得 Python 開發者可以利用 PyEDB 的 API 來自動化 PCB 設計分析流程。

### PyEDB 支援的 Cadence 相關功能

* 匯入 Cadence Allegro `.brd` 檔案
* 轉換為 AEDB 格式進行電磁模擬分析
* 支援多種 PCB 設計檔案格式的互轉換
* 可與 Ansys AEDT 工具鏈整合進行 SI/PI 分析

## 授權需求

根據 Ansys AEDT 版本的不同，匯入 Cadence Allegro `.brd` 檔案需要不同的授權：

| AEDT 版本 | 授權需求 |
|-----------|---------|
| AEDT 2024（含）之前 | Allegro license |
| AEDT 2025 | Allegro + partner_extracta license |

**注意**：在執行 PyEDB 程式碼前，請確認已正確設置所需的授權伺服器。

## 匯入 Cadence Allegro 檔案

### 基本用法

PyEDB 提供了直接開啟 `.brd` 檔案的功能，會自動將其轉換為 `.aedb` 格式：

```python
from pyedb import Edb

# 直接開啟 Cadence Allegro .brd 檔案
edb = Edb("D:/demo/Galileo_G87173_204.brd", edbversion='2024.1')

# 檢查是否成功開啟
print(f"已開啟設計: {edb.cellname}")
print(f"EDB 路徑: {edb.edbpath}")

# 儲存為 .aedb 格式
edb.save_edb_as("D:/demo/output_design.aedb")

# 關閉 EDB
edb.close()
```

### 使用 import_cadence_file() 方法

PyEDB 還提供了專門的 `import_cadence_file()` 方法來匯入 Cadence 檔案：

```python
from pyedb import Edb

# 建立新的 EDB 實例
edb = Edb(edbversion='2024.1')

# 使用 import_cadence_file 方法匯入
edb.import_cadence_file("D:/designs/my_board.brd")

# 進行後續處理
print(f"設計名稱: {edb.cellname}")
print(f"層數: {edb.stackup.num_layers}")

# 列出所有網路
for net_name, net_obj in edb.nets.items():
    print(f"網路: {net_name}")

edb.save_edb()
edb.close()
```

## 支援的檔案格式

PyEDB 可以匯入多種 PCB/IC 設計檔案格式，這些格式都可以透過 `Edb()` 建構子直接開啟：

| 格式 | 副檔名 | 說明 |
|------|--------|------|
| Cadence Allegro | `.brd` | PCB 設計檔案 |
| GDSII | `.gds`, `.gdsII` | IC 版圖設計 |
| ODB++ | `.odb++` | PCB 製造交換格式 |
| IPC2581 | `.xml` | 電子組裝資料交換標準 |
| DXF | `.dxf` | CAD 圖面交換格式 |

### 批次轉換範例

以下範例示範如何批次將多個 `.brd` 檔案轉換為 `.aedb` 格式：

```python
from pyedb import Edb
import os
import glob

def batch_convert_brd_to_aedb(input_folder, output_folder, edb_version='2024.1'):
    """
    批次轉換 .brd 檔案為 .aedb 格式
    
    Parameters
    ----------
    input_folder : str
        包含 .brd 檔案的資料夾路徑
    output_folder : str
        輸出 .aedb 檔案的資料夾路徑
    edb_version : str
        EDB 版本號
    """
    # 確保輸出資料夾存在
    os.makedirs(output_folder, exist_ok=True)
    
    # 尋找所有 .brd 檔案
    brd_files = glob.glob(os.path.join(input_folder, "*.brd"))
    
    print(f"找到 {len(brd_files)} 個 .brd 檔案")
    
    for brd_file in brd_files:
        try:
            print(f"正在轉換: {os.path.basename(brd_file)}")
            
            # 開啟 .brd 檔案
            edb = Edb(brd_file, edbversion=edb_version)
            
            # 建立輸出檔案路徑
            base_name = os.path.splitext(os.path.basename(brd_file))[0]
            output_path = os.path.join(output_folder, f"{base_name}.aedb")
            
            # 儲存為 .aedb
            edb.save_edb_as(output_path)
            
            # 顯示基本資訊
            print(f"  - 設計名稱: {edb.cellname}")
            print(f"  - 層數: {edb.stackup.num_layers}")
            print(f"  - 網路數: {len(edb.nets)}")
            print(f"  - 元件數: {len(edb.components.components)}")
            
            # 關閉 EDB
            edb.close()
            
            print(f"✓ 轉換完成: {output_path}\n")
            
        except Exception as e:
            print(f"✗ 轉換失敗: {brd_file}")
            print(f"  錯誤: {str(e)}\n")

# 使用範例
if __name__ == "__main__":
    input_dir = "D:/cadence_designs"
    output_dir = "D:/aedb_output"
    
    batch_convert_brd_to_aedb(input_dir, output_dir, '2024.1')
```

## 轉換後的常見操作

### 1. 檢視堆疊結構

```python
from pyedb import Edb

edb = Edb("design.brd", edbversion='2024.1')

# 列出所有層
print("堆疊層資訊:")
for layer_name, layer in edb.stackup.stackup_layers.items():
    print(f"  層名稱: {layer_name}")
    print(f"  層類型: {layer.type}")
    print(f"  厚度: {layer.thickness}")
    print()

edb.close()
```

### 2. 分析網路連接

```python
from pyedb import Edb

edb = Edb("design.brd", edbversion='2024.1')

# 取得特定網路資訊
net_name = "GND"
if net_name in edb.nets:
    net = edb.nets[net_name]
    components = edb.core_nets.components_by_nets
    
    print(f"網路 '{net_name}' 連接的元件:")
    if net_name in components:
        for comp in components[net_name]:
            print(f"  - {comp}")

edb.close()
```

### 3. 設置端口並匯出至 HFSS

```python
from pyedb import Edb
from pyaedt import Hfss3dLayout

# 開啟 Cadence 設計
edb = Edb("design.brd", edbversion='2024.1')

# 在特定元件上建立端口
edb.core_components.create_port_on_component('U1', ['DDR_DQ0', 'DDR_DQ1'])

# 建立 HFSS 設定
setup = edb.create_hfss_setup("MySetup")

# 儲存 EDB
output_aedb = "design_with_ports.aedb"
edb.save_edb_as(output_aedb)
edb.close()

# 在 HFSS 3D Layout 中開啟
hfss = Hfss3dLayout(output_aedb, specified_version='2024.1')
print(f"已在 HFSS 3D Layout 中開啟設計")
```

### 4. 電源完整性分析設定

```python
from pyedb import Edb

edb = Edb("design.brd", edbversion='2024.1')

# 建立 SIwave DC 分析設定
dc_setup = edb.create_siwave_dc_setup("DC_Analysis")

# 在電源網路上建立激勵源
edb.core_siwave.create_voltage_source_on_pin(
    component_name="U1",
    net_name="VDD",
    voltage_value="1.0V"
)

# 建立電流源
edb.core_siwave.create_current_source_on_pin(
    component_name="U2",
    net_name="VDD",
    current_value="2A"
)

# 儲存並關閉
edb.save_edb_as("design_dc_analysis.aedb")
edb.close()
```

## 與 SKILL 腳本的比較

雖然 PyEDB 不直接執行 SKILL 腳本，但對於熟悉 SKILL 的工程師來說，以下是兩者的主要差異：

| 功能 | SKILL (Cadence) | PyEDB (Python) |
|------|-----------------|----------------|
| **執行環境** | Cadence 工具內部 | 獨立 Python 環境 |
| **主要用途** | Allegro/Virtuoso 自動化 | EDB/AEDB 檔案處理與分析 |
| **學習曲線** | 專屬語法，較陡峭 | Python 生態，容易上手 |
| **整合性** | 深度整合 Cadence 工具 | 整合 Ansys AEDT 與 Python 生態系 |
| **分析能力** | 設計規則檢查、佈局編輯 | 電磁模擬、SI/PI 分析 |

## 工作流程建議

### 典型的 Cadence 到 Ansys 工作流程

```
┌─────────────────┐
│ Cadence Allegro │ 
│   (.brd 檔案)   │
└────────┬────────┘
         │
         │ PyEDB 匯入
         ▼
┌─────────────────┐
│  PyEDB 處理     │
│  - 建立端口     │
│  - 設定激勵     │
│  - 簡化模型     │
└────────┬────────┘
         │
         │ 儲存 .aedb
         ▼
┌─────────────────┐
│  Ansys AEDT     │
│  - HFSS 3D      │
│  - SIwave       │
│  - Q3D          │
└─────────────────┘
```

### 推薦的 Python 腳本結構

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Cadence Allegro 設計自動化處理腳本
"""

from pyedb import Edb
from pyaedt import Hfss3dLayout
import logging

# 設定日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def process_cadence_design(brd_file, output_aedb, edb_version='2024.1'):
    """
    處理 Cadence 設計檔案
    
    Parameters
    ----------
    brd_file : str
        輸入的 .brd 檔案路徑
    output_aedb : str
        輸出的 .aedb 檔案路徑
    edb_version : str
        EDB 版本
    """
    try:
        logger.info(f"開始處理: {brd_file}")
        
        # 1. 匯入 Cadence 設計
        edb = Edb(brd_file, edbversion=edb_version)
        logger.info(f"已載入設計: {edb.cellname}")
        
        # 2. 顯示基本資訊
        logger.info(f"層數: {edb.stackup.num_layers}")
        logger.info(f"網路數: {len(edb.nets)}")
        logger.info(f"元件數: {len(edb.components.components)}")
        
        # 3. 進行必要的處理（依需求修改）
        # 例如：建立端口、設定材料、簡化模型等
        
        # 4. 儲存結果
        edb.save_edb_as(output_aedb)
        logger.info(f"已儲存: {output_aedb}")
        
        # 5. 清理
        edb.close()
        
        return True
        
    except Exception as e:
        logger.error(f"處理失敗: {str(e)}")
        return False

if __name__ == "__main__":
    # 使用範例
    input_brd = "D:/designs/my_board.brd"
    output_path = "D:/designs/my_board_processed.aedb"
    
    success = process_cadence_design(input_brd, output_path, '2024.1')
    
    if success:
        print("✓ 處理完成")
    else:
        print("✗ 處理失敗")
```

## 常見問題

### Q1: PyEDB 可以直接修改 .brd 檔案嗎？

**A:** 不行。PyEDB 只能讀取 `.brd` 檔案並轉換為 `.aedb` 格式。若需要修改原始 Cadence 設計，必須在 Allegro 中進行。

### Q2: 轉換後的 .aedb 檔案可以再轉回 .brd 嗎？

**A:** 不行。轉換是單向的。`.aedb` 格式主要用於 Ansys 的電磁模擬分析，無法直接轉回 Cadence 格式。

### Q3: 匯入時遇到「找不到授權」錯誤怎麼辦？

**A:** 確認以下事項：
1. 檢查授權伺服器是否正常運作
2. 確認環境變數 `ANSYSEM_LICENSE_FILE` 是否正確設置
3. 確認使用的 AEDT 版本與所需授權是否匹配
4. 聯繫 IT 管理員確認授權可用性

### Q4: 轉換大型設計時很慢，有優化方法嗎？

**A:** 可以考慮以下方法：
1. 使用較新版本的 AEDT（效能較佳）
2. 在轉換前在 Allegro 中簡化設計
3. 使用 `create_cutout()` 方法只保留關注區域
4. 利用多執行緒處理功能（如 `create_cutout_multithread()`）

### Q5: 如何在 PyEDB 中執行類似 SKILL 的迴圈操作？

**A:** 使用 Python 的標準語法：

```python
from pyedb import Edb

edb = Edb("design.brd", edbversion='2024.1')

# 遍歷所有元件（類似 SKILL 的 foreach）
for comp_name, comp_obj in edb.components.components.items():
    print(f"元件: {comp_name}")
    
    # 遍歷元件的所有接腳
    pins = edb.components.get_pin_from_component(comp_name)
    for pin in pins:
        print(f"  - 接腳: {pin}")

edb.close()
```

## 參考資源

### PyEDB 官方文件
* [PyEDB API 文件](https://edb.docs.pyansys.com/)
* [PyAEDT 文件](https://aedt.docs.pyansys.com/)

### 相關教學
* 參考本目錄下的其他教學文件：
  - `常用方法.md` - PyEDB 常用 API 速查
  - `PyEDB 常問問題集.md` - 更多疑難排解
  - `PyEDB Workshop Labs.md` - 實作練習
  - `Stackup匯出匯入EXCEL.md` - 堆疊結構處理

### Cadence 工具資訊
* Cadence Allegro PCB Designer
* Cadence Design Entry HDL
* SKILL Programming Language Reference

## 結語

PyEDB 為 Cadence Allegro 使用者提供了一個強大的 Python 自動化介面，使得工程師能夠結合 Cadence 的 PCB 設計能力與 Ansys 的電磁分析能力。雖然 PyEDB 不直接執行 SKILL 腳本，但透過 Python 豐富的生態系統與簡潔的語法，可以實現更靈活、更強大的自動化流程。

建議工程師根據具體需求選擇適當的工具：
- **Cadence Allegro + SKILL**：適合 PCB 佈局設計與製造輸出
- **PyEDB + Python**：適合電磁模擬前處理與 SI/PI 分析

兩者結合使用，可以建立完整的 PCB 設計到驗證工作流程。
