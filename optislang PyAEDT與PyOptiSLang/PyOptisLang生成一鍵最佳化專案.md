PyOptisLang生成一鍵最佳化專案
---

「一鍵最佳化」(One-Click Optimization, OCO) 是optisLang高度自動化的優化流程，旨在通過幾個關鍵步驟有效地探索和優化設計空間。這個過程從初步取樣開始，分析輸入與輸出參數間的關係，以確定各參數對結果的影響。接著，結合全局搜索和局部搜索策略，全局搜索幫助識別整個參數空間的潛在優化方向，而局部搜索則在這些區域內進一步細化和優化。

當現有優化方法表現不佳或已收斂時，OCO會評估並切換到新的優化策略，以提高效率和效果。這個過程會不斷迭代，直到達到預設的最大評估次數。在整個過程中，OCO利用後台的元模型來選擇最佳的代理模型，這些模型評估各參數的重要性，自動選擇最有前途的優化方法和設定。這種方法允許快速、高效地達到設計的最優解。

### PyOptiSLang

PyOptiSLang 是一個針對 ANSYS OptiSLang 設計的 Python 接口，它允許開發者直接使用 Python 腳本來設定、控制和執行優化工作。這種接口大大簡化了優化流程的設置，使得開發者可以更快速、更靈活地生成和管理優化專案。以下是 PyOptiSLang 提供的主要優點：
 
1. **自動化流程** ：
  - 通過 PyOptiSLang，開發者可以編寫腳本來自動化常見的設置步驟，例如參數定義、模型加載、目標和約束的設置等，這些都可以在不離開 Python 環境的情況下完成。
 
2. **直觀的 API** ：
  - PyOptiSLang 提供了一套直觀的 API，使得開發者可以容易地與 OptiSLang 的核心功能交互，比如參數管理、優化策略設定、結果處理等。
 
3. **靈活性與擴展性** ：
  - 這個接口支持多種優化方法和技術，開發者可以根據具體需求選擇合適的方法。此外，它也支持與其他 Python 庫的整合，如PyAEDT、SPICE模擬等等，進一步提升優化的能力和精確度。
 
4. **腳本化與再現性** ：
  - 使用 PyOptiSLang，所有優化的設置和過程都可以腳本化，這不僅提高了工作的效率，也保證了過程的可追蹤性和再現性。
 
5. **更快的迭代與開發速度** ：
  - 開發者可以快速迭代優化設置和參數，立即看到變更效果，這對於複雜系統的性能調整尤其有價值。

總的來說，PyOptiSLang 為開發者提供了一個強大而靈活的工具，可以快速且有效地生成所需的優化專案，從而加速設計和開發過程，提升產品的性能和質量。這對於需要進行大規模和高精度優化的工程和科研領域尤為重要。

### Python OCO框架

「一鍵最佳化」(One-Click Optimization, OCO) 的optisLang專案呈現了整個OCO優化過程的框架和組件。流程開始於「One-Click Optimization (OCO)」的主要模塊，然後通過Python腳本進行參數的調整和計算。最後，優化結果將進入到「Postprocessing」階段，也就是後處理部分，用於分析和視覺化優化結果。

這個框架當中Python節點，OCO設定皆為空白。

![2025-01-13_14-08-39](/assets/2025-01-13_14-08-39.png)

### 透過PyOptisLang增添框架內容

這段程式碼示範了如何在使用ansys.optislang套件的環境中，設置和執行一個基於Python的優化任務。整個過程分為幾個主要部分：
 
1. **條件檢查與變數設定** ： 
  - 首先檢查`OSL_REGULAR_EXECUTION`變數是否已在本地環境定義。如果沒有，則設定`OSL_REGULAR_EXECUTION`為`False`。
 
  - 如果`OSL_REGULAR_EXECUTION`為`False`，則設定`x1`和`x2`為0.1。
 
2. **計算函數** ： 
  - 定義函數`y`，這是一個二次函數，用於優化。
 
3. **設定優化環境** ： 
  - 將Python代碼寫入文件`test.py`，並在OptiSLang環境中設定相關路徑和參數。
 
  - 創建`TcpOslServer`對象，並開啟模板。

  - 獲取項目樹結構並設定Python腳本的路徑與參數。
 
4. **參數與響應變量註冊** ： 
  - 使用OptiSLang的TCP服務器註冊`x1`和`x2`作為輸入參數，`y`作為響應變量。

  - 為每個參數設定上下界限。
 
5. **設定優化目標與標準** ： 
  - 在優化控制器中添加最小化`y`的目標。

  - 更新並保存優化設定。
 
6. **啟動優化** ： 
  - 使用`Optislang`類開啟和啟動項目。

> :memo: 附註：關於add_criterion()
> <br>add_criterion(uid: str, criterion_type: str, expression: str, name: str, limit: str | None = None)
<br>**criterion_type：**
>- **Variable**：ignore 
>- **Objective**：min / max
>- **Constraint**：lessequal / equal / greaterequal
>- **Limit State**：lesslimitstate / greaterlimitstate

#### 範例代碼
```python

'''
template_opf_path = 'd:/demo/oco.opf'
opf_path = 'd:/demo/oco_finished.opf'

text = '''
if not 'OSL_REGULAR_EXECUTION' in locals(): 
    OSL_REGULAR_EXECUTION = False

if not OSL_REGULAR_EXECUTION:
    x1 = 0.1  #para
    x2 = 0.1  #para

y = (x1 -1)**2 + (x2 -3)**2

'''

import re
paras = re.findall('(\S+).*?=.*?(\S+).*#para', text)

with open('d:/demo/test.py', 'w') as f:
    f.write(text)

import os
from ansys.optislang.core import Optislang
from ansys.optislang.core.tcp.osl_server import TcpOslServer
osl_server = TcpOslServer()
osl_server.open(template_opf_path)

tree_props = osl_server.get_full_project_tree_with_properties()

oco_node = tree_props['projects'][0]['system']['nodes'][0]['uid']
python_node = tree_props['projects'][0]['system']['nodes'][0]['nodes'][0]['uid']
post_node = tree_props['projects'][0]['system']['nodes'][0]['uid']

prop = osl_server.get_actor_properties(post_node)


osl_server.set_actor_property(python_node, 'AllowSpaceInFilePath', True)
prop = osl_server.get_actor_properties(python_node)
prop['Path']['path']['split_path']['head'] = 'd:/demo'
prop['Path']['path']['split_path']['tail'] = 'test.py'

osl_server.set_actor_property(python_node, 'Path', prop['Path'])
x = osl_server.get_actor_properties(python_node)

for p, v in paras:
    osl_server.register_location_as_parameter(python_node, p, p, float(v))

osl_server.register_location_as_response(python_node, 'y', 'y', 0.1)
info = osl_server.get_actor_properties(oco_node)

container = info['ParameterManager']['parameter_container']
container[0]['deterministic_property']['lower_bound'] = -5
container[0]['deterministic_property']['upper_bound'] = 5

container[1]['deterministic_property']['kind'] = 'ordinaldiscrete_value'
container[1]['deterministic_property']['discrete_states'] = [-4.0, -3.0, -2.0, -1.0, 0.0, 1.0, 2.0, 3.0, 4.0]

osl_server.add_criterion(oco_node, 'min', 'y', 'obj_0')

osl_server.set_actor_property(oco_node, 'ParameterManager', info['ParameterManager'])

osl_server.save_as(opf_path)
osl_server.dispose()

#%%
with Optislang(project_path=opf_path) as osl:
    osl.application.project.start()
    
os.system('notepad D:\demo\oco_finished.opd\out.csv')
```

### oco_finished.opf輸出
當執行Python檔案，Python會自動將程式碼與相關設定填入框架節點、存檔並完成計算。完成計算的optisLang專案節點出現打勾，代表完成計算：

![2025-01-13_14-02-43](/assets/2025-01-13_14-02-43.png)

#### Python內容、參數與響應
箭頭處標示程式碼所加入的內容：

![2024-07-27_03-59-29b](/assets/2024-07-27_03-59-29b.png)

#### OCO節點
程式碼所加入的優化目標：

![2024-07-27_04-04-38](/assets/2024-07-27_04-04-38.png)

#### 後處理結果

osl.application.project.start()啟動優化計算並儲存結果：

![2024-07-27_04-07-23](/assets/2024-07-27_04-07-23.png)

### 結論

透過結合 PyOptiSLang、PyAEDT（ANSYS Electronics Desktop 的 Python 接口），以及 SPICE 模擬工具，開發者可以搭建一個強大的自動化優化框架，用於電子設計和分析。這種整合使得從電子設計的初步階段到最終的性能優化可以在一個連貫的流程中完成，大大提高效率和精確度。

> OCO.opf框架下載
[oco.opf](/assets/oco.opf)