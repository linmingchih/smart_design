第1章 PyAEDT 介紹與開發工具安裝
---

在電子與多物理模擬設計日益複雜的今天，如何提升模擬流程效率、減少重複性人工操作、達成流程自動化，是產業界的重要課題。Ansys 公司推出的 Python 生態系統——PyANSYS，正是一個劃時代的解決方案。其中，PyAEDT 以及其子模組 PyAEDT Circuit 是針對電子模擬領域最關鍵的兩個套件。以下將依序介紹這三者的角色與應用。


### PyANSYS：Ansys 的 Python 自動化生態系

PyANSYS 並非單一程式或工具，而是 Ansys 官方推出的一套開源 Python 生態系統，涵蓋多個專門對應不同模擬產品的 Python 套件。其目標是讓工程師透過 Python 腳本整合與自動化整個 Ansys 模擬流程，提升效率並強化資料流程整合。

PyANSYS 生態系包含下列主要模組：
- `PyMAPDL`：操作 Ansys Mechanical（MAPDL）進行結構模擬。
- `PyFluent`：操作 Ansys Fluent 進行流體模擬。
- `PyAEDT`：操作 Ansys Electronics Desktop（HFSS、Q3D、Icepak 等）。
- `PyOptiSLang`：進行設計最佳化與敏感度分析。

PyANSYS 架構具備模組化、開源、跨平台的特性，支援 API 文件完善、可與 Jupyter Notebook 或 CI/CD 系統整合。這為跨部門、多物理模擬與雲端部署打下穩固基礎。

官方網站：https://docs.pyansys.com


### PyAEDT：電子模擬工作流程的自動化引擎

PyAEDT 是 PyANSYS 生態系統中，專門負責操作 Ansys Electronics Desktop 的 Python 套件。AEDT 是 Ansys 用來整合 HFSS（電磁模擬）、Q3D（寄生參數提取）、Icepak（熱模擬）、Maxwell（磁場模擬）等工具的平台。

PyAEDT 可以讓使用者：
- 自動建立與控制設計專案（如 3D Layout、HFSS Design）
- 匯入 PCB 或封裝檔案（如 .aedb 或 .brd）
- 設定材料、激發源、邊界條件、網格與求解器參數
- 啟動模擬、監控進度並擷取結果（如 S 參數、溫度分佈等）
- 匯出圖片、報表與後處理數據

與 GUI 操作不同，PyAEDT 能實現大規模設計流程的程式化控制，適合自動化分析、DOE（設計空間探索）、客製化報表等進階應用。

官方文件：https://aedt.docs.pyansys.com

### PyAEDT Circuit：系統級電路模擬的程式化控制

PyAEDT Circuit 是 PyAEDT 中的一個子模組，專門對應 Electronics Desktop 中的 Circuit Design 模組。該模組常用於系統級電路模擬，包含 SI/PI 分析、電源網路建模、IBIS 模型整合、SPICE 電路驗證等。

透過 PyAEDT Circuit，使用者可以：
- 建立電路拓撲（新增元件、連線、設定參數）
- 匯入 IBIS、Touchstone、SPICE 元件模組
- 控制模擬設定（AC 分析、Transient、S-參數等）
- 自動執行模擬並擷取結果波形或頻響圖
- 結合其他模擬結果（如 HFSS、Q3D）進行聯合分析

此模組特別適用於電源設計工程師與訊號完整性分析人員，可大幅減少建立測試電路的時間，並可與現有流程整合形成完整的自動化模擬鏈。

PyAEDT Circuit 是 PyAEDT 的一部分，可參考相同官方文件：https://aedt.docs.pyansys.com




### 開發環境安裝
使用 Ansys 內建的 Python 建立虛擬環境，安裝所需 Python 套件並啟動 Spyder 編輯器

這段批次檔主要是自動化設定一個新的 Python 虛擬環境（`C:\my_venv`），安裝特定的 Python 套件（例如 `pyaedt`、`matplotlib`、`pyvista`、`spyder`），並開啟 Spyder 開發環境，以方便後續開發與模擬工作。

```python
@echo off

if exist C:\my_venv (
    rmdir /s /q C:\my_venv
)

"C:\Program Files\AnsysEM\v242\Win64\commonfiles\CPython\3_10\winx64\Release\python\python.exe" -m venv C:\my_venv
call C:\my_venv\Scripts\activate.bat
C:\my_venv\Scripts\python.exe -m pip install --upgrade pip
pip install pyaedt==0.14.0 matplotlib pyvista spyder
start spyder

if exist C:\demo (
    rmdir /s /q C:\demo
)

mkdir C:\demo
echo 完成

```



#### 流程架構
1. **刪除舊有虛擬環境**：
   - 如果 `C:\my_venv` 已存在，會先整個刪除以避免衝突。

2. **建立虛擬環境**：
   - 使用 Ansys 安裝目錄中的 Python 執行檔來建立新的虛擬環境在 `C:\my_venv`。

3. **啟動虛擬環境並安裝套件**：
   - 啟用虛擬環境後，先升級 pip。
   - 接著安裝以下套件：
     - `pyaedt==0.15.0`：用於與 Ansys Electronics Desktop 溝通的 Python API
     - `matplotlib`：繪圖用
     - `pyvista`：3D 資料視覺化
     - `spyder`：Python IDE

4. **啟動 Spyder 編輯器**：
   - 安裝完畢後直接開啟 Spyder，方便使用者進行開發

5. **清理與建立資料夾**：
   - 如果 `C:\demo` 資料夾存在，就刪除
   - 然後重新建立一個空的 `C:\demo` 資料夾

6. **顯示完成訊息**


#### 補充說明
- **`@echo off`**：避免在執行批次檔時顯示每一行命令，讓畫面更乾淨。
- **`rmdir /s /q`**：強制刪除資料夾，包括底下所有檔案與子資料夾。
- **`call`**：確保在執行虛擬環境啟動腳本後，能繼續執行後續命令。
- **`start spyder`**：使用內建的 `start` 指令在新視窗中啟動 Spyder。
- **`if exist` / `mkdir`**：用來確認是否需要刪除/建立資料夾，確保環境乾淨。

這份批次檔對於需要在 Ansys 環境下進行 Python 自動化或模擬開發的使用者來說非常實用，可以快速建立乾淨且一致的開發環境。

