**完整 GUI 工具專案架構範例生成請求**
---

請依以下規格，產生使用 **PyWebView + PyEDB/PyAEDT + uv + Git** 的完整 GUI 工具專案架構、所有必要的程式碼與檔案內容。

**一、 開發環境與核心架構**

  * **GUI 框架**: 使用 **PyWebView** (基於 HTML/CSS/JS)。
  * **後端 API 模擬**: 核心功能使用 **PyEDB / PyAEDT** 模擬。
  * **環境管理**: 專案使用 **uv** 進行環境與依賴管理。
  * **版本控制**: 專案結構需包含 **Git** 相關檔案。
  * **專案生命週期**:
      * 工具啟動時，若無已開啟專案，%TEMP% 自動建立一個臨時設計專案資料夾例如project1.vw，並允許使用者自訂名稱。project1.vw 內含 `project.json` 檔案，儲存所有 GUI 參數與設定。以及所有執行過程中產生的中間檔案與結果檔案。

      * 支援 **New / Open / Save / Save As** 行為。
      * **Save / Save As**: 將專案狀態（包括 GUI 輸入的參數）儲存到專案資料夾內的 `project.json` 檔案中。
      * **Open**: 選擇一個專案資料夾，載入其中的 `project.json` 內容到 GUI 介面。

**二、 專案目錄結構與必要檔案內容**

AI 必須產生以下所有目錄和檔案的內容，確保結構完整且檔案內容可用：

```
project_root/
    .git/                   <-- 初始化 Git 專案
    .venv/                  <-- uv 管理的虛擬環境 (不會被 Git 追蹤)
    src/
        __init__.py
        main.py             <-- PyWebView GUI 主程式
        project_manager.py  <-- 處理 New/Open/Save/Save As, project.json 讀寫, 專案路徑管理
        gui_backend.py      <-- 處理 PyWebView expose 的所有後端邏輯和非同步執行
        web/
            index.html      <-- GUI 主介面
            css/
                style.css   <-- 基礎樣式
            js/
                main.js     <-- 介面初始化、全域邏輯、通訊
                tab_preprocess.js <-- Preprocess Tab 邏輯
                tab_simulation.js <-- Simulation Tab 邏輯
                tab_postprocess.js <-- Postprocess Tab 邏輯
    scripts/
        preprocess.py       <-- 由後端執行 (subprocess.Popen)，讀取 project.json 執行 PyEDB/PyAEDT 模擬，並回傳 .aedb 路徑。
        simulation.py       <-- 由後端執行 (subprocess.Popen)，讀取 project.json 執行 PyAEDT 模擬，並回傳 result.json (S參數)。
    config.json             <-- 專案配置，包含版本號、作者等元數據
    pyproject.toml          <-- uv 配置，包含專案依賴
    .python-version         <-- 指定 Python 版本
    README.md
    README_zh-TW.md
    run.bat                 <-- 啟動腳本
```

**三、 GUI 佈局規格 (HTML/CSS/JS)**

GUI 採三段式佈局：Menu Bar / Tool Bar、Tab Pages、Message Window。

1.  **Menu Bar / Tool Bar (頂部)**

      * **File 菜單**:
          * New (新建臨時專案資料夾並清空介面)
          * Open (開啟現有專案目錄，載入 `project.json`)
          * Save (儲存至當前專案目錄的 `project.json`)
          * Save As (儲存專案目錄為新名稱)
          * Exit
      * **Option 菜單**:
          * Version: 彈出對話框 (Dialog)，顯示並允許使用者編輯 `config.json` 中的 `aedt_version` 和 `edb_version` 兩個欄位。
      * **Help 菜單**:
          * About: 顯示專案名稱、版本、作者、版權等資訊（從 `config.json` 讀取）。

2.  **Tab Pages (中央區域)**

      * 包含三個主要頁籤：**Preprocess**、**Simulation**、**Postprocess**。

      * 每個 Tab 內的邏輯和事件處理必須寫在**獨立的 `.js` 檔案中** (`tab_preprocess.js`, `tab_simulation.js`, `tab_postprocess.js`)。

      * **Preprocess 頁籤規格**:

          * **左側 Panel**: 讓使用者輸入傳輸線與介質參數：
              * `line_width` (預設: '10mil')
              * `line_thickness` (預設: '0.2mil')
              * `line_length` (預設: '100mil')
              * `dielectric_width` (預設: '50mil')
              * `dielectric_thickness` (預設: '1mil')
              * `dielectric_permittivity` (預設: '4')
              * `dielectric_loss_tangent` (預設: '0.01')
          * **主要 Panel**: 顯示座標系統，並**動態更新** Line 與 Dielectric 的XY二維形狀預覽。
          * **Apply 按鈕**:
            1.  將所有參數寫入 `project.json`。
            2.  呼叫 `gui_backend.py`，後者使用 `subprocess.Popen()` 執行 `scripts/preprocess.py`，並將 `project.json` 路徑作為參數傳入。
            3.  `preprocess.py` 執行模擬並將aedb路徑寫入 `project.json` 中的 `aedb_path` key。

      * **Simulation 頁籤規格**:

          * **頂部**: 顯示上一步驟產生的 `.aedb` 專案路徑。
          * **左側 Panel**: 讓使用者輸入模擬參數：
              * `simulation_type` (下拉選單: 'HFSS', 'SIwave')
              * `max_frequency` (預設: '10GHz')
          * **主要 Panel**: 顯示 3D 結構預覽（可動態旋轉視角，zoom in/out）。
          * **Apply 按鈕**:
            1.  將參數寫入 `project.json`。
            2.  呼叫 `gui_backend.py`，執行 `scripts/simulation.py` (傳入 `project.json` 路徑)。
            3.  `simulation.py` 執行模擬並回傳 S11 與 S21 隨頻率變化的資料於project.json中的 `result` key當中。 
    
      * **Postprocess 頁籤規格**:

          * **頂部**: 顯示 `.aedb` 專案路徑。
          * **左側 Panel**: 讓使用者切換 S 參數顯示模式 (單選按鈕/下拉選單)：`mag`, `db`, `phase`, `real`, `imag`。
          * **主要 Panel**: 顯示**動態圖表**（如使用 Chart.js 或 Plotly.js 模擬），可實現 **Zoom In/Out, Pan, Reset View** 等功能。圖表數據來自 `result.json`。

      * 根據以上建立project.json結構範例：當中提供完整資料欄位及mock數據。以作為後續腳本開發參考。

3.  **Message Window (底部)**

      * 全域共用，能即時顯示 Python 後端（包括 `preprocess.py` 和 `simulation.py`）腳本執行的**進度或日誌訊息**。
      * 訊息傳遞機制：**Python Thread + `pywebview.expose` 回呼**。
      * 需包含一個**清除按鈕**。
      * 每次切換專案 (New/Open) 時自動重置。

**四、 Python 腳本執行與非同步機制**

  * **腳本執行**: 所有 PyEDB/PyAEDT 相關腳本 (`preprocess.py`, `simulation.py`) 必須透過 Python 主程式中的 `subprocess.Popen()` 執行，以確保它們在獨立的進程中運行，避免阻塞 GUI。
  * **非同步通訊**: GUI (JS) 與後端 (Python) 之間的即時訊息傳遞，需使用：
    1.  Python 後端在**獨立的 Thread** 中處理耗時操作 (如呼叫 `Popen`)。
    2.  執行進程的標準輸出/錯誤 (Stdout/Stderr) 應被捕獲。
    3.  使用 `pywebview.api.log_message(message)` (或其他 exposed function) 將訊息**即時回傳**給前端 Message Window。

**五、 `run.bat` 啟動腳本要求**

AI 需產生完整的 `run.bat` 腳本，實現以下功能：

1.  **檢查 `uv`**: 檢查系統是否已安裝 `uv` (例如，檢查 `uv --version` 是否成功)。
2.  **自動安裝 `uv`**: 若未安裝，則自動下載並安裝 `uv`。
3.  **安裝 Python**: 讀取 `.python-version` 文件中指定的 Python 版本，並使用 `uv tool run python` (或等效的 uv 命令) 確保該版本 Python 環境存在。
4.  **建立環境**: 執行 `uv sync` 以建立/同步專案所需的虛擬環境 (`.venv/`) 和依賴。
5.  **啟動 GUI**: 以**隱藏 Console 視窗**的方式，啟動 `src/main.py` (即 PyWebView GUI)。

**六、 參數與通訊流程重點**

  * `config.json` 必須包含 `aedt_version`, `edb_version`, `project_name`, `version`, `author`, `copyright` 欄位。
  * `project.json` 必須能儲存 Preprocess 和 Simulation 頁籤的所有使用者輸入參數，以及腳本執行結果 (`.aedb_path`, `result_json_path`)。

請從 `config.json` 和 `pyproject.toml` 開始，依序生成所有檔案內容。