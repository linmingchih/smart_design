Lab4 結合PyAEDT與PyOptiSLang
---

在傳統的 AEDT 環境中，參數化通常是透過 GUI 介面手動設定，這對於簡單的模型來說是可行的，但當模型變得複雜或需要大量重複性工作時，這種方式就顯得非常低效。因此，使用 Python 腳本來自動化這一過程變得越來越重要。

PyAEDT可以幫助我們在 Python 環境中直接控制 AEDT，從幾何建模、邊界條件設定到求解和結果擷取都可以通過腳本完成。這不僅提高了效率，還能確保過程的一致性和可重複性。對於需要進行大量參數掃描或優化的情況，這種自動化方式尤其有價值。

### PyAEDT部分
這段程式碼主要是在 自動化操作 ANSYS Icepak，建立一個簡單的熱分析模型並取得模擬結果。前半段先透過 sys.path.append 手動加入 Python 套件路徑，確保可以成功匯入 ansys.aedt.core。接著建立 Icepak 物件並指定版本與無 GUI 模式（non_graphical=True），這在自動化或伺服器環境特別重要。之後定義幾個參數（圓柱高度 x1、功率 x2），並使用 modeler.create_cylinder 建立一個鋁材圓柱體。接著對圓柱上表面施加熱源（Total Power = 1W），底部則設定為固定溫度 0°C，形成一個典型的熱傳邊界條件。

後半段則是進行模擬與資料擷取流程。先在圓柱上表面設置溫度監測點（monitor），再建立分析設定（setup）並使用 12 核心進行求解。模擬完成後，透過 post.get_solution_data 讀取監測點的溫度結果，並轉成 Python float 存入變數 y。最後呼叫 release_desktop() 釋放 AEDT 資源，避免背景程序殘留。整體來看，這段程式展示了從「幾何建模 → 邊界條件 → 求解 → 結果擷取」的完整自動化流程，是典型的 PyAEDT 熱模擬腳本範例。

#### **c:/demo/icapak.py**
```python
import sys
sys.path.append(r'C:\0416\Lib\site-packages')

if not 'OSL_REGULAR_EXECUTION' in locals(): 
    OSL_REGULAR_EXECUTION = False

if not OSL_REGULAR_EXECUTION:
    x1 = 0.1
    x2 = 0.1

from ansys.aedt.core import Icepak

icepak = Icepak(version='2025.2', non_graphical=True)
c1 = icepak.modeler.create_cylinder('XY', (0,0,0), '0.5cm', f'{x1}cm', material="Al-Extruded")
icepak.assign_source(
    assignment=c1.top_face_z.id, 
    thermal_condition='Total Power', 
    assignment_value=f'{x2}W')

icepak.assign_stationary_wall(c1.bottom_face_z.id, 
                              "Temperature",
                              temperature=0)


icepak.monitor.assign_face_monitor(c1.top_face_z.id, monitor_name='m1')
setup = icepak.create_setup()
icepak.analyze(cores=12, tasks=12)
data = icepak.post.get_solution_data('m1.Temperature')
y = float(data.data_real()[0])
icepak.release_desktop()
```

### PyOptiSLang部分

這段程式碼是在用 Ansys optiSLang 建立一個完整的參數最佳化流程，並將前面寫好的 Icepak Python 腳本整合進來做自動化模擬。程式先啟動 optiSLang，取得專案的 root system，接著建立兩個節點：AMOP（參數最佳化核心）與 Design Export，並將 AMOP 的設計輸出接到 Design Export。

然後在 AMOP 裡新增一個 Python 節點，指定要執行的腳本路徑（icepak.py），並將腳本中的變數 x1、x2 註冊為可調整的設計參數，同時把輸出結果 y 註冊為 response。接著設定參數範圍（例如 x1 在 10~20、x2 在 1~5），並定義最佳化目標為「最小化 y」，也就是希望找到讓溫度最低的設計組合。最後將專案存成 .opf 檔並啟動計算，整體流程就是將「模擬腳本」轉為「可被最佳化引擎自動搜尋最佳解的設計流程」。

#### **c:/demo/lab4.py**
```python
script_path = 'c:/demo/icepak.py'
opf_path = 'c:/demo/lab3.opf'

from ansys.optislang.core import Optislang
import ansys.optislang.core.node_types as node_types
from ansys.optislang.core.nodes import DesignFlow
from ansys.optislang.core.project_parametric import (
    ComparisonType,
    ConstraintCriterion,
    ObjectiveCriterion,
    OptimizationParameter,
)


with Optislang(ini_timeout=60) as osl:
    root_system = osl.application.project.root_system
    amop = root_system.create_node(node_types.AMOP)
    design_export = root_system.create_node(node_types.DesignExport)
    
    amop_slot = amop.get_output_slots(name='ODesigns')[0]
    design_export_slot = design_export.get_input_slots(name='IDesigns')[0]
    amop_slot.connect_to(design_export_slot)
    
    python_node = amop.create_node(node_types.Python2, design_flow=DesignFlow.RECEIVE_SEND)
    prop = python_node.get_property('Path')
    prop['path']['split_path']['tail'] = script_path
    python_node.set_property('Path', prop)
    
    python_node.register_location_as_parameter('x1', 'x1', 0.1)
    python_node.register_location_as_parameter('x2', 'x2', 0.1)
    python_node.register_location_as_response('y', 'y', 0.1)
    
    parameters = amop.parameter_manager.get_parameters()
    parameters[0].range = [10.0, 15.0]
    parameters[1].range = [1.0, 3.0]
    
    amop.parameter_manager.modify_parameter(parameters[0])
    amop.parameter_manager.modify_parameter(parameters[1])
    
    criterion = ObjectiveCriterion(name="obj", expression="y", criterion=ComparisonType.MIN)
    amop.criteria_manager.add_criterion(criterion)
    
    osl.application.save_as(opf_path)
    #osl.application.project.start()
```