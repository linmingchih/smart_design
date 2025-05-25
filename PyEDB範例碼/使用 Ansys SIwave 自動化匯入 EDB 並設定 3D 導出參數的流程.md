使用 Ansys SIwave 自動化匯入 EDB 並設定 3D 導出參數的流程
---

## 目的

這段程式碼的目的是透過 Python 自動化流程，利用 Ansys 的 API 將一個 EDB 電路資料檔匯入 SIwave，進行基本設定後，再將其導出成 3D 模型，以便後續在 HFSS/Q3D/Maxwell 等工具中進行電磁模擬。

### 功能

* 使用 `win32com` 操控 SIwave 應用程式開啟指定專案。
* 利用 `ansys.aedt.core` 的 Edb 模組讀取與另存修正版的 EDB 檔案。
* 設定介電層上的過孔（via）形狀與尺寸。
* 指定過孔的鍍銅比例。
* 選取特定訊號網路進行後續操作。
* 套用設定檔，將模型輸出為適用於 HFSS/Q3D/Maxwell 的 3D 格式。

### 流程架構

1. **初始化與路徑設定**：
   設定 EDB、設定檔與輸出資料夾的路徑，並產生另存的檔案路徑。

2. **EDB 資料處理**：
   使用 Ansys 的 `Edb` 類別載入原始 EDB 檔，提取所有的網路（nets）與介電層（dielectric layers）名稱，再另存為 \*\_fixed.aedb。

3. **SIwave 操作流程**：

   * 將 EDB 匯入 SIwave 專案中。
   * 設定指定過孔於各介電層的焊墊（Pad）形狀與尺寸。
   * 設定過孔的鍍銅比例為 30%。
   * 選取所有非 DUMMY 的訊號網路進行後續處理。
   * 匯入預先設定的 3D 導出選項。
   * 將處理後的模型導出為 3D 模型。
   * 關閉專案並結束應用程式。

### 補充說明

* `win32com.client.Dispatch`：用來啟動並控制 Windows COM 介面的 SIwave 應用程式。
* `Edb` 類別：Ansys 提供用於讀取與操作 AEDT EDB 檔案的 Python API。
* `ScrSetPadOnLayer`：設定指定層上過孔的 pad 外型與尺寸。
* `ScrSetPadstackViaPlatingRatio`：設定過孔的鍍銅比例，影響電氣與熱傳導性能。
* `ScrSetOptionsFor3DModelExport` 與 `ScrExport3DModel`：設定與執行將模型匯出為 Maxwell 支援的 3D 模型格式。
* `options.config` 檔案：這是一個文字設定檔，供 SIwave 在導出 3D 模型時使用，內容可以定義如：要包含哪些金屬層、是否保留過孔結構、是否簡化幾何外型、不同材質屬性定義等。透過這個設定檔，使用者可以更細緻地控制匯出的 3D 模型內容與品質，提升與 Maxwell 等模擬工具的整合度與精準性。

### 範例程式

```python
import os
from ansys.aedt.core import Edb
from win32com import client

# 啟動 SIwave 應用程式
oApp = client.Dispatch("SIwave.Application.2025.1")
oApp.RestoreWindow()
oDoc = oApp.GetActiveProject()

# 設定檔案路徑
edb_path = "D:/demo2/Galileo_G87173_20454.aedb"
config_path = "D:/demo2/options.config"
q3d_path = 'd:/demo2/test29'
fix_edb_path = edb_path.replace('.aedb', '_fixed.aedb')

# 使用 Edb 操作 EDB 檔案
edb = Edb(edb_path, edbversion='2024.1')
allnets = list(edb.nets.nets.keys())
dielectric_layers = list(edb.stackup.dielectric_layers.keys())
edb.save_edb_as(fix_edb_path)
edb.close_edb()

# 匯入至 SIwave
oDoc.ScrImportEDB(edb_path)

# 設定 pad stack 與鍍銅比例
for name in dielectric_layers[1:-1]:
    oDoc.ScrSetPadOnLayer('VIA_20-10-28_SMB', name, "Circle", "0.40mm", "0.40mm")
oDoc.ScrSetPadstackViaPlatingRatio('VIA_20-10-28_SMB', 0.3)

# 選取所有非 DUMMY 的網路
for net in allnets:
    if net != 'DUMMY':
        oDoc.ScrSelectNet(net, 1)

# 設定並導出 3D 模型
oDoc.ScrSetOptionsFor3DModelExport(config_path)
oDoc.ScrExport3DModel('Maxwell', q3d_path)

# 關閉專案與應用程式
oDoc.ScrCloseProject()
oApp.Quit()
```

![2025-05-23_14-02-23](/assets/2025-05-23_14-02-23.png)



### options.config
```bash
NUM_PADS_FACET_COUNT 16                   # Pad表面離散切分面數，影響3D Pad幾何精細度
NUM_ANTIPAD_FACET_COUNT 16                # Antipad（避孔）離散切分面數
DEFAULT_SOLDERBALL_FACET_COUNT 16         # 預設錫球（solder ball）切分面數
VIA_SEGMENTS 16                           # 每個過孔切分為多少段，影響過孔建模精細度
DEFAULT_BONDWIRE_FACET_COUNT 6            # 預設Bondwire建模時的切分面數
UNITE_NETS 1                              # 是否將同網路物件合併（1:合併, 0:不合併）
EXCLUDE_TERMINALS_FROM_UNITE 1            # 合併網路時是否排除終端（1:排除, 0:不排除）
TOTAL_VIA_FILL 0                          # 過孔是否完全填充（1:填滿, 0:中空）
IGNORE_DIELECTRICS 1                      # 匯出時是否忽略介電材料（1:忽略, 0:包含）
SEPARATE_DIELECTRICS 1                    # 是否將不同介電材料分開建模（1:分開, 0:合併）
UNITE_LAYERS_WITH_SAME_MATERIALS 1        # 相同材料的層是否合併建模（1:合併, 0:分開）
IGNORE_UNCONNECTED_PADS 1                 # 忽略未連接的Pad（1:忽略, 0:包含）
CLIP_TRACES 0                             # 是否裁剪走線以避免重疊（1:裁剪, 0:不裁剪）
CUT_DIELECTRICS 0                         # 是否切割介電體以配合金屬（1:切割, 0:不切割）
CREATE_SHEET_BODIES 0                     # 是否將銅箔表面建模為sheet body（薄殼）（1:是, 0:否）
GENERATE_TERMINALS 0                      # 是否產生終端元件（1:產生, 0:不產生）
IGNORE_PLANES_WITH_AREA_LESS_THAN_THRESOLD 1  # 忽略小面積平面（1:忽略, 0:不忽略）
IGNORE_FLOAT_BODIES 0                     # 是否忽略浮動（未接地/未接線）物件（1:忽略, 0:包含）
MIN_PLANE_AREA 0.358979                   # 平面物件最小面積門檻（單位：mm²），小於此值會被忽略
MIN_EDGE_LENGTH_PADS 1um                  # Pad最小邊長（1微米），小於則合併或忽略
MIN_EDGE_LENGTH_PLANES 1um                # 平面最小邊長
MIN_EDGE_LENGTH_TRACES 1um                # 走線最小邊長
MIN_DIELECTRIC_EDGE_LENGTH 10um           # 介電材料最小邊長
DIELECTRIC_EXPANSION_FACTOR 0.100000      # 介電體膨脹係數（如需擴大邊界以包覆金屬）
IGNORE_HOLES 1                            # 忽略所有過孔與孔洞（1:忽略, 0:包含）
MIN_HOLE_AREA 0.358979                    # 最小孔洞面積，小於此值的孔洞會被忽略
REMOVE-PLATING_TAILS 0                    # 是否移除鍍層尾巴（1:移除, 0:不移除）
SUBTRACT_METAL_FROM_SUBSTRATE 0           # 是否從基板中扣除金屬部分（1:是, 0:否）
DISCRETIZE_ARCS 0                         # 圓弧是否離散化成多段線（1:是, 0:否）
CHOP_TRACE_ENDS 0                         # 走線末端是否切斷（1:切, 0:不切）
AIRBOX_THICKNESS_FACTOR 1.100000          # 空氣盒厚度擴張倍率（用於HFSS邊界條件）
AIRBOX_PAD_AMOUNT_PLUS_Z 0.500000         # 空氣盒Z方向（上方）額外加寬距離（mm）
AIRBOX_PAD_AMOUNT_MINUS_Z 0.500000        # 空氣盒Z方向（下方）額外加寬距離（mm）
PORT_PAD_AMOUNT 0.500000                  # Port端額外加寬距離（mm）
CREATE_PORTS_FOR_PWR_GND_NETS 0           # 是否為電源/地網自動產生Port（1:是, 0:否）
PORTS_FOR_PWR_GND_NETS 0                  # 是否僅為電源/地網產生Port（1:是, 0:否）
LAUNCH_HFSS 1                             # 匯出完成後自動開啟HFSS（1:是, 0:否）
USE_CAUSAL_MATERIALS 1                    # 使用因果性材料模型（1:啟用, 0:關閉）
AUTO_DC_THICKNESS 1                       # DC仿真自動調整厚度（1:是, 0:否）
HFSS_VERSION 2014                         # 指定HFSS版本（如2014）
SOLVE_CAPACITANCE 1                       # 執行電容分析（1:執行, 0:不執行）
SOLVE_DC_RESISTANCE 0                     # 執行DC電阻分析
SOLVE_DC_INDUCTANCE_RESISTANCE 0          # 執行DC電感電阻分析
SOLVE_AC_INDUCTANCE_RESISTANCE 0          # 執行AC電感電阻分析
SOLVE_PROJECT 0                           # 匯出後自動執行專案求解
LAUNCH_Q3D 1                              # 匯出後自動開啟Q3D Extractor（1:是, 0:否）
ASSIGN_SOLDER_BALLS_AS_SOURCES 0          # 錫球是否作為電源端
Q3D_MERGE_SOURCES 0                       # Q3D自動合併Source端
Q3D_MERGE_SINKS 0                         # Q3D自動合併Sink端
Q3D_VERSION 2014                          # Q3D目標版本
ACIS_VERSION 0                            # 幾何匯出時目標ACIS版本
```