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
aedb_path = 'd:/demo4/test27.aedb'

from pyedb import Edb

edb = Edb('d:/demo4/Galileo_G87173_204162.aedb', edbversion='2024.1')


for layer_name, layer in edb.stackup.stackup_layers.items():
    print('---' ,layer_name)
    print(layer.type)
    print(layer.thickness)
    print(layer.material)
    print(layer.etch_factor)
    print(layer.dielectric_fill)
    
    print(layer.roughness_enabled)
    print(layer.top_hallhuray_nodule_radius)
    print(layer.top_hallhuray_surface_ratio)
    print(layer.bottom_hallhuray_nodule_radius)
    print(layer.bottom_hallhuray_surface_ratio)    
    print(layer.side_hallhuray_nodule_radius)
    print(layer.side_hallhuray_surface_ratio)


for layer_name, layer in edb.stackup.stackup_layers.items():
    print('---' ,layer_name)
    print(layer.type)
    layer.thickness = 1e-5
    
    if layer.type == 'dielectric':
        layer.material = 'FR4_epoxy'
    
    elif layer.type == 'signal':
        layer.material = 'Aluminum'
        layer.dielectric_fill = 'FR4_epoxy'
        layer.etch_factor = 1.2    
        
        layer.roughness_enabled = True 
        layer.assign_roughness_model("huray", "0.6um", "3.1", apply_on_surface="all")
        

edb.save_as(aedb_path)
edb.close_edb()
```

![2024-08-13_10-21-19](/assets/2024-08-13_10-21-19.png)