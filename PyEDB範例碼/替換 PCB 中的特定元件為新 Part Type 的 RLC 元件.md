替換 PCB 中的特定元件為新 Part Type 的 RLC 元件
--- 

此段程式碼的主要目的是在現有的 EDB PCB 設計檔案中，將某一個指定的元件（例如電容 C3B17）移除後，使用相同的接腳與位置重新建立一個指定參數的新 RLC 元件，最後另存為新的設計檔案。

### 功能

* 載入既有的 PCB 設計資料（`.aedb`）。
* 讀取指定元件（C3B17）的資訊。
* 解散元件群組（Ungroup），準備進行替換。
* 使用相同的 pins、位置和參考名稱，建立一個新的電容元件。
* 將修改後的設計儲存為另一份檔案，避免覆蓋原始設計。

### 流程架構

1. 載入原始 PCB 設計（`pcb.aedb`）。
2. 從元件清單中選出指定元件 `C3B17`。
3. 取得該元件的：

   * 參考名稱（refdes）
   * 接腳資訊（pins）
   * 佈局層（placement layer）
   * 零件名稱（part name）
4. 解散原本的元件，使其不再為一個群組化的元件。
5. 建立一個新的元件，並指定為 RLC 電容，設定值為 1μF（1e-6 F）。
6. 另存為新的 PCB 設計檔（`pcb2.aedb`）。

### 補充說明

* `edb.components.components['C3B17']` 是從元件庫中抓取指定元件的方式。
* `Ungroup(True)` 是解除該元件與其他物件的關聯，使其可以被替換。
* `is_rlc=True` 表示這是個簡化的 RLC 元件，適合模擬用途。
* `create()` 方法可直接建立新的 RLC 元件，並掛載在相同位置與接腳上。

### 範例程式

```python
from pyedb import Edb

# 開啟既有的EDB專案，指定版本為2024.1
edb = Edb('d:/demo/pcb.aedb', version='2024.1')

# 取得元件C3B17的物件
component_to_change = edb.components.components['C3B17']

# 擷取原始元件的基本資訊
refdes = component_to_change.refdes
pins = list(component_to_change.pins.values())
layer = component_to_change.placement_layer
old_part_name = component_to_change.part_name

# 將原本的元件解除群組，準備取代
component_to_change.edbcomponent.Ungroup(True)

# 建立一個新的元件，使用相同的pins、參考名稱與層，指定為RLC元件並設定電容值
new_component = edb.components.create(
    pins, refdes, layer, 'new_part', is_rlc=True, c_value='1e-6')

# 儲存為新的EDB專案檔案
edb.save_edb_as('d:/demo/pcb2.aedb')
```
