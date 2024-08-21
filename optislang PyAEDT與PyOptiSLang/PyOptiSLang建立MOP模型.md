PyOptiSLang建立MOP模型
---

為了提升使用 PyAEDT 與 optiSLang 的整合效率，我們可以利用 PyOptiSLang 模組自動化一些過程。在過去，將 Python 代碼手動添加到 optiSLang 的 schematic 中並設置相關參數及其範圍，若參數眾多，這一步驟將會變得相當繁重。但現在，通過使用 PyOptiSLang 模組，我們可以編寫程式碼來自動化這些設置，從而大大減輕手動操作的負擔。這不僅提高了工作效率，還有助於減少因手動設置錯誤而導致的問題。

以下這段代碼主要展示了如何使用 PyOptiSLang API 在 optiSLang 中自動化設定一個基本的參數化模型和優化過程。重點摘要如下： 
1. **初始化並設定變數** ：首先檢查是否已定義 `OSL_REGULAR_EXECUTION` 變數，若未定義則將其設為 `False`。當此變數為 `False` 時，設定兩個參數 `x1` 和 `x2` 的初始值。 
2. **計算目標函數** ：計算目標函數 `y`，這是一個典型的二次函數，用於後續的優化。 
3. **寫入 Python 腳本** ：將包含變數初始化和目標函數計算的 Python 代碼寫入到文件 `test.py`。 
4. **設定與連接節點** ：在 optiSLang 服務器上創建節點，並設定 Python 節點的路徑屬性，使其指向剛才創建的腳本文件。 
5. **註冊參數與響應** ：將 `x1` 和 `x2` 註冊為優化參數，並將 `y` 註冊為響應函數。 
6. **設定參數範圍** ：設定參數 `x1` 和 `x2` 的範圍，此範圍將用於優化過程。 
7. **保存並執行MOP建模** ：保存設定並啟動優化過程，最終目的是找到最小化 `y` 的參數值。

這樣的自動化過程能夠有效地提升模型設置的效率和準確性，適用於需要進行參數優化的各種工程和科研領域。


```python
text = '''
if not 'OSL_REGULAR_EXECUTION' in locals(): 
    OSL_REGULAR_EXECUTION = False


if not OSL_REGULAR_EXECUTION:
    x1 = 0.1
    x2 = 0.1

y = (x1 -1)**2 + (x2 -3)**2

'''

with open('d:/demo3/test.py', 'w') as f:
    f.write(text)

from ansys.optislang.core import Optislang
from ansys.optislang.core import node_types
from ansys.optislang.core.project_parametric import ObjectiveCriterion
from ansys.optislang.core.tcp.osl_server import TcpOslServer
osl_server = TcpOslServer()
osl_server.new()
para = osl_server.create_node(node_types.AMOP.id)
python = osl_server.create_node(node_types.Python2.id, parent_uid=para)

osl_server.set_actor_property(python, 'AllowSpaceInFilePath', True)
prop = osl_server.get_actor_properties(python)
prop['Path']['path']['split_path']['head'] = 'd:/demo3'
prop['Path']['path']['split_path']['tail'] = 'test.py'

osl_server.set_actor_property(python, 'Path', prop['Path'])
x = osl_server.get_actor_properties(python)

osl_server.connect_nodes(para, "IODesign", python, "IDesign")
osl_server.connect_nodes(python, "ODesign", para, "IIDesign")

osl_server.register_location_as_parameter(python, 'x1', 'x1', 0.1)
osl_server.register_location_as_parameter(python, 'x2', 'x2', 0.1)

osl_server.register_location_as_response(python, 'y', 'y', 0.1)
info = osl_server.get_actor_properties(para)

container = info['ParameterManager']['parameter_container']
container[0]['deterministic_property']['lower_bound'] = -5
container[0]['deterministic_property']['upper_bound'] = 5

container = info['ParameterManager']['parameter_container']
container[1]['deterministic_property']['lower_bound'] = -5
container[1]['deterministic_property']['upper_bound'] = 5

osl_server.set_actor_property(para, 'ParameterManager', info['ParameterManager'])

osl_server.save_as('d:/demo3/example.opf')

osl_server.add_criterion(para, 'min', 'y', 'obj_0')


osl_server.dispose()

#%%

with Optislang(project_path='d:/demo3/example.opf') as osl:
    osl.application.project.start()
```

### 完成並輸出AMOP檔案
![2024-05-30_12-35-12](/assets/2024-05-30_12-35-12.png)


### 利用AMOP快速得到答案
之後可以用程式碼輸入數值並快速得到計算結果，可以連結網頁伺服器來提供服務。

``` python
from mopsolver import MOPSolver
osl_install_path = r'C:\Program Files\ANSYS Inc\v241\optiSLang'
omdb_file = r"D:\demo3\example.opd\AMOP\AMOP.omdb"

solver = MOPSolver(osl_install_path, omdb_file)

print(solver)
print(solver.run([[0, 0], [1, 1]]))
```

![2024-05-30_14-49-54](/assets/2024-05-30_14-49-54.png)