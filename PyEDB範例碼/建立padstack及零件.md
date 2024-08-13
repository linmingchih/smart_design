建立padstack及零件
---
這段代碼是使用 `pyedb` 和 `pyaedt` 來操作 AEDT 的 EDB 文件和 HFSS 3D Layout 的模型。這裡有幾個重點功能： 
1. **讀取 EDB 文件** ：使用 `Edb` 類別來加載 `d:/demo4/a40.aedb` 文件，並指定版本為 `2024.1`。
 
2. **在不同層上創建矩形和導線** ： 
  - 首先迭代所有層，跳過名稱為 "layer3" 的層，然後在類型為 `signal` 的層上創建矩形。
 
  - 創建兩個導線 (trace)，一個名稱為 `sp`，一個為 `sn`，並放置在 "layer3" 上。
 
3. **創建差分波端口** ：在 `sp` 和 `sn` 之間創建一個差分波端口，這在差分信號分析中是常見的。
 
4. **創建 Padstack** ：定義一個新的 `mypadstack`，並將其放置在不同的位置 (根據 `padstack_info` 列表)，然後將這些 padstack 組合為一個元件 "U1"。
 
5. **設置焊球和端口** ：對 "U1" 元件設置焊球大小，並創建端口。
 
6. **保存 EDB 文件** ：將修改後的 EDB 文件另存為 `d:/demo4/a81.aedb`。
 
7. **打開 HFSS 3D Layout** ：使用 `Hfss3dLayout` 類別來打開剛剛保存的 EDB 文件，以便進一步分析。

這段代碼示範了如何在不同的層上創建導線和元件，並將它們組合成一個可以在 HFSS 中進行模擬的設計。整體流程展示了如何利用 Python 脚本來自動化電子設計過程中的許多步驟。
```python
from pyedb import Edb
from pyaedt import Hfss3dLayout
edb = Edb('d:/demo4/a40.aedb', edbversion='2024.1')

for layer_name, layer in edb.stackup.stackup_layers.items():
    if layer_name == 'layer3':
        continue
    
    if layer.type == 'signal':
        rect = edb.modeler.create_rectangle(layer.name, 'gnd', (0e-3, -1e-3), (5e-3, 1e-3))

sp = edb.modeler.create_trace([(2e-3, 0e-3), (2e-3, 1e-3)],
                              layer_name='layer3',
                              width = '0.4mm',
                              net_name='sp',
                              end_cap_style='Flat')

sn = edb.modeler.create_trace([(3e-3, 0e-3), (3e-3, 1e-3)],
                              layer_name='layer3',
                              width = '0.4mm',
                              net_name='sn',
                              end_cap_style='Flat')

edb.core_hfss.create_differential_wave_port(sp, (2e-3, 1e-3), sn, (3e-3, 1e-3), horizontal_extent_factor=2)

edb.padstacks.create_padstack('mypadstack',                              
                              startlayer='layer1', 
                              endlayer='layer4',)

padstack_info = [(1e-3, 0, 'gnd'),
                 (2e-3, 0, 'sp'),
                 (3e-3, 0, 'sn'),
                 (4e-3, 0, 'gnd')]

pins = []
for x, y, net in padstack_info:
    p = edb.padstacks.place_padstack((x, y), 'mypadstack', net_name=net, is_pin=True)
    pins.append(p)

comp = edb.components.create_component_from_pins(pins, 'U1', 'layer1')

edb.core_components.set_solder_ball('U1', '0.24mm', '0.24mm')
edb.core_components.create_port_on_component('U1', ['sp', 'sn'])

edb_path = 'd:/demo4/a81.aedb'
edb.save_as(edb_path)

hfss = Hfss3dLayout(edb_path, specified_version='2024.1')
```

![2024-08-13_14-11-30](/assets/2024-08-13_14-11-30.png)