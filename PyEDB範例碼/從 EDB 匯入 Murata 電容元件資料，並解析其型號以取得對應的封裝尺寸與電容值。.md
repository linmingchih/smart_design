從 EDB 匯入 Murata 電容元件資料，並解析其型號以取得對應的封裝尺寸與電容值。
---

協助工程師在使用 Ansys AEDT 進行 PCB 模擬與設計時，自動解析 Murata 元件型號，取得對應的 EIA 封裝尺寸與實際電容值，提升資料準備的效率與準確性。

### 功能

* 使用 AEDT 提供的 EDB 介面取得元件庫資料。
* 對 Murata 電容型號（如 GRM 系列）進行解析。
* 自動轉換出 EIA 標準封裝尺寸（如 0603、0402 等）。
* 自動解析電容值並換算為對應單位（pF、nF、µF）。

### 流程架構

1. 透過 Ansys AEDT 的 API 匯入元件庫資料。
2. 使用正規表示式拆解 Murata 的型號結構，擷取封裝尺寸與電容編碼。
3. 根據 Murata 的尺寸代碼對應表轉換為標準 EIA 封裝尺寸。
4. 根據電容值格式判斷是『數字 + R + 數字』或『三位數』格式，並換算為實際容量值。
5. 將解析結果以標準單位格式化顯示。
6. 批次處理 Murata GRM18 系列的所有電容元件並輸出解析結果。

### 補充說明

* `Edb()` 是 Ansys AEDT 的一個介面類別，用於讀取與操作電路板設計資料庫。
* `re.search` 與 `re.findall` 是 Python 正規表示式的函式，用來從字串中擷取符合特定模式的資料。
* 封裝尺寸對應表（`eia_map`）是根據 Murata 命名規則手動對照出來的。
* 電容值的解析邏輯涵蓋了 Murata 常見的標示方式，包含帶有 `R`（代表小數點）以及傳統的三碼科學記號格式。

### 範例程式

```python
# 從 Ansys AEDT 匯入元件資料
from ansys.aedt.core import Hfss, Hfss3dLayout, Edb

# 初始化 AEDT 的資料庫介面
edb = Edb()
comp_lib = edb.components.get_vendor_libraries()

# 定義 Murata 型號解析函式
import re

def parse_murata_with_eia(part_number: str):
    m_dim2 = re.search(r'^[A-Za-z]{1,3}(\d{2})', part_number)
    if not m_dim2:
        raise ValueError(f"無法從型號『{part_number}』中擷取尺寸代碼前兩位。")
    dim_code = m_dim2.group(1)
    idx_after_dim2 = m_dim2.end()

    eia_map = {
        "03": "0201", "05": "0202", "08": "0303", "11": "0504",
        "15": "0402", "18": "0603", "21": "0805", "22": "1111",
        "31": "1206", "32": "1210", "42": "1808", "43": "1812",
        "52": "2211", "55": "2220",
    }
    eia_size = eia_map.get(dim_code, f"Unknown({dim_code})")

    tail = part_number[idx_after_dim2:]
    matches = re.findall(r'\d*R\d+|\d{3}', tail)
    if not matches:
        raise ValueError(f"無法從型號『{part_number}』中擷取電容值編碼。")
    cap_code = matches[-1]

    if 'R' in cap_code:
        num_str = '0.' + cap_code[1:] if cap_code.startswith('R') else cap_code.replace('R', '.')
        pf_value = float(num_str)
    else:
        mantissa = int(cap_code[:2])
        exponent = int(cap_code[2])
        pf_value = mantissa * (10 ** exponent)

    if pf_value >= 1_000_000:
        uf = pf_value / 1_000_000
        cap_str = f"{uf:.3f}".rstrip('0').rstrip('.') + " µF"
    elif pf_value >= 1_000:
        nf = pf_value / 1_000
        cap_str = f"{nf:.3f}".rstrip('0').rstrip('.') + " nF"
    else:
        cap_str = f"{pf_value:.3f}".rstrip('0').rstrip('.') + " pF"

    return eia_size, cap_str

# 批次處理 Murata GRM18 系列
data = {}
for name, model in comp_lib.capacitors["Murata"]['GRM18'].items():
    print(name)
    print(parse_murata_with_eia(name))
```

![2025-06-01_11-00-40](/assets/2025-06-01_11-00-40.png)

### 附註：PyAEDT Extras 功能完整指南

說明 PyAEDT 支援的 extras 選項及其功能與依賴套件，並提供使用與安裝建議。

#### 1. 什麼是 extras？

在 Python 套件開發中，開發者可以在 `setup.cfg` 或 `pyproject.toml` 中定義 "extras\_require" 區塊，讓使用者在安裝時透過 `pip install` 搭配中括號 `[]` 指定要安裝的額外功能套件。例如：

```bash
pip install pyaedt[graphics]
```

這樣的語法會除了安裝基本的 `pyaedt` 外，還額外安裝 `graphics` 模組所需的相關 Python 套件。


#### 2. 支援的 PyAEDT Extras 一覽

PyAEDT 官方在 `setup.cfg` 中定義了以下三種 extras：

##### 2.1 `graphics`

用於啟用圖形視覺化功能，例如場分佈的 3D 視覺化、圖片匯出、GIF 動畫等。

**額外安裝的套件：**

| 套件名稱              | 功能描述              |
| ----------------- | ----------------- |
| `pyvista>=0.32.0` | 基於 VTK 的 3D 視覺化套件 |
| `imageio`         | 圖片與動畫讀寫（可輸出 GIF）  |
| `matplotlib`      | 常用的 2D/3D 繪圖工具    |
| `numpy`           | 數值運算與矩陣處理（常見依賴）   |

安裝方式：

```bash
pip install "pyaedt[graphics]"
```


##### 2.2 `ipc2581`

用於支援將設計匯出成 IPC-2581 格式的 XML 檔案。

**額外安裝的套件：**

| 套件名稱                | 功能描述                      |
| ------------------- | ------------------------- |
| `lxml>=4.9.1`       | 高效能 XML 處理函式庫（支援 XPath 等） |
| `defusedxml>=0.7.1` | XML 安全防護（避免 XXE 等攻擊）      |

安裝方式：

```bash
pip install "pyaedt[ipc2581]"
```


##### 2.3 `full`

同時安裝 `graphics` 與 `ipc2581` 所需的所有依賴，是最完整的安裝選項。

**額外安裝的套件：**

| 套件名稱                | 來源（含於哪些 extras） |
| ------------------- | --------------- |
| `pyvista>=0.32.0`   | graphics、full   |
| `imageio`           | graphics、full   |
| `matplotlib`        | graphics、full   |
| `numpy`             | graphics、full   |
| `lxml>=4.9.1`       | ipc2581、full    |
| `defusedxml>=0.7.1` | ipc2581、full    |

安裝方式：

```bash
pip install "pyaedt[full]"
```


#### 3. 使用建議

| 使用情境             | 建議 extras                       |
| ---------------- | ------------------------------- |
| 僅需控制 AEDT 模型與分析  | 無需 extras（`pip install pyaedt`） |
| 需要匯出場分佈圖、動畫      | `graphics`                      |
| 需要匯出 IPC-2581 格式 | `ipc2581`                       |
| 通通都想支援           | `full`                          |


#### 4. 寫入 requirements.txt

若要用於團隊或伺服器統一安裝環境，可在 `requirements.txt` 中加入：

```text
pyaedt[full]
```

或根據需求選擇 `pyaedt[graphics]` 或 `pyaedt[ipc2581]`。


#### 5. 小結

PyAEDT 支援的 extras 機制，讓使用者可以依照實際功能需求安裝對應的依賴套件，不僅提高彈性，也能減少不必要的套件安裝。建議在開發環境時明確指定需求，便於管理。

如需更多細節，歡迎參考官方 GitHub：
[https://github.com/ansys/pyaedt](https://github.com/ansys/pyaedt)

