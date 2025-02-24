掃描傳輸線模型並輸出S參數
---
此程式使用 PyAEDT 建立一個 Circuit 設計，並執行頻率響應模擬。它載入 "Ideal Distributed" 庫中的 TRLK_NX 傳輸線元件，並設定屬性 "A" 為 0.01。接著，程式在電路圖上創建兩個介面端口 a3 和 a4，設定 NexximLNA 類型的模擬設置，頻率掃描範圍從 0GHz 到 20GHz，共 2001 點。最後，迴圈修改傳輸線參數 "P"（長度），範圍從 10mm 到 100mm，每次變化 10mm，執行模擬並輸出 .s4p 檔案至 d:/demo/。
```python
from pyaedt import Circuit

circuit = Circuit(specified_version="2025.1")

tline = circuit.modeler.schematic.create_component(
    component_library="Ideal Distributed",
    component_name="TRLK_NX",
    location=(0,-0.00625/2)
)

tline.set_property("A", '0.01')
circuit.modeler.schematic.create_interface_port('a3', location=(-0.00625,0))
circuit.modeler.schematic.create_interface_port('a4', location=(0.00625,0))

#%%
setup = circuit.create_setup(setup_type=circuit.SETUPS.NexximLNA)
setup.props['SweepDefinition']['Data'] = 'LINC 0GHz 20GHz 2001'

for i in range(10, 110, 10):
    tline.set_property("P", f'{i}mm')
    circuit.analyze()
    circuit.export_touchstone(output_file=f'd:/demo/{i}mm.s4p')

```

![2025-02-25_05-38-47](/assets/2025-02-25_05-38-47.png)