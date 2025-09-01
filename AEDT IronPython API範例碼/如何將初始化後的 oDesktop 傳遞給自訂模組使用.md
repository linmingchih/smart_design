如何將初始化後的 oDesktop 傳遞給自訂模組使用
---

這段程式碼示範了如何在使用 ANSYS Python API 操作 HFSS 專案時，將初始化後的 `oDesktop` 物件正確傳遞給外部模組，使模組可以順利存取 HFSS 環境進行自動化控制。

### 功能

* 初始化 ANSYS HFSS 的操作環境（以非圖形模式運行）
* 將 `oDesktop` 指定給模組中的變數
* 開啟指定的 HFSS 專案檔
* 取得所有設計名稱、分析設定與掃描清單
* 輸出整理好的資訊
* 關閉專案與環境，釋放資源

### 流程架構

1. **初始化環境**：透過 `ScriptEnv.InitializeNew(NonGraphical=True)` 啟動非圖形操作模式，適合自動化腳本執行。
2. **全域變數設定**：

   * `ScriptEnv.InitializeNew()` 執行後，ANSYS 會自動在全域命名空間中注入 `oDesktop` 物件，代表 HFSS 的操作介面。
   * 為了讓自訂模組（如 `util.py`）可以使用 `oDesktop`，需在主程式中加上 `util.oDesktop = oDesktop`，手動指定給模組使用。
3. **開啟專案**：呼叫 `util.get_info()` 函式並傳入 `.aedt` 專案路徑，啟動分析流程。
4. **讀取設計與設定**：

   * 取得所有設計名稱（designs）
   * 對每個設計設定為目前操作目標，並取得對應的分析模組（AnalysisSetup）
   * 遍歷分析設定名稱，並取得對應的掃描（sweep）
   * 將結果以 (設計名稱, 設定名稱, 掃描清單) 的形式加入清單中
5. **輸出結果**：印出整理後的資訊供檢查或後續使用
6. **清除環境**：關閉專案與操作環境

### 補充說明

* `ScriptEnv` 是 ANSYS 提供的初始化模組，用來建立與 HFSS 的溝通橋樑。
* `ScriptEnv.InitializeNew(NonGraphical=True)` 執行後，`oDesktop` 會自動變成全域變數。
* `util.oDesktop = oDesktop` 是讓模組 `util.py` 能夠讀取 `oDesktop` 的必要步驟。
* `util.py` 是自定義模組，將資料讀取邏輯封裝為 `get_info()` 函式，讓主程式碼更簡潔。
* `oDesktop` 是 ANSYS 的應用層級物件，代表整個 HFSS 的應用環境。
* `GetModule("AnalysisSetup")` 是 HFSS 中的 API 呼叫方式，用來操作分析設定模組。
* `.GetSweeps()` 是讀取掃描設定的函式。

> 初學者可能對 `oProject`, `oDesign`, `oAnalysis` 等物件不熟悉，這些都是 ANSYS COM API 的常見操作對象，代表專案、設計與模組，都是透過 ANSYS 提供的 Python 介面進行存取與控制。

### 範例程式

#### main.py
```python

import sys
sys.path.append(r"C:\Program Files\ANSYS Inc\v252\AnsysEM\PythonFiles\DesktopPlugin")

import ScriptEnv
import util

# 初始化 ANSYS 環境（非圖形介面）
ScriptEnv.InitializeNew(NonGraphical=True)

# oDesktop 是 ScriptEnv 初始化後自動建立的全域變數
util.oDesktop = oDesktop

# 讀取指定專案的設計與分析資訊
result = util.get_info(r"C:\Program Files\ANSYS Inc\v252\AnsysEM\Examples\HFSS\RF Microwave\Bandpass_Filter.aedt")
print(result)

# 關閉環境
ScriptEnv.Shutdown()
```

#### util.py
```python

def get_info(aedt_path):
    oProject = oDesktop.OpenProject(aedt_path)
    design_names = oProject.GetTopDesignList()
    info = []
    for dn in design_names:
        oProject.SetActiveDesign(dn)
        oDesign = oProject.GetActiveDesign()
        oAnalysis = oDesign.GetModule("AnalysisSetup")
        setups = oAnalysis.GetSetups()
        for sn in setups:
            sweeps = oAnalysis.GetSweeps(sn)
            info.append((dn, sn, sweeps))
    oProject.Close()
    return info
```
