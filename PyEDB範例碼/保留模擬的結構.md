使用 PyEDB 精簡電路板設計：保留電源與地線相關物件
---

這段程式碼的目的是從一個完整的電路板設計檔中，保留與指定的電源與地線（例如 GND、V3P3\_S3）有關的物件，並刪除其他無關的連線與元件，最後另存為一個簡化版的檔案，方便進行後續的分析或模擬。

### 功能

* 讀取 EDB 檔案
* 保留指定 nets 的導線物件與過孔（vias）
* 移除未連接至指定 nets 的元件
* 儲存簡化後的設計檔案

### 流程架構

1. 使用 `Edb` 類別載入指定路徑的設計檔。
2. 定義要保留的電網名稱，例如 GND 和 V3P3\_S3。
3. 遍歷所有 nets，刪除不屬於指定 nets 的導線物件。
4. 遍歷所有過孔（vias），刪除其連接 net 不在指定列表中的過孔。
5. 遍歷所有元件（components），如果其連接的 nets 少於兩個與指定 nets 相交，則刪除該元件。
6. 儲存處理後的設計檔為新的檔案。

### 補充說明

* `Edb` 是 PyAEDT 提供的類別，用來操作 Ansys 的設計資料庫。
* `net.primitives` 表示該 net 下的所有導線、pad 等幾何物件。
* `via.net.name` 可取得過孔所屬的 net 名稱。
* 使用 `set` 做交集可以快速判斷元件是否同時連接多個指定 nets。

### 範例程式

```python
from pyaedt import Edb

# 設定原始檔案路徑
path = "D:/demo/pcb.brd"
edb = Edb(path, edbversion='2024.1')

# 要保留的 net 名稱清單
nets = ['GND', 'V3P3_S3']

# 刪除不屬於目標 nets 的導線物件
for net_name, net in edb.nets.nets.items():
    if net_name not in nets:
        for obj in net.primitives:
            obj.delete()

# 刪除不屬於目標 nets 的過孔
for via_name, via in edb.padstacks.vias.items():
    if via.net.name not in nets:
        via.delete()

# 刪除不屬於目標 nets 的元件
for component_name, component in edb.components.components.items():
    cmp_nets = [pin.net.name for pin_name, pin in component.pins.items()]
    if len(set(cmp_nets) & set(nets)) < 2:
        component.delete()

# 儲存簡化後的檔案
edb.save_edb_as('d:/demo/simple.aedb')
```

### 精簡之後結構

![2025-07-02_12-15-03](/assets/2025-07-02_12-15-03.jpg)