掃描W_Element並擷取插入損
---
這段程式碼的目的是 **在 Ansys AEDT 中建立並模擬一個傳輸線電路，透過參數掃描分析 S21（傳輸係數）的頻率響應，並使用 Matplotlib 繪製結果** 。
它的主要功能包括：
 
1. **建立 AEDT Circuit 專案** ：以 `Circuit` 類別初始化非圖形化模式的電路模擬環境。
 
2. **載入網表（Netlist）** ：從 `six_lines.sp` 文件匯入電路結構。
 
3. **新增傳輸線元件** ：在電路圖上建立一個 `TRL_W_06` 傳輸線模型，並設定參數。
 
4. **建立接地與端口** ：對應元件的接腳（pins）連接地線和介面端口。
 
5. **設定模擬條件** ： 
  - 透過 `NexximLNA` 設定頻率掃描範圍（0GHz 到 10GHz，2001 點）。
 
  - 設定 `len_t`（傳輸線長度）為變數，並進行參數掃描（0.1 到 0.5，3 個值）。
 
6. **執行模擬與數據提取** ： 
  - 針對不同的 `len_t` 值，執行模擬並擷取 `S21` 的 dB 值。

  - 使用 Matplotlib 繪製頻率響應曲線。
這段程式碼適合 **自動化電路模擬與參數掃描** ，可應用於 **SI（信號完整性）分析、傳輸線特性驗證、頻率響應測試等** 。

[W Element下載](/assets/six_lines.sp)

```python
import matplotlib.pyplot as plt
from ansys.aedt.core import Circuit

circuit = Circuit(version='2025.1', non_graphical=True)

circuit.add_netlist_datablock('d:/demo/six_lines.sp')
circuit['len_t'] = 0.1

tline = circuit.modeler.schematic.create_component(
    component_library="Transmission Lines",
    component_name="TRL_W_06",
    location=(0,0)
)
tline.set_property("ModelName", 'Inner1_GND1_')
tline.set_property("L", 'len_t')

x, y = tline.pins[0].location
circuit.modeler.schematic.create_gnd((x, y-0.0025))
x, y = tline.pins[1].location
circuit.modeler.schematic.create_gnd((x, y-0.0025))

for i in range(2, 14):
    port = circuit.modeler.schematic.create_interface_port(f'port_{i-1}', tline.pins[i].location)

setup = circuit.create_setup(setup_type=circuit.SETUPS.NexximLNA)
setup.props['SweepDefinition']['Data'] = 'LINC 0GHz 10GHz 2001'

sweep = circuit.parametrics.add('len_t', 0.1, 0.5, 3, 'LinearCount', setup.name)
sweep.analyze()


for value in [0.1, 0.3, 0.5]:
    circuit.variable_manager.set_variable('len_t', value)
    data = circuit.post.get_solution_data('dB(S21)', setup.name)
    y = data.data_real()
    x = data.primary_sweep_values
    plt.plot(x, y)
```

![2025-02-26_12-51-28](/assets/2025-02-26_12-51-28.png)