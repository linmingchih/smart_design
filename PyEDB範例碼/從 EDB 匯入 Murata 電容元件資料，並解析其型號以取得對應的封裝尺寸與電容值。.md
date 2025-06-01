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