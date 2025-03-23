Icepak熱模擬建立
---

這段程式的目的是**建立一個完整的 3D 封裝熱模擬模型，並自動在 Icepak 中進行設定與分析** 。整體流程從初始化專案開始，到載入 HFSS 3D Layout 專案，再進行幾何結構建模、功率載入、邊界條件設定、網格優先順序安排，最後進行模擬並儲存結果。

1. **初始化與清理環境** ：如果存在舊的 Icepak 專案，就先刪除它，確保執行時不受先前模擬影響。
 
2. **讀取 HFSS Layout 並建立 PCB 模型** ：透過 `create_pcb_from_3dlayout` 方法將 HFSS 3D Layout 專案的封裝元件 `U1` 匯入至 Icepak 中，作為熱模擬的初始基礎。
 
3. **根據 power map 自動建立功率來源區塊** ：從文字檔讀入功率分布資料後，依據座標建立一系列的 rectangle 作為發熱區域，並分別指派功率來源。
 
4. **建立 processor 和 dies 模型，並監控溫度** ：建立主要熱源處理器與四顆晶粒，並在每個元件中設置溫度監視點，用以後續溫度分析。
 
5. **建構模封、基板與球腳結構** ：依據幾何位置建構 molding、substrate、焊球（ball）等材料區塊，並使用指定的材料參數。
 
6. **設定熱邊界條件** ：在 molding 頂部與 PCB 底部指定對流熱傳邊界條件，以模擬實際冷卻環境。
 
7. **指定網格優先順序** ：安排模擬中不同幾何體的網格細緻程度，越小的元件通常需要更細的網格。
 
8. **建立並設定模擬 setup** ：指定收斂條件與最大迭代次數，以確保穩定解算。
 
9. **執行模擬與儲存** ：開始模擬流程、儲存模擬結果，並關閉專案，完成整個熱模擬流程。

### 程式碼範例

```python
import os
from ansys.aedt.core import Hfss3dLayout
from ansys.aedt.core import Icepak

dx, dy = 1000, 1000
total_thickness = 4.22

if os.path.exists('c:/demo/chip.aedt'):
    os.remove('c:/demo/chip.aedt')
    
hfss = Hfss3dLayout('c:/demo/chip.aedb', version='2024.2')
icepak = Icepak(version='2024.2')
icepak.solution_type = 'SteadyState'
icepak.problem_type = 'TemperatureOnly'
icepak.design_settings['ExportSettings'] = True


icepak.modeler.model_units = 'mm'
icepak.modeler.delete('Region')

cmp = icepak.create_pcb_from_3dlayout('U1', hfss.project_name, hfss.design_name, resolution=6)

sources = []
with open('c:/demo/power_map.txt') as f:
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

setup = icepak.create_setup()
setup.props['Convergence Criteria - Energy'] = 1e-16
setup.props['Convergence Criteria - Max Iterations'] = 500
icepak.analyze()
icepak.save_project()
icepak.close_project()
```
### 完成建模

![2025-03-19_04-21-34](/assets/2025-03-19_04-21-34.png)

### 關於Trace Mapping

Trace Mapping是一種將電路板(PCB)上複雜的導線佈局轉換成可在熱模擬軟體(如ANSYS Icepak)中精確分析的方法。電路板上的每一條導線(Trace)都具有特定的電流值、電阻值以及金屬覆蓋密度(Metal Density)。當電流流過這些導線時，由於電阻會產生焦耳熱(Joule Heating)，造成熱量累積於電路板上。

此外，PCB內金屬覆蓋密度不同，也會影響材料的熱導率與散熱效率。因此，若能將導線的電流資訊、導線電阻及金屬密度一併考量，完整轉換成熱模擬所需資訊，便能更準確地呈現實際電子產品運作中的熱分佈狀況。Trace Mapping即是這種精確轉換過程的重要技術，能直接且快速地建立模擬所需的熱源資訊，改善傳統熱源設定過於簡化所造成的誤差。


