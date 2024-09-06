設定stackup
---

 Python 程式碼片段是使用 `pyedb` 模組來處理 ANSYS Electronics Desktop (AEDT) 的電子資料庫 (EDB) 文件。這個程式碼主要進行以下幾個操作： 

1. **導入 Edb 模組** ：從 `pyedb` 包中導入 `Edb` 類，這是處理 EDB 文件的核心類。
 
2. **打開 EDB 文件** ：使用 `Edb` 類實例化一個物件來打開特定路徑的 EDB 文件。您還指定了版本號，這對於確保與特定版本的 AEDT 的兼容性很重要。
 
3. **遍歷並打印層信息** ：遍歷 EDB 的堆疊層 (`stackup_layers`)，並打印出每層的詳細信息，包括層的名稱、類型、厚度、材料、蝕刻因子、介電填充等，還有與表面粗糙度模型相關的參數。這些信息對於理解和分析 PCB 布局和材料特性非常有用。
 
4. **修改層的屬性** ：在第二個循環中，根據層的類型（例如 'dielectric' 或 'signal'）來調整厚度、材料、介電填充等屬性。對於信號層，還啟用了表面粗糙度並指定了粗糙度模型 ("huray") 的特定參數，這對於模擬電氣性能有重要影響。
 
5. **儲存更改** ：將所有更改保存到新的 EDB 文件路徑中，然後關閉 EDB 文件以釋放資源。

此代碼片段是自動化 PCB 分析和修改的一個實用工具，能夠對電子堆疊的各個層進行詳細檢視和調整，幫助工程師優化設計和性能。



```python
import pyedb
from pyedb import Edb
assert pyedb.version == '0.23.0', f'version:{pyedb.version} is not "0.23.0"'



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


edb_path = 'd:/demo/example2.aedb'
edb.save_as(edb_path)
edb.close_edb()
```

![2024-08-13_10-21-19](/assets/2024-08-13_10-21-19.png)