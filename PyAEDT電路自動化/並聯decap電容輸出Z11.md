並聯decap電容輸出Z11
---

這段程式碼的主要目的是使用 PyAEDT 建立一個電路模擬環境，並透過讀取 Touchstone (.sNp) 檔案來分析電容元件的頻率響應。程式碼首先初始化 Circuit 物件，並設定為 non-graphical 模式，以提升運行效率。接著，它遍歷 C:/caps 目錄中的所有 Touchstone 檔案，為每個檔案建立對應的電路元件，並自動添加接地（GND），確保元件能夠正確運作。所有電容元件都與 p1 端口串聯連接，形成一個完整的電路拓撲。這樣的設計允許模擬不同電容的頻率響應行為。

在模擬設定方面，程式碼使用 NexximLNA 進行小信號網絡分析，並設定對數掃頻範圍為 1Hz 到 1GHz，共 2001 個頻率點。執行 setup.analyze() 來開始模擬後，程式碼透過 circuit.post.get_solution_data('mag(Z11)') 獲取輸入阻抗 Z11 的數據。最後，這些數據會使用 Matplotlib 以對數對數 (log-log) 座標繪製頻率對阻抗的變化圖，方便觀察電容元件在不同頻率下的行為特性。這種方法適用於高頻電路模擬與電容模型驗證，使工程師能夠快速分析元件的頻率響應特性。

![2025-03-20_09-22-20](/assets/2025-03-20_09-22-20.png)

```python
import os

import matplotlib.pyplot as plt
from pyaedt import Circuit


cap_dir = r'C:/caps'
circuit = Circuit(non_graphical=True)

caps = []

port = circuit.modeler.components.create_interface_port('p1', location=(-0.05,0))

for n, file in enumerate(os.listdir(cap_dir)):
    path = os.path.join(cap_dir, file)
    s1 = circuit.modeler.components.create_touchstone_component(path, location=(0.01, n*0.01))
    x, y = s1.pins[1].location
    circuit.modeler.components.create_gnd(location=(x, y-0.0025))
    circuit.modeler.connect_schematic_components(s1.composed_name, port.schematic_id, 1, 0, use_wire=False)


setup = circuit.create_setup(setup_type=circuit.SETUPS.NexximLNA)
setup.props['SweepDefinition']['Data'] = 'DEC 1Hz 1GHz 2001'

setup.analyze()

data = circuit.post.get_solution_data('mag(Z11)')
y = data.data_real()
x = data.primary_sweep_values
plt.figure(figsize=(6, 4))
plt.loglog(x, y)

# 標籤與標題
plt.xlabel("X (log scale)")
plt.ylabel("Y (log scale)")
plt.title("Log-Log Plot Example")
plt.grid(True, which="both", linestyle="--", linewidth=0.5)
```

![2025-03-20_09-25-02](/assets/2025-03-20_09-25-02.png)