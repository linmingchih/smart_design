透過 Python 操作非圖形模式（NonGraphical Mode）執行自動化流程
---

### 目的

這段程式碼示範如何使用 ANSYS 提供的 Python API，啟動 HFSS 的**非圖形模式**進行自動化作業。非圖形模式不會開啟 GUI，適合在伺服器或背景執行環境下使用，大幅提升自動化腳本的效率與穩定性。

範例中以列出 HFSS 專案中各設計的分析設定與掃描參數為例，說明非圖形模式的應用。

### 功能

* 在非圖形模式下初始化 ANSYS HFSS 操作環境。
* 開啟指定 HFSS 專案（.aedt）。
* 列出專案中各個設計（Design）的分析設定與掃描（Sweep）資訊。
* 關閉專案並釋放資源。

### 流程架構

1. **匯入與初始化**：

   * 將 ANSYS Python API 插件路徑加入 Python 系統路徑。
   * 使用 `ScriptEnv.InitializeNew(NonGraphical=True)` 啟動非圖形模式。

2. **打開 HFSS 專案檔**：

   * 使用 `oDesktop.OpenProject()` 指定並開啟 `.aedt` 專案檔案。

3. **範例操作流程**（取得設計設定）：

   * 使用 `GetTopDesignList()` 取得所有設計名稱。
   * 對每個設計設為當前操作對象，並取得分析模組。
   * 讀取該設計中每個分析設定及其掃描參數，並輸出。

4. **結束並釋放資源**：

   * 關閉專案，並結束 ANSYS 環境。

### 補充說明

* **非圖形模式的優勢**：

  * 不需開啟 GUI，減少資源消耗。
  * 適用於自動化、CI/CD、批次模擬前檢查等背景任務。
  * 較少受到 GUI 相依設定或視窗卡頓影響。

* `ScriptEnv.InitializeNew(NonGraphical=True)`：是這段程式碼的關鍵，代表所有動作都會在背景模式下執行。

* 此範例使用分析設定與掃描資訊當作展示內容，實際可延伸應用至模型參數調整、自動化模擬流程、結果匯出等。

### 範例程式

```python
import sys
# 新增 ANSYS Python API 所在路徑
sys.path.append(r"C:\Program Files\ANSYS Inc\v252\AnsysEM\PythonFiles\DesktopPlugin")

import ScriptEnv
# 初始化 ANSYS 操作環境（非圖形模式）
ScriptEnv.InitializeNew(NonGraphical=True)

# 開啟 HFSS 專案
oProject = oDesktop.OpenProject(r"C:\Program Files\ANSYS Inc\v252\AnsysEM\Examples\HFSS\RF Microwave\Bandpass_Filter.aedt")

# 取得所有設計名稱並依序讀取設定
design_names = oProject.GetTopDesignList()
for dn in design_names:
    oProject.SetActiveDesign(dn)             # 設定目前操作設計
    oDesign = oProject.GetActiveDesign()     # 取得設計物件
    oAnalysis = oDesign.GetModule("AnalysisSetup")  # 取得分析模組
    setups = oAnalysis.GetSetups()           # 所有分析設定名稱
    for sn in setups:
        sweeps = oAnalysis.GetSweeps(sn)     # 該設定下的掃描名稱
        print(dn, sn, sweeps)                # 輸出資訊

# 關閉專案與環境
oProject.Close()
ScriptEnv.Shutdown()
```
