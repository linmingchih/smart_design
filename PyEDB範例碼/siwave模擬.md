siwave模擬
---

這段程式碼利用了`pyaedt`和`pyedb`這兩個Python庫來進行電子設計自動化（EDA）任務，具體地涉及到對PCB或IC封裝設計的模擬和分析。這裡是逐步分析這段程式碼的功能：
#### 初始化設置 
 
- 定義一些基本的變數，包括控制器和DRAM的名稱，以及一組數據線（`nets`）的名稱。

- 指定了一個用於儲存AEDB（ANSYS Electronic DataBase）檔案的路徑。

#### 使用pyEDB操作 
 
- 使用`Edb`類從`pyedb`庫打開一個現有的AEDB文件，這是一個包含了電子設計資料的數據庫。

- 從資料庫中檢索指定的控制器和DRAM組件。

- 對於每個組件，搜集所有連接到地線的引腳，並創建一個引腳組。

- 在這些組件上建立端口，這些端口與特定的數據線相連接。

- 創建一個訊號完整性分析的設定，並在這個設定中加入頻率掃描。

#### 模擬和分析 

- 將修改後的資料庫另存為新的AEDB檔案並關閉數據庫。
 
- 利用`Hfss3dLayout`類（來自`pyaedt`）打開這個AEDB檔案，進行非圖形化模式的高頻結構模擬器（HFSS）布局模擬。

- 執行所有設定的分析，並將結果導出為Touchstone檔案格式，這是一種常用於描述電子元件頻率特性的文件格式。

- 最後關閉HFSS項目。

#### 總結 

這段程式碼涵蓋了從數據庫讀取電子組件、設定模擬參數、進行模擬分析到導出結果的整個流程。這對於需要在PCB或IC封裝設計上進行電磁相容性和訊號完整性分析的工程師來說是非常有用的。這種自動化工具能大幅提高設計的效率和準確性。

```python
controller_name = 'U2A5'
dram_name = 'U1B5'
nets = [f'M_DQ<{i}>' for i in range(8)]
aedb_path = 'd:/demo4/test17.aedb'

from pyaedt import Hfss3dLayout
from pyedb import Edb

edb = Edb('d:/demo4/Galileo_G87173_204162.aedb', edbversion='2024.1')

controller = edb.components[controller_name]
gnd_pins = [j for i, j in controller.pins.items() if j.net.name=='GND']
pg_gnd = edb.core_components.create_pingroup_from_pins(gnd_pins)
edb.core_components.create_port_on_component(controller_name, nets)

dram = edb.components[dram_name]
gnd_pins = [j for i, j in dram.pins.items() if j.net.name=='GND']
dram_gnd = edb.core_components.create_pingroup_from_pins(gnd_pins)
edb.core_components.create_port_on_component(dram_name, nets)

setup1 = edb.create_siwave_syz_setup()

setup1.add_frequency_sweep()
edb.save_as(aedb_path)
edb.close_edb()

hfss = Hfss3dLayout(specified_version='2024.1', non_graphical=True, projectname=aedb_path)
hfss.analyze_all()
hfss.export_touchstone()
hfss.close_project()
```
#### 輸出S參數
![2024-08-12_16-11-29](/assets/2024-08-12_16-11-29.png)