PyEDB Workshop Labs
---
>:link: **範例edb下載**
[example_edb.aedb](/assets/example_edb.aedb.zip)

### 線上資源
[PyEDB官方網站](https://edb.docs.pyansys.com/version/stable/)

[AEDT自動化臉書社群](https://www.facebook.com/groups/304721550536923)

### Lab 0. 開發環境安裝  

在Windows開啟Command視窗(不是PowerShell視窗)並將下面程式碼一次複製貼上完成開發環境安裝。這個程序首先檢查並移除 C:\demo 目錄，然後重新建立一個新的 C:\demo 資料夾。接著，它使用指定的 Python 執行檔創建一個虛擬環境，進入該環境後啟動虛擬環境並安裝 pyaedt(含pyedb)、matplotlib 和 spyder 等 Python 套件。完成後，程序會回傳「安裝完成」訊息，表示所需環境和套件已設置成功，並可開始使用。
```bash
REM 檢查並移除 C:\demo 資料夾
if exist C:\demo (
    rmdir /s /q C:\demo
)

REM 檢查並移除 C:\myvenv 資料夾
if exist C:\myvenv (
    rmdir /s /q C:\myvenv
)

REM 建立新的 C:\demo 資料夾
mkdir C:\demo

REM 創建虛擬環境
"C:\Program Files\AnsysEM\v241\Win64\commonfiles\CPython\3_10\winx64\Release\python\python.exe" -m venv C:\myvenv

REM 進入虛擬環境並啟動
cd /d C:\myvenv\Scripts
call activate

REM 安裝需要的 Python 套件
pip install pyaedt
pip install matplotlib
pip install spyder

REM 啟動 Spyder
spyder
```


### Lab 1. 以阻值分類所有電阻
```python
from collections import defaultdict
from pyedb import Edb

edb = Edb("C:\demo\example_edb.aedb", edbversion='2024.1')
resistors = edb.components.resistors

table = defaultdict(list)
for name, obj in resistors.items():
    table[obj.value].append(name)
```
![2024-10-11_13-21-16](/assets/2024-10-11_13-21-16.png)

#### 補充說明
`defaultdict` 是 Python `collections` 模組中的一個容器，類似於字典（`dict`），但有個特殊之處：當查詢的鍵不存在時，它會自動生成一個預設值。使用 `defaultdict` 可以讓我們避免顯式檢查鍵是否存在，大幅簡化程式碼。不用 `defaultdict` 時，我們必須手動檢查鍵是否已存在，並初始化它，像是：

```python
table = {}
for name, obj in resistors.items():
    if obj.value not in table:
        table[obj.value] = []
    table[obj.value].append(name)
```
這樣的寫法較冗長，且每次都要進行存在性檢查。而使用 `defaultdict`，可以這樣簡化：

```python
from collections import defaultdict

table = defaultdict(list)
for name, obj in resistors.items():
    table[obj.value].append(name)
```


### Lab 2. 找出V3P3_S5上的去耦合電容名稱及電容值
```python
from pyedb import Edb

edb = Edb("C:\demo\example_edb.aedb", edbversion='2024.1')

group1 = edb.components.get_components_from_nets('V3P3_S5')
group2 = edb.components.get_components_from_nets('GND')

decaps = []
for name in set(group1) & set(group2):
    obj = edb.components.get_component_by_name(name)
    if obj.type == 'Capacitor':
        decaps.append((name, obj.value))
```

![2024-10-11_13-29-51](/assets/2024-10-11_13-29-51.png)

#### 補充說明
`set` 是 Python 中的一種內建資料結構，類似於數學中的集合（set），用來儲存不重複的元素，且元素的順序不固定。`set` 的主要特性是每個元素都是唯一的，因此在進行大量資料操作時，`set` 特別適合用來去除重複項目和進行集合運算。創建 `set` 可以使用大括號 `{}` 或是 `set()` 函數，如下所示：

```python
# 使用大括號
my_set = {1, 2, 3, 4}

# 使用 set() 函數，特別是當從其他可迭代對象（如列表）創建 set 時
my_set = set([1, 2, 2, 3, 4])  # 自動去除重複的 2
```
`set` 支援常見的集合運算，像是交集（`&`）、聯集（`|`）、差集（`-`）與對稱差（`^`），這些運算能快速比較和處理不同集合間的關係：

```python
a = {1, 2, 3}
b = {3, 4, 5}

# 交集：{3}
intersection = a & b

# 聯集：{1, 2, 3, 4, 5}
union = a | b

# 差集：{1, 2}
difference = a - b
```
使用 `set` 的好處在於它能快速檢查元素是否存在（時間複雜度為 O(1)），以及進行高效的集合運算。這使得 `set` 在處理大量資料和去重等情境中非常實用。



### Lab 3. 建立新材料並設定疊構
```python
from pyedb import Edb

edb = Edb(edbversion='2024.1')

material_info = {('metal1', 'conductor'): 5e8,
                 ('metal2', 'conductor'): 5e8,
                 ('epoxy1', 'ds'):(4, 0.02, 1),
                 ('epoxy2', 'ds'):(3.8, 0.015, 1)}


layers_info = {('layer1', 'signal'):('0.05mm', 'metal1', 1.6, '0.6um', '3.1'),
               ('dielectric12', 'dielectric'):('0.28mm', 'epoxy1'),
               ('layer2', 'signal'):('0.05mm', 'metal2', 1.7, '0.8um', '3.4'),
               ('dielectric23', 'dielectric'):('0.43mm', 'epoxy2'),
               ('layer3', 'signal'):('0.05mm', 'metal2', 1.7, '0.8um', '3.4'),
               ('dielectric34', 'dielectric'):('0.28mm', 'epoxy1'),
               ('layer4', 'signal'):('0.05mm', 'metal1', 1.6, '0.6um', '3.1')}


for (name, _type), prop in material_info.items():
    if _type == 'conductor':
        conductivity = prop
        edb.materials.add_conductor_material(name, conductivity)
    elif _type == 'ds':
        permittivity, loss_tangent, test_frequency = prop
        edb.materials.add_djordjevicsarkar_dielectric(name, permittivity, loss_tangent, test_frequency)

for (name, _type), prop in layers_info.items():
    if _type == 'signal':
        thickness, material, etch_factor, radius, ratio = prop
        layer = edb.stackup.add_layer(name, 
                                      layer_type=_type, 
                                      material=material, 
                                      thickness=thickness,
                                      enable_roughness=True,
                                      method='add_on_bottom')
        layer.etch_factor=etch_factor
        layer.assign_roughness_model("huray", radius, ratio, apply_on_surface="all")
    
    elif _type == 'dielectric':
        thickness, material = prop
        edb.stackup.add_layer(name, 
                              layer_type=_type, 
                              material=material, 
                              thickness=thickness,
                              method='add_on_bottom')



edb.save_as('c:/demo/lab3.aedb')
edb.stackup.export_stackup('c:/demo/lab3.xml')
edb.close_edb()
```
![2024-10-11_13-46-39](/assets/2024-10-11_13-46-39.png)

### Lab 4. 建立差分對結構並設置WavePort
```python
from pyedb import Edb
from functools import partial

edb = Edb(edbversion='2024.1')
edb.core_stackup.load('c:/demo/lab3.xml')

create_trace = partial(edb.modeler.create_trace, layer_name='layer2', width='1mm', start_cap_style='Flat', end_cap_style='Flat')
tp = create_trace([('0mm','-1mm'), ('10mm', '-1mm')], net_name='pos')
tn = create_trace([('0mm','1mm'), ('10mm', '1mm')], net_name='neg')

edb.modeler.create_rectangle('layer1', 'GND', ('0mm', '-5mm'), ('10mm', '5mm'))
edb.modeler.create_rectangle('layer3', 'GND', ('0mm', '-5mm'), ('10mm', '5mm'))

edb.core_hfss.create_differential_wave_port(tp, ('0mm', '-1mm'), tn, ('0mm', '1mm'), horizontal_extent_factor=2)
edb.core_hfss.create_differential_wave_port(tp, ('10mm', '-1mm'), tn, ('10mm', '1mm'), horizontal_extent_factor=2)

edb.save_as('c:/demo/lab4.aedb')
edb.close_edb()
```
![2024-10-11_14-15-21](/assets/2024-10-11_14-15-21.png)

#### 補充說明

`partial` 是 Python `functools` 模組中的一個高階函數，用來「部分應用」某個函數的參數。它的作用是預先設定某些參數的值，然後返回一個新的函數，這個新函數會以預設的參數進行呼叫。`partial` 對於需要重複使用相同參數但稍微改變部分輸入的情況特別有用。在你的例子中，`create_trace` 使用了 `partial` 函數來預先設置一些固定參數，如 `layer_name='layer2'`、`width='1mm'`、`start_cap_style='Flat'` 及 `end_cap_style='Flat'`。這樣可以避免每次呼叫 `edb.modeler.create_trace` 時都重複傳入這些參數，提升程式的可讀性和維護性。

```python
from functools import partial

create_trace = partial(
    edb.modeler.create_trace, 
    layer_name='layer2', 
    width='1mm', 
    start_cap_style='Flat', 
    end_cap_style='Flat'
)
```
這行代碼會返回一個新的 `create_trace` 函數，它自動帶有指定的參數，然後你只需要傳入剩下的參數（在這裡是點座標和網路名稱）：

```python
tp = create_trace([('0mm','-1mm'), ('10mm', '-1mm')], net_name='pos')
tn = create_trace([('0mm','1mm'), ('10mm', '1mm')], net_name='neg')
```
在這兩個例子中，你只需傳入座標與網路名稱 `net_name`，其他參數已經由 `partial` 預設好了。這樣做的好處是大幅減少了重複代碼，使程式更簡潔。



### Lab 5. 設置 3D Layout SI 模擬
```python
from pyedb import Edb
from ansys.aedt.core import Hfss3dLayout
edb = Edb('c:/demo/lab4.aedb', edbversion='2024.1')
setup = edb.core_hfss.configure_hfss_analysis_setup()

sim_setup = edb.new_simulation_configuration()
sim_setup.solver_type = sim_setup.SOLVER_TYPE.Hfss3dLayout
sim_setup.ac_settings.start_freq = "0GHz"
sim_setup.ac_settings.stop_freq = "5GHz"
sim_setup.ac_settings.step_freq = "0.1GHz"
edb.build_simulation_project(sim_setup)
edb.save_edb_as('c:/demo/lab5.aedb')
edb.close_edb()

hfss = Hfss3dLayout('c:/demo/lab5.aedb', version="2024.1")
hfss.set_export_touchstone(True, 'c:/demo')
hfss.analyze()
hfss.close_desktop()
```
![2024-10-11_14-46-15](/assets/2024-10-11_14-46-15.png)

### Lab 6. 設置Siwave SYZ SI模擬
```python
controller_name = 'U2A5'
dram_name = 'U1B5'
nets = [f'M_DQ<{i}>' for i in range(8)]

import pyaedt
from pyaedt import Hfss3dLayout
from pyedb import Edb

edb = Edb('c:/demo/example_edb.aedb', edbversion='2024.1')

controller = edb.components[controller_name]
gnd_pins = [j for i, j in controller.pins.items() if j.net.name=='GND']
pg_gnd = edb.core_components.create_pingroup_from_pins(gnd_pins)
edb.core_components.create_port_on_component(controller_name, nets, reference_net='GND')

dram = edb.components[dram_name]
gnd_pins = [j for i, j in dram.pins.items() if j.net.name=='GND']
dram_gnd = edb.core_components.create_pingroup_from_pins(gnd_pins)
edb.core_components.create_port_on_component(dram_name, nets, reference_net='GND')

setup1 = edb.create_siwave_syz_setup()

setup1.add_frequency_sweep()
edb.save_as('c:/demo/lab6.aedb')
edb.close_edb()

hfss = Hfss3dLayout(specified_version='2024.1', 
                    non_graphical=True, 
                    projectname='c:/demo/lab6.aedb', 
                    remove_lock=True)
hfss.analyze()
hfss.export_touchstone()
hfss.close_project()
```

![2024-10-11_15-00-14](/assets/2024-10-11_15-00-14.png)
