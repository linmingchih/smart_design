將Primitives轉成Pins並合成Components
---

這段程式碼的目的是將特定層（例如 top 層）上的 primitive 幾何結構，轉換成可識別的 pins（焊墊），再依照 pins 的座標位置劃分成三個區塊，並為每個區塊建立一個獨立的元件（component），最後儲存為新的 AEDB 檔案。

### 功能

* 匯入並載入 AEDB 專案檔案。
* 從指定圖層擷取 primitive，並轉換成 vias/pins。
* 根據座標位置（x, y）將 pins 分為三群。
* 將每一群 pins 建立為一個 component。
* 儲存處理後的結果為新的 AEDB 檔案。

### 流程架構

1. 開啟指定路徑的 AEDB 專案。
2. 從 top 層收集所有 primitive，轉換成 vias。
3. 遍歷所有轉換後的 pin，根據 x, y 座標進行分類：

   * `x < x0` 為 die1
   * `x >= x0` 且 `y > y0` 為 die2
   * 其他為 die3
4. 各群 pins 分別建立為 component：U1、U2、U3
5. 儲存新的 AEDB 專案。

### 補充說明

* `pyedb` 是 Ansys 提供的 Python API，用於操作 AEDB 資料。
* `ConvertPrimitivestoVias` 是內部 API 方法，將幾何物件轉換成實體焊盤（vias/pins）。第二個參數代表是否自動命名。
* `edb.padstacks.instances` 可存取目前專案中所有焊盤實體及其座標位置。
* `create_component_from_pins` 可從一組 pins 建立成一個元件（component），常用於 die 自動辨識或模擬模型建立。
* 使用 `List[Primitive]()` 是因為內部 API 需傳入 .NET 的 List 類型。

### 範例程式

```python
from pyedb import Edb
from System.Collections.Generic import List

# 載入 AEDB 專案
edb_path = r"D:\demo\ic.aedb"
edb = Edb(edb_path, version='2024.1')

# 準備 primitive list
Primitive = edb.core.Cell.Primitive.Primitive
die1_primitive_list = List[Primitive]()

# 從 top 層擷取所有 primitive 加入 list
for prim in [p.primitive_object for p in edb.modeler.primitives_by_layer['top']]:
    die1_primitive_list.Add(prim)

# 將 primitive 轉換成 pins
edb.layout._edb_object.ConvertPrimitivestoVias(die1_primitive_list, True)

# 初始化分類用 lists
die1 = []
die2 = []
die3 = []

# 分割基準座標
x0 = -0.0188
y0 = 0.0115

# 依據 pins 座標分類
for pin in edb.padstacks.instances.values():
    x, y = pin.position
    if x < x0:
        die1.append(pin)
    else:
        if y > y0:
            die2.append(pin)
        else:
            die3.append(pin)

# 建立三個 component
edb.components.create_component_from_pins(die1 , 'U1', 'top')
edb.components.create_component_from_pins(die2 , 'U2', 'top')
edb.components.create_component_from_pins(die3 , 'U3', 'top')

# 儲存成新專案
edb.save_edb_as('d:/demo/finished.aedb')
```

![](/assets/2025-10-21_21-19-58.png)