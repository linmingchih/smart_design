第3章 使用 PyAEDT 進行 TDR（時域反射）分析
---

這個範例中使用了電路模擬器（Circuit）來設計和分析一個差分時域反射計（TDR）的設置。以下是這段代碼各部分的功能說明：

> [pcie.s4p下載](https://github.com/linmingchih/smart_design/blob/main/assets/pcie.s4p)

1. **初始化電路模擬器** : 
  - `Circuit(non_graphical=True)`：創建一個新的Circuit對象，`non_graphical=True`表示在無圖形介面模式下運行，適用於腳本化和自動化流程。
 
2. **導入和創建元件** : 
  - `create_model_from_touchstone`：從Touchstone文件（這裡是`pcie.s4p`）導入一個模型。Touchstone文件通常用於描述網絡參數，如S參數。
 
  - `create_touchstone_component`：在電路中創建一個基於導入的Touchstone文件的元件。
 
  - `create_component`和`create_resistor`：創建其他需要的元件，包括探針和電阻。
 
3. **建立連接** : 
  - `connect_schematic_components`：將元件按指定的端口連接起來。例如，將Touchstone元件的端口連接到探針和電阻上，並將電阻接地。
 
4. **設置分析** : 
  - `create_setup`：創建一個新的仿真設置，指定仿真類型為`NexximTransient`，設定仿真的時間範圍。
 
  - `analyze_all`：執行所有設置的仿真。
 
5. **生成和導出報告** : 
  - `create_report`：生成報告，此處生成差分時域反射報告。
 
  - `export_report_to_jpg`：將報告導出為JPEG格式，儲存至指定路徑。

這個代碼的用途在於透過腳本自動設計和分析電子電路，特別是在信號完整性分析中常用的時域反射測量。這種自動化流程可以大幅節省手動設置和分析的時間，並且可以方便地集成到更大的設計和測試流程中。

```python
from pyaedt import Circuit

circuit = Circuit(non_graphical=True)

circuit.modeler.components.create_model_from_touchstone(r"D:\Downloads\pcie.s4p")

#%%
s1 = circuit.modeler.components.create_touchstone_component('pcie')
probe = circuit.modeler.components.create_component('a1', 'Probes','TDR_Differential_Ended')
rp = circuit.modeler.components.create_resistor()
rn = circuit.modeler.components.create_resistor()

g1 = circuit.modeler.components.create_gnd()
g2 = circuit.modeler.components.create_gnd()

circuit.modeler.connect_schematic_components(s1.composed_name, probe.composed_name, 1, 1)
circuit.modeler.connect_schematic_components(s1.composed_name, probe.composed_name, 2, 2)

circuit.modeler.connect_schematic_components(s1.composed_name, rp.composed_name, 3, 1)
circuit.modeler.connect_schematic_components(s1.composed_name, rn.composed_name, 4, 1)

circuit.modeler.connect_schematic_components(g1.composed_name, rp.composed_name, 1, 2)
circuit.modeler.connect_schematic_components(g2.composed_name, rn.composed_name, 1, 2)

setup = circuit.create_setup('mysetup', 'NexximTransient')
setup.props['TransientData'] = ['10ps', '10ns']
circuit.analyze_all()

report = circuit.post.create_report(f"O(A{probe.id}:zdiff)", 
                                    domain='Time',
                                    primary_sweep_variable='Time',
                                    variations={"Time": ["All"]},
                                    plotname='differential_tdr')
circuit.post.export_report_to_jpg('d:/demo',  report.plot_name)
```
![differential_tdr](/assets/differential_tdr.jpg)