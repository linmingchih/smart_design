結合pyAEDT與optisLang進行機器學習應用的最佳實踐
---
隨著機器學習技術的快速發展，越來越多的工具和軟件被開發出來，以幫助研究者和工程師在不同領域進行應用。本文旨在探討如何有效結合pyAEDT與optisLang，並在機器學習項目中實施這些工具，以提高效率和結果的準確性。本文將介紹這兩款工具的基本功能、結合使用的優勢以及在實際應用中的最佳實踐。

### 流程說明

在optisLang建模中，主要使用AMOP模塊，並連接Python模塊。該Python模塊可以透過pyAEDT連接AEDT進行建模、設置、模擬並抓取數據。以下是具體操作和注意事項：

1. **AMOP模塊設置** ：
- 使用AMOP模塊作為主模塊，允許使用者定義參數輸入範圍和機器學習算法設置。
- 執行時，AMOP從所有參數構成的參數空間產生樣本點，這些樣本點將饋入Python模塊。並從Python方塊抓取資料以作機器學習。
2. **Python模塊設置** ：
- 連接Python腳本，在Python腳本中，使用pyAEDT進行模型設置、模擬並提取數據。 
- 配置Python模塊的參數（左側欄位）和響應（右側欄位）。

3. **數據處理與優化** ：
- AMOP模塊迭代運行，不斷送入參數樣本點，並通過Python模塊獲取模擬結果。
- 使用這些結果訓練機器學習模型，評估模型預測能力，直到達到所需的準確度。
- 完成之後生成AMOP.omdb檔案，使用者可以將參數輸入到模型當中並快速得到計算結果。

![2024-06-08_11-47-52](/assets/2024-06-08_11-47-52.png)

### 注意事項
1. 在pyAEDT腳本中，參數定義通常放在以下模塊當中：

```python
if not 'OSL_REGULAR_EXECUTION' in locals(): 
    OSL_REGULAR_EXECUTION = False

if not OSL_REGULAR_EXECUTION:
    pcb_w = 30 # 30
    pcb_l = 30 # 30
    ws = 28.5 # (15, 35)
    ls = 10 # [10, 11, 12]
    dd = 1.5 # (1, 3)
    w1 = 2.5 # (1, 4)
    w2 = 1.5 # (1, 4)
    gap1 = 2 # (1, 5)
    gap2 = 1 # (1, 3)
    wf = 3 # (-4, 4)
    lf = 13 # (13, 16)
    t = 1 # 1
```

響應定義方式
```python
    s11_2p4 = y[14]  # response
    s11_5p8 = y[48]  # response
```

此代碼段確保參數開發及調試階段可以被初始化，但在optisLang模型訓練階段不會被執行，如此AMOP傳遞進Python模塊便不會被覆蓋。參數定義後面並以註解方式設置了參數的範圍和類型（連續或離散）。

2. 在pyAEDT腳本中進行例外處理，這可以確保在某組參數無法成功建模時，程式能夠正確地關閉並返回optisLang，繼續處理下一組參數。以下是腳本示例：

``` python
import pyaedt
import time
from pyaedt import Hfss

# 禁用錯誤處理器
pyaedt.settings.enable_error_handler = False

try:
    # 初始化Hfss
    hfss = Hfss(specified_version='2024.1', non_graphical=False)
    
    # 前處理程式碼
    # （在這裡設置您的模型和參數）

    # 驗證設計
    if not hfss.validate_full_design()[-1]:
        raise ValueError("Failed Validation.")

    # 執行模擬
    hfss.analyze_nominal(num_cores=20)
    
    # 後處理程式碼
    # （在這裡處理模擬結果）

except Exception as e:
    print(f"An error occurred: {e}")
    pass

finally:
    # 關閉專案且不保存
    hfss.close_project(save_project=False)
    time.sleep(5)

```

3. 使用PyOptisLang腳本建立新的optisLang檔案(.opf)，該腳本可以讀取Python參數定義及響應定義並自動添加到python模塊及AMOP模塊當中，大大節省手動設置時間。
- `( )` 用於表示連續範圍，如 `ws = 28.5 # (15, 35)` 
- `[ ]` 用於表示離散值選項，如 `ls = 10 # [10, 11, 12]` 
- 無註解則表示為常數，如 `pcb_w = 30`
- `response`代表響應，如 `s11_2p4 = y[14]  # response`
- 使用上述註解標記，PyOptislang腳本可以自動識別參數類型並生成對應的範圍設置，減少手動配置的繁瑣步驟。

![2024-06-08_19-12-16](/assets/2024-06-08_19-12-16.png)


4. optisLang一旦完成機器模型訓練，會輸出omdb檔案。我們便可以用Python程式碼調用該機器模型，輸入參數並迅速得到結果。欲取得mopsolver模組請與ANSYS聯繫。

```python
from mopsolver import MOPSolver
osl_install_path = r'C:\Program Files\ANSYS Inc\v241\optiSLang'
omdb_file = r"D:/OneDrive - ANSYS, Inc/GitHub/generate_opf/assets/dual_band_antenna.opd/AMOP/AMOP.omdb"

solver = MOPSolver(osl_install_path, omdb_file)

print(solver)
print(solver.run([[15.1, 10.0, 1.01, 1.015, 1.015, 1.0199999999999998, 1.01, 2.01, 13.015], 
                  [34.9, 12.0, 2.99, 3.9850000000000003, 3.985, 4.98, 2.99, 3.99, 15.985]]))
```

### pyOptisLang轉換腳本
```python
import os, re, time
from numpy import arange, linspace
from ansys.optislang.core import Optislang
from ansys.optislang.core import node_types
from ansys.optislang.core.project_parametric import ObjectiveCriterion
from ansys.optislang.core.tcp.osl_server import TcpOslServer

script_path = 'D:/OneDrive - ANSYS, Inc/GitHub/generate_opf/dual_band_antenna.py'

opf_path = os.path.join(os.path.dirname(script_path),
                        'assets',
                        os.path.basename(script_path).replace('.py', '.opf'))


osl_server = TcpOslServer(ini_timeout=120)

osl_server.new()
para_node = osl_server.create_node(node_types.AMOP.id)
python_node = osl_server.create_node(node_types.Python2.id, parent_uid=para_node)

osl_server.set_actor_property(python_node, 'AllowSpaceInFilePath', True)
prop = osl_server.get_actor_properties(python_node)
prop['Path']['path']['split_path']['head'] = os.path.dirname(script_path)
prop['Path']['path']['split_path']['tail'] = os.path.basename(script_path)

osl_server.set_actor_property(python_node, 'Path', prop['Path'])
x = osl_server.get_actor_properties(python_node)

osl_server.connect_nodes(para_node, "IODesign", python_node, "IDesign")
osl_server.connect_nodes(python_node, "ODesign", para_node, "IIDesign")

def get_inout(script_path):
    with open(script_path) as f:
        text = f.readlines()
    
    parameters = []
    responses = []
    flag = False
    
    for line in text:
        if len(line.strip()) == 0:
            continue
        
        if 'OSL_REGULAR_EXECUTION:' in line:
            flag = True
            continue
        
        elif flag and line[0:4] == '    ':
            try:
                assignment = line.strip().split('#')[0]
                _range = eval(line.strip().split('#')[1])
            except:
                _range = None
                
            parameter, initial_value = [i.strip() for i in assignment.split('=')]
            initial_value = eval(initial_value)
            
            match _range:
                case None:
                    parameters.append((parameter, initial_value, 'Constant' , initial_value))
                case (x, y):
                    parameters.append((parameter, initial_value, 'Continuous' , (x, y)))
                case list():
                    parameters.append((parameter, initial_value, 'Discrete' , _range))
        
        elif flag and line[0] != '':
            flag = False
            
            
        elif re.search('#(\s+?|)response', line):
            assignment, comment = line.strip().split('#')
            response, _ = assignment.split('=')
            responses.append(response.strip())
        
    return parameters, responses
        
        
#%%     
parameters, responses = get_inout(script_path)

for key, initial_value, *_ in parameters:
    osl_server.register_location_as_parameter(python_node, key, key, initial_value)

for response in responses:
    osl_server.register_location_as_response(python_node, response, response, 0.1)


info = osl_server.get_actor_properties(para_node)
container = info['ParameterManager']['parameter_container']
info['AMopSettings']['num_designs_max'] = 300

for (key, initial_value, _type, _range), item in zip(parameters, container):
    if _type == 'Constant':
        item['const'] = True
    
    elif _type == 'Continuous':
        lower_bound, upper_bound = _range
        item['const'] = False
        item['deterministic_property']['domain_type'] = 'real'
        item['deterministic_property']['kind'] = 'continuous'        
        item['deterministic_property']['lower_bound'] = lower_bound
        item['deterministic_property']['upper_bound'] = upper_bound
    
    elif _type == 'Discrete':
        item['const'] = False
        item['deterministic_property']['domain_type'] = 'real'
        item['deterministic_property']['kind'] = 'ordinaldiscrete_value'
        item['deterministic_property']['discrete_states'] = _range      


osl_server.set_actor_property(para_node, 'ParameterManager', info['ParameterManager'])
osl_server.set_actor_property(para_node, 'AMopSettings', info['AMopSettings'])


osl_server.save_as(opf_path)
osl_server.dispose()
```

### 雙頻天線範例
```python
import pyaedt
from pyaedt import Hfss
import time
import sys
pyaedt.settings.enable_error_handler = False


if not 'OSL_REGULAR_EXECUTION' in locals(): 
    OSL_REGULAR_EXECUTION = False


if not OSL_REGULAR_EXECUTION:
    pcb_w = 30
    pcb_l = 30
    ws = 28.5 # (15, 35)
    ls = 10 # [10, 11, 12]
    dd = 1.5 # (1, 3)
    w1 = 2.5 # (1, 4)
    w2 = 1.5 # (1, 4)
    gap1 = 2 # (1, 5)
    gap2 = 1 # (1, 3)
    wf = 3 # (-4, 4)
    lf = 13 # (13, 16)
    t = 1


try:
    hfss = Hfss(specified_version='2024.1', non_graphical=False)
    hfss.modeler.model_units = 'mm'
       
    hfss.modeler.create_rectangle(2, (-pcb_w/2, -pcb_l/2, 0), (pcb_w, pcb_l), matname='FR4_epoxy', name='pcb')
    hfss.modeler.sweep_along_vector('pcb', (0, 0, -t))
    
    hfss.modeler.create_rectangle(2, (-pcb_w/2, -pcb_l/2, 0), (pcb_w, pcb_l), matname='PEC', name='gnd')
    hfss.modeler.create_rectangle(2, (-ws/2, -ls/2, 0), (ws, ls), name='void')
    
    hfss.modeler.subtract('gnd', 'void', False)
    hfss.assign_perfecte_to_sheets('gnd')
    
    pts = [(-dd/2, -ls/2+gap2),
           (-ws/2+gap1, -ls/2+gap2),
           (-ws/2+gap1, ls/2-gap2),
           (-dd/2, ls/2-gap2),
           (-dd/2, ls/2-gap2-w2),
           (-ws/2+gap1+w1, ls/2-gap2-w2),
           (-ws/2+gap1+w1, -ls/2+gap2+w2),
           (-dd/2, -ls/2+gap2+w2),]
    
    
    hfss.modeler.create_polyline([(x, y, 0) for x, y in pts],
                                           cover_surface=True,
                                           close_surface=True,
                                           name='antenna')
    
    hfss.assign_perfecte_to_sheets('antenna')
    
    hfss.modeler.duplicate_and_mirror('antenna', (0,0,0), (1,0,0))
    
    hfss.modeler.create_polyline([(0, pcb_l/2, -t), (0, pcb_l/2-lf, -t)],
                                        xsection_type='Rectangle',
                                        xsection_height=0,
                                        xsection_width=wf,
                                        matname='PEC', name='feed')
    
    hfss.assign_perfecte_to_sheets('feed')
    
    hfss.modeler.create_polyline([(-wf/2, pcb_l/2, 0),
                                             (wf/2, pcb_l/2, 0),
                                             (wf/2, pcb_l/2, -t),
                                             (-wf/2, pcb_l/2, -t)],
                                            close_surface=True,
                                            cover_surface=True,
                                            name='sheet')
    
    hfss.create_lumped_port_to_sheet('sheet', axisdir=2)
    hfss.create_open_region('3GHz')
    hfss.oeditor.FitAll()

    setup = hfss.create_setup()
    setup.props['MaximumPasses'] = 10
    sweep = setup.create_frequency_sweep(unit='GHz', freqstart=1, freqstop=7, num_of_freq_points=61)
    sweep.props['Type'] = 'Interpolating'
    sweep.props['SaveFields'] = False
    sweep.update()
    

    if not hfss.validate_full_design()[-1]:
        raise ValueError("Failed Validation.")

    hfss.analyze_nominal(num_cores=20)
    
    
    data = hfss.post.get_solution_data('dB(S11)')
    x = data.primary_sweep_values
    y = data.data_real()
    
    s11_2p4 = y[14]  # response
    s11_5p8 = y[48]  # response

except:
    pass

finally:
    hfss.close_project(save_project=False)
    time.sleep(5)
```