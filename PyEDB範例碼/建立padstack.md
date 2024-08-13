建立padstack
---
這段程式碼的主要用途是基於現有的 EDB 專案 (`a40.aedb`)，進一步添加一些幾何結構和 padstack，然後保存這些更改並使用它進行 HFSS 3D Layout 模擬。以下是每個部分的具體說明： 
1. **初始化 EDB 和載入專案** ： 
  - 使用 `pyedb` 中的 `Edb` 類來載入已經存在的 EDB 專案 (`a40.aedb`)，並指定使用 ANSYS 2024.1 版本。
 
2. **創建矩形結構** ： 
  - 迭代 EDB 中所有的堆疊層，如果該層是信號層 (`signal`)，則在該層上創建一個矩形。
 
  - 矩形的幾何尺寸由兩個頂點 `(0e-3, -1e-3)` 和 `(5e-3, 1e-3)` 定義，並且將這個矩形與網絡 `'gnd'` 相關聯。
 
3. **創建和放置 Padstack** ： 
  - 使用 `create_padstack` 函數創建一個新的 padstack，命名為 `'mypadstack'`，並定義它的起始層為 `'layer1'`，終止層為 `'layer4'`。
 
  - 定義一組 padstack 的位置和相關的網絡信息 (`padstack_info`)，其中每個 padstack 都有一組坐標 `(x, y)` 和一個對應的網絡名稱 (`net`)。
 
  - 使用 `place_padstack` 函數將這些 padstack 放置到對應的位置。
 
4. **保存修改後的 EDB 專案** ： 
  - 將修改後的 EDB 專案保存為新的文件 (`a59.aedb`)。
 
5. **初始化 HFSS 3D Layout** ： 
  - 使用 `pyaedt` 中的 `Hfss3dLayout` 類來載入剛剛保存的 EDB 專案 (`a59.aedb`)，以便進行即時觀察EDB內容正確與否。
  
```python
from pyedb import Edb
from pyaedt import Hfss3dLayout
edb = Edb('d:/demo4/a40.aedb', edbversion='2024.1')

for layer_name, layer in edb.stackup.stackup_layers.items():
    if layer.type == 'signal':
        rect = edb.modeler.create_rectangle(layer.name, 'gnd', (0e-3, -1e-3), (5e-3, 1e-3))

edb.padstacks.create_padstack('mypadstack',                              
                              startlayer='layer1', 
                              endlayer='layer4',)

padstack_info = [(1e-3, 0, 'gnd'),
                 (2e-3, 0, 'sp'),
                 (3e-3, 0, 'sn'),
                 (4e-3, 0, 'gnd')]
                 
for x, y, net in padstack_info:
    edb.padstacks.place_padstack((x, y), 'mypadstack', net_name=net)
    

edb_path = 'd:/demo4/a59.aedb'
edb.save_as(edb_path)

edb.close_edb()
hfss = Hfss3dLayout(edb_path, specified_version='2024.1')

```

![2024-08-13_13-15-25](/assets/2024-08-13_13-15-25.png)