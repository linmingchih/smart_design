PyOptiSLang建立MOP模型
---

為了提升使用 PyAEDT 與 optiSLang 的整合效率，我們可以利用 PyOptiSLang 模組自動化一些過程。在過去，將 Python 代碼手動添加到 optiSLang 的 schematic 中並設置相關參數及其範圍，若參數眾多，這一步驟將會變得相當繁重。但現在，通過使用 PyOptiSLang 模組，我們可以編寫程式碼來自動化這些設置，從而大大減輕手動操作的負擔。這不僅提高了工作效率，還有助於減少因手動設置錯誤而導致的問題。

這份程式碼示範如何透過 Ansys Optislang API 建立一個簡單的優化流程。整個流程可以分為以下幾個步驟：
 
1. **定義並儲存 Python 腳本** 
程式首先定義了一段 Python 腳本，此腳本執行簡單的數學運算：根據輸入變數 x1 和 x2 計算 y，其計算公式為 y = (x1 - 1)² + (x2 - 3)²。程式將這段腳本存入指定的檔案路徑，供後續節點讀取與執行。
 
2. **初始化 Optislang 專案與節點建立** 
利用 Optislang 物件初始化專案，取得專案的根系統後建立兩個主要節點： 
  - **AMOP 節點** ：負責管理設計樣本與參數設定。
 
  - **DesignExport 節點** ：用來匯出設計資料。
程式透過連接 AMOP 節點的輸出插槽與 DesignExport 節點的輸入插槽，確保設計資料能在流程中正確傳遞。
 
3. **建立 Python 節點與參數註冊** 
在 AMOP 節點內新增一個 Python 節點，並設定其屬性，使其能夠讀取先前儲存的腳本。接著，利用方法 register_location_as_parameter 將腳本中的變數 x1 與 x2 註冊為優化參數，同時將變數 y 註冊為響應結果，這樣在執行優化時便能正確讀取與傳遞各變數的數值。
 
4. **設定參數範圍與目標準則** 
從參數管理器中取得已註冊的參數，並將每個參數的搜尋範圍設定在 -5 到 5 之間。這樣可限制優化過程中參數的可能取值範圍。接著，定義一個目標準則，其目標為使 y 的數值最小化，並將此目標加入 Criteria 管理器中，供優化演算法參考。
 
5. **儲存專案與執行優化流程** 
程式最後將整個專案存檔成指定的 .opf 檔案，再啟動優化流程。流程結束後，系統會自動釋放相關資源。

```python
script_path = 'd:/demo/script.py'
opf_path = 'd:/demo/example5.opf'

from ansys.optislang.core import Optislang
import ansys.optislang.core.node_types as node_types
from ansys.optislang.core.nodes import DesignFlow
from ansys.optislang.core.project_parametric import (
    ComparisonType,
    ConstraintCriterion,
    ObjectiveCriterion,
    OptimizationParameter,
)

script = '''
if not 'OSL_REGULAR_EXECUTION' in locals(): 
    OSL_REGULAR_EXECUTION = False


if not OSL_REGULAR_EXECUTION:
    x1 = 0.1
    x2 = 0.1

y = (x1 -1)**2 + (x2 -3)**2
'''

with open(script_path, 'w') as f:
    f.write(script)

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
    parameters[0].range = [-5.0, 5.0]
    parameters[1].range = [-5.0, 5.0]
    
    amop.parameter_manager.modify_parameter(parameters[0])
    amop.parameter_manager.modify_parameter(parameters[1])
    
    criterion = ObjectiveCriterion(name="obj", expression="y", criterion=ComparisonType.MIN)
    amop.criteria_manager.add_criterion(criterion)
    
    osl.application.save_as(opf_path)
    osl.application.project.start()

```

### 完成並輸出AMOP檔案
![2025-02-01_12-41-58](/assets/2025-02-01_12-41-58.png)

### 利用AMOP快速得到答案
之後可以用程式碼輸入數值並快速得到計算結果，可以連結網頁伺服器來提供服務。

``` python
from mopsolver import MOPSolver
osl_install_path = r'C:\Program Files\ANSYS Inc\v241\optiSLang'
omdb_file = r"D:\demo\example5.opd\AMOP\AMOP.omdb"

solver = MOPSolver(osl_install_path, omdb_file)

print(solver)
print(solver.run([[0, 0], [1, 1]]))
```

![2024-05-30_14-49-54](/assets/2024-05-30_14-49-54.png)