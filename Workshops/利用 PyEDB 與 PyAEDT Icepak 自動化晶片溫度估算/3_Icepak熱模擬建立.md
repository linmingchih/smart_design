Icepak熱模擬建立
---

這段Python程式是用於自動化建立高精度晶片封裝的熱分析模型，並透過ANSYS Icepak進行熱模擬。首先，程式透過Hfss3dLayout模組讀取前一階段建立的chip.aedb資料庫，取得晶片實際電路佈局、金屬密度及層疊結構的資訊，然後利用Icepak建立真實尺寸且精細的PCB幾何模型。接著從外部的power_map.txt檔案匯入每個區域的功耗數值，自動化在晶片表面建立對應的熱源分佈矩形區塊，模擬晶片內部因電流流動產生的局部熱點效應。

隨後，程式進一步建立處理器與其他晶片(dies)、封裝樹脂(molding)、基板(substrate)、錫球(balls)、以及底部PCB結構，並且依據實際尺寸、位置與材料（如矽、銅、特殊封裝材料）進行模型設定。其中晶片(dies)和處理器的區域還額外設定了內部的點溫度監控點(monitor)，用於即時追蹤模擬過程中重要區域的溫度變化，以方便後續的分析與判斷。

在模型完成後，程式針對模型上下表面分別設定了真實環境下的熱傳邊界條件（Heat Transfer Coefficient），例如晶片封裝頂面與底部PCB面，提供不同的熱傳係數設定，進一步模擬實際產品運作時上下表面的熱散逸狀況。最後，在啟動熱模擬分析前，透過Icepak內建的網格優先級設定功能，定義了模型內各元件的網格生成順序，確保模擬計算時，最重要或溫度變化劇烈的區域獲得較精細的網格配置，以提升模擬的準確度與效率。

```python
import os
from ansys.aedt.core import Hfss3dLayout
from ansys.aedt.core import Icepak

dx, dy = 1000, 1000
total_thickness = 4.22

if os.path.exists('chip.aedt'):
    os.remove('chip.aedt')
    
hfss = Hfss3dLayout('chip.aedb', version='2024.2')
icepak = Icepak(version='2024.2')
icepak.solution_type = 'SteadyState'
icepak.problem_type = 'TemperatureOnly'
icepak.modeler.model_units = 'mm'
icepak.modeler.delete('Region')

cmp = icepak.create_pcb_from_3dlayout('U1', hfss.project_name, hfss.design_name, resolution=6)

sources = []
with open('power_map.txt') as f:
    for line in f:
        sources.append([float(i) for i in line.split()])
        
for m, i in enumerate(sources):
    for n, value in enumerate(i):
        cell = icepak.modeler.create_rectangle('XY', 
                                               (f'{m*dx}um', f'{n*dy}um', f'{4.25}um'),
                                               (f'{dx}um', f'{dy}um'))
        icepak.assign_source(cell.name, "Total Power", f'{value}mW', f's{m}_{n}')
        
processor = icepak.modeler.create_box((0, 0, f'{total_thickness}um'), 
                                      (10, 10, 0.2), 
                                      name = 'processor',
                                      material='silicon' )
icepak.assign_point_monitor_in_object(processor.name, monitor_name=f'monitor_{processor.name}')
processor.transparency = 0

dies = [
        icepak.modeler.create_box((12, 0, 0), (5, 5, 0.25), 'd1', 'silicon'),
        icepak.modeler.create_box((12, 6, 0), (5, 5, 0.25), 'd2', 'silicon'), 
        icepak.modeler.create_box((0, 12, 0), (5, 5, 0.25), 'd3', 'silicon'), 
        icepak.modeler.create_box((6, 12, 0), (5, 5, 0.25), 'd4', 'silicon'),
        ]

for die in dies:
    icepak.assign_source(die.name, "Total Power", '0.1W', f's_{die.name}')
    icepak.assign_point_monitor_in_object(die.name, monitor_name=f'monitor_{die.name}')
    die.transparency = 0

molding = icepak.modeler.create_box((-1, -1, 0), (19, 19, 1), 'molding','mold_material')

sub = icepak.materials.add_material('substate')
sub.thermal_conductivity = [35, 35, 3.5]
substrate = icepak.modeler.create_box((-1, -1, 0), (19, 19, -1), 'substrate', sub.name)

balls = []
for i in range(0, 17):
    for j in range(0, 17):
        ball = icepak.modeler.create_box((i+0.3, j+0.3, -1), (0.4, 0.4, -0.4), f'ball_{i}_{j}', 'copper')
        balls.append(ball)

pcb = icepak.modeler.create_rectangle('XY', (-1, -1, -1.4),  (19, 19))

icepak.assign_stationary_wall(molding.top_face_z.id, 
                              boundary_condition = "Heat Transfer Coefficient",
                              htc = "1000w_per_m2kel"
                              )
icepak.assign_stationary_wall(pcb.bottom_face_z.id, 
                              boundary_condition = "Heat Transfer Coefficient",
                              htc = "100w_per_m2kel"
                              )

priorities = [[molding.name, substrate.name],
              [b.name for b in balls],
              [d.name for d in dies] + [processor.name], 
              [cmp.name]]

icepak.mesh.assign_priorities(priorities)

icepak.create_setup()
icepak.analyze()

```
### 完成建模

![2025-03-19_04-21-34](/assets/2025-03-19_04-21-34.png)

### 關於Trace Mapping
Trace Mapping是一種將電路板(PCB)上複雜的導線佈局轉換成可在熱模擬軟體(如ANSYS Icepak)中精確分析的方法。電路板上的每一條導線(Trace)都具有特定的電流值、電阻值以及金屬覆蓋密度(Metal Density)。當電流流過這些導線時，由於電阻會產生焦耳熱(Joule Heating)，造成熱量累積於電路板上。

此外，PCB內金屬覆蓋密度不同，也會影響材料的熱導率與散熱效率。因此，若能將導線的電流資訊、導線電阻及金屬密度一併考量，完整轉換成熱模擬所需資訊，便能更準確地呈現實際電子產品運作中的熱分佈狀況。Trace Mapping即是這種精確轉換過程的重要技術，能直接且快速地建立模擬所需的熱源資訊，改善傳統熱源設定過於簡化所造成的誤差。


