如何用 ChatGPT Codex 協助開發 PyAEDT 腳本
---

在日常開發自動化模擬流程的過程中，我經常需要針對 PyAEDT 增加客製化功能，例如建立特定幾何結構、指定邊界條件或是批次導出模擬結果。然而由於 PyAEDT 是一個龐大的工程庫，其模組之間結構複雜、版本差異大，單靠記憶與搜尋文件常常效率不彰。

最近我嘗試了 **ChatGPT Codex**，並將我 Fork 的 PyAEDT 連結進去，實際驗證 Codex 能否協助我快速理解、擴充這個專案。這篇文章是我個人的心得紀錄，分享這個工具在工程開發上帶來的幫助與驚喜。


### 🔗 Codex 與一般 AI 程式生成工具有何不同？

傳統的 ChatGPT 程式生成功能雖然可以寫出段落整齊、語法正確的程式碼，但它通常是「根據語意推測」產生通用邏輯，並不了解您實際使用的程式庫。

而 Codex 的關鍵優勢在於：

> **它可以連接至您 GitHub 上的實際代碼庫，實際掃描與理解您的專案內容，再根據上下文產生程式碼。**

這樣的能力，對像 PyAEDT 這種大型 Python 工程庫來說，簡直是一位能讀懂程式脈絡的助手。


### ⚙️ 我是這樣操作的：

1. **Fork 一份 PyAEDT 到我的 GitHub 個人帳號**
2. **啟用 Codex 並連結到這個 repo**
3. **輸入自然語言 Prompt，例如：**

   > 為 `Hfss` 類別新增一個函式，可建立一個 200mil 長、10mil 寬的傳輸線，板厚 15mil，設定 wave port，掃描頻率 DC\~10GHz，並匯出 S2P。




### Codex 的行為讓我非常驚艷：

* 它會在右側 console 顯示「正在讀取 `hfss.py`、`modeler.py`、`boundary.py` 等檔案」
* 自動補齊正確的 API，例如 `hfss.modeler.create_rectangle()`、`hfss.create_wave_port()`、`hfss.export_touchstone()`
* 在輸出程式碼時，完整考慮到現有架構與變數命名一致性
* 不會混用過時版本的 API（這點在 PyAEDT 多版本開發中非常重要）



### 🧠 Codex 是怎麼做到的？

它並不只是靜態補齊語法，而是：

* 掃描整個 repo 的 `__init__.py` 和模組路徑，了解 class 與函式定義
* 讀懂各模組之間的引用關係（import 結構）
* 根據歷史代碼風格，自動產生一致的命名與邏輯流程

也就是說，它能「看懂這個專案」，而不只是「看懂你剛輸入的一句話」。



### 🧪 使用情境舉例：PyAEDT + Codex

我讓 Codex 幫我快速生成以下流程的程式碼：

1. 建立傳輸線幾何
2. 設定材料與邊界
3. 指定 wave port
4. 設定頻率掃描 Setup（DC\~10GHz）
5. 執行分析並匯出 S-Parameter

生成程式碼不但一次成功執行，還完全符合 PyAEDT 的架構設計原則。甚至 Codex 還會根據我專案中現有的 `analyze()` 調用邏輯自動補上適當註解與 log 行為。

### 生成代碼
```python
from pyaedt import Desktop, Hfss

# 開啟 AEDT
Desktop(specified_version="2024.1", new_desktop_session=True)

# 建立 HFSS 專案
hfss = Hfss(projectname="TxLine", designname="TransmissionLine",
            solution_type="DrivenModal", new_desktop_session=False)

# 使用 mil 為模型單位
hfss.modeler.model_units = "mil"

# 建立基板 (長 200 mil、寬 50 mil、厚 15 mil)
sub = hfss.modeler.create_box([0, -25, -15], [200, 50, 15],
                              name="Substrate", material="FR4_epoxy")

# 建立地平面
gnd = hfss.modeler.create_box([0, -25, -15], [200, 50, 1],
                              name="GND", material="copper")

# 建立傳輸線導體 (寬 10 mil、長 200 mil、厚 1 mil)
trace = hfss.modeler.create_box([0, -5, 0], [200, 10, 1],
                                name="Line", material="copper")

# 在兩端建立波導埠
port1 = hfss.wave_port(assignment=gnd.name, reference=trace.name,
                       create_port_sheet=True, integration_line=hfss.AxisDir.XNeg,
                       is_microstrip=True, name="Port1")
port2 = hfss.wave_port(assignment=gnd.name, reference=trace.name,
                       create_port_sheet=True, integration_line=hfss.AxisDir.XPos,
                       is_microstrip=True, name="Port2")

# 建立 Setup 並設定 DC~10GHz 的掃頻
setup = hfss.create_setup("Setup1", Frequency="1GHz")
hfss.create_linear_count_sweep(setup.name, "GHz",
                               start_frequency=0, stop_frequency=10,
                               num_of_freq_points=201, sweep_type="Interpolating")

# 讓求解後自動輸出 Touchstone
hfss.export_touchstone_on_completion(True, output_dir=hfss.working_directory)

# 執行求解
hfss.analyze_setup(setup.name)

# 關閉 AEDT
hfss.release_desktop()


```

### 💡 心得總結

> 「Codex 不是只是幫我寫程式，而是像一位真正理解專案背景的開發同事。」

它能：

* 深入理解 GitHub 專案結構
* 在代碼上下文中推敲 API 寫法
* 降低出錯機率、避免版本錯誤
* 加快自動化開發的速度與信心

對於我這種經常進行工具鏈客製化、自動化模擬腳本開發的工程師來說，Codex 不僅是輔助工具，更是一個可靠的開發拍檔。



### 📌 建議與應用場景

* 想快速上手大型開源專案（如 PyAEDT、PyFluent、PyMAPDL 等）
* 要在既有架構中加功能而非重寫
* 想提升團隊開發速度與代碼一致性

推薦給所有正在處理大型 Python 專案、自動化工作流程的工程師，你會發現 Codex 是「值得信賴的 AI 夥伴」。
