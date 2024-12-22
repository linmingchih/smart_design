串接S參數模擬並輸出S參數
---

```python
netlist = r'''
.model channel S TSTONEFILE="D:/OneDrive - ANSYS, Inc/Models/S_Parameter/channel.s4p"
+ INTERPOLATION=LINEAR INTDATTYP=MA HIGHPASS=10 LOWPASS=10 convolution=0 enforce_passivity=0 enforce_adpe=1 Noisemodel=External

S1 Port1 Port2 net_1 net_2 FQMODEL="channel"
S2 net_1 net_2 Port3 Port4 FQMODEL="channel"
'''

import os
from pyaedt import Circuit

circuit = Circuit(version='2024.1', non_graphical=True)

cir_path = os.path.join(circuit.temp_directory, 'channel.cir')
with open(cir_path, 'w') as f:
    f.write(netlist)
    
circuit.add_netlist_datablock(cir_path)
for i in range(4):
    circuit.modeler.components.create_interface_port(f'Port{i+1}')

setup = circuit.create_setup(setup_type=circuit.SETUPS.NexximLNA)
setup.props['SweepDefinition']['Data'] = 'LINC 0GHz 20GHz 2001'

circuit.analyze()
circuit.export_touchstone(output_file='c:/demo/channel.s4p')

```

這段代碼展示了如何使用 PyAEDT 中的 `Circuit` 模組來進行電路的建模與模擬，並導出結果。這裡，我將逐步解釋這段代碼的作用和流程： 
### 1. **建立 netlist** ：

```python
netlist = r'''
.model channel S TSTONEFILE="D:/OneDrive - ANSYS, Inc/Models/S_Parameter/channel.s4p"
+ INTERPOLATION=LINEAR INTDATTYP=MA HIGHPASS=10 LOWPASS=10 convolution=0 enforce_passivity=0 enforce_adpe=1 Noisemodel=External

S1 Port1 Port2 net_1 net_2 FQMODEL="channel"
S2 net_1 net_2 Port3 Port4 FQMODEL="channel"
'''
```
這段 `netlist` 使用的是 HSPICE 格式的模型描述。`channel` 使用了一個已有的 `.s4p` S 參數檔案來描述一個通道的行為。
 
### 2. **匯入相關的模組與初始化 Circuit** ：

```python
from pyaedt import Circuit
circuit = Circuit(version='2024.1', non_graphical=True)
```
使用 `pyaedt` 初始化了一個非圖形化界面的 Circuit 對象，`version='2024.1'` 表明使用的 ANSYS 版本。
 
### 3. **寫入 netlist 到檔案** ：

```python
cir_path = os.path.join(circuit.temp_directory, 'channel.cir')
with open(cir_path, 'w') as f:
    f.write(netlist)
```

將 netlist 寫入到一個臨時檔案中。這樣可以讓 Circuit 載入該網表。
 
### 4. **將 netlist 資料塊加入電路模組** ：

```python
circuit.add_netlist_datablock(cir_path)
```
利用 `add_netlist_datablock()` 將 netlist 加載進 Circuit 模型中，這樣可以讓 ANSYS 模擬工具了解我們的電路結構。
 
### 5. **創建接口端口** ：

```python
for i in range(4):
    circuit.modeler.components.create_interface_port(f'Port{i+1}')
```

創建了四個接口端口，這些端口將對應 netlist 中的 Port1 到 Port4，為進一步分析準備好端點。

> :warning: 如果在網表中定義了 S 參數的 Port 元件，會導致 AEDT 電路模擬時找不到端口而出現錯誤。正確的做法是在網表中不直接宣告 Port 元件，而是使用 PyAEDT 的 create_interface_port() 函數在 AEDT 電路模擬環境中動態地加入這些端口。

### 6. **創建分析設置** ：

```python
setup = circuit.create_setup(setup_type=circuit.SETUPS.NexximLNA)
setup.props['SweepDefinition']['Data'] = 'LINC 0GHz 20GHz 2001'
```

創建一個分析設置，這裡選擇了 Nexxim LNA 類型的設置，並定義了掃描參數：從 0GHz 到 20GHz，共 2001 個點進行線性掃描。
 
### 7. **進行分析與導出結果** ：

```python
circuit.analyze()
circuit.export_touchstone(output_file='c:/demo/channel.s4p')
```
執行電路分析，然後將模擬結果以 Touchstone 格式導出到指定的位置 (`c:/demo/channel.s4p`)。
這段代碼的目的是基於已有的 S 參數模型，通過 `Circuit` 模組進行進一步的電路設計、分析並輸出結果，以便在不同的頻率範圍下了解該通道的行為。
