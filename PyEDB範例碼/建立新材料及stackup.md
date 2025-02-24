建立新材料及stackup
---

這段程式碼的主要用途是通過 `pyedb` 庫來建立和配置一個電磁數據庫 (EDB) 專案，設定其中的材料屬性以及堆疊結構的層次，最後將該設計保存為一個 `.aedb` 文件。以下是用途的綱要解釋： 
1. **初始化 EDB 專案** ： 
  - 使用 `pyedb` 庫中的 `Edb` 類來創建一個新的 EDB 物件，指定使用的 ANSYS 版本（2024.1）。
 
2. **設定材料屬性** ： 
  - 使用 `material_info` 字典來定義不同材料的屬性，包括導體 (`conductor`) 和介質 (`ds`)。
 
  - 透過遍歷 `material_info` 字典，將這些材料屬性添加到 EDB 專案中。
 
3. **配置層疊結構** ： 
  - 使用 `layers_info` 字典來定義電路板的層疊結構，包括信號層 (`signal`) 和介電層 (`dielectric`)。
 
  - 透過遍歷 `layers_info` 字典，為每一層指定其厚度、材料、蝕刻因子（對信號層）、粗糙度模型等屬性，並將這些層添加到 EDB 中。
 
4. **保存專案並關閉** ： 
  - 將配置完成的 EDB 專案保存到指定路徑（如 `d:/demo4/a40.aedb`）。

  - 最後關閉 EDB 專案以釋放資源。

這段程式碼的用途在於自動化處理 PCB 設計過程中的材料屬性和層疊結構配置，並將其保存為 EDB 文件以便後續的模擬和分析。


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



edb.save_as('d:/demo4/a40.aedb')
edb.close_edb()


```

![2024-08-13_12-11-48](/assets/2024-08-13_12-11-48.png)