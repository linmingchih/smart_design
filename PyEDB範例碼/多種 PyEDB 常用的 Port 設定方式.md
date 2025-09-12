多種 PyEDB 常用的 Port 設定方式
---

這段程式碼示範如何使用 `pyedb` 套件，針對一個 AEDB 電路板檔案，建立五種不同類型的 Port，包括：同軸埠（Coax Port）、電路埠（Circuit Port）、Gap 埠、Wave 埠，以及 Pin Group Port，並將設定結果另存為新的 AEDB 檔案。

### 功能

* 載入並初始化指定版本的 AEDB 專案
* 對特定元件建立 Coax 與 Circuit Port
* 對指定走線建立 Gap 與 Wave Port
* 以 Pin Group 的方式建立 Port 並指定參考端子
* 儲存修改後的 AEDB 專案

### 流程架構

1. 載入 AEDB 檔案，指定版本為 2024.1
2. 對元件 `U3A1` 設定焊球並建立 Coax Port
3. 對電容元件 `C3A18` 建立 Circuit Port（並停用該元件）
4. 對走線 `RLIM1_2` 建立 Gap Port（邊緣埠）
5. 對走線 `SS1_2` 建立 Wave Port（波導埠）
6. 建立 `U2B1` 上 AVIN1 與 GND 的 Pin Group，並用這兩組建立 Pin Group Port，設定阻抗與參考端
7. 將所有修改儲存到新的 AEDB 專案檔

### 補充說明

* `create_coax_port_on_component`：自動尋找元件特定 pin，產生一個同軸形式的激發端口。
* `create_circuit_port_on_pin`：以兩個 pin 之間建立電路端口，常用於電容或電感等二端元件。
* `create_edge_port`：在走線的端點設定為 port，可以選擇 "Gap"（縫隙）或 "Wave"（波導）形式。
* `create_pin_group_on_net`：將同一網路的多個接腳群組成一個 Pin Group，常用於多腳接地或電源組合。
* `SetReferenceTerminal`：設定 port 的參考地，對於電源與地的激發端口特別重要。

### 範例程式

```python
from my_tools import scan
from pyedb import Edb

# 設定 AEDB 檔案與版本
edb_path = "D:/demo/Galileo_G87173_204.aedb"
new_path = "D:/demo/example.aedb"
edb = Edb(edb_path, edbversion='2024.1')

# Coax Port on U3A1
u3 = edb.components.components['U3A1']
edb.components.set_solder_ball('U3A1')
edb.hfss.create_coax_port_on_component('U3A1', ['BST1_2'])

# Circuit Port on C3A18
c3 = edb.components.components['C3A18']
c3.enabled = False
p1, p2 = c3.pins.values()
edb.hfss.create_circuit_port_on_pin(p1, p2)

# Gap Port on trace RLIM1_2
trace_rlim = next(t for t in edb.modeler.paths if t.net_name == 'RLIM1_2')
_, start_style, stop_style = trace_rlim.get_end_cap_style()
trace_rlim.set_end_cap_style(type(start_style).Flat, stop_style)
trace_rlim.create_edge_port('port_1', port_type="Gap", position='Start')

# Wave Port on trace SS1_2
trace_ss = next(t for t in edb.modeler.paths if t.net_name == 'SS1_2')
_, start_style, stop_style = trace_ss.get_end_cap_style()
trace_ss.set_end_cap_style(type(start_style).Flat, stop_style)
trace_ss.create_edge_port('port_2', port_type="Wave", position='Start')

# Pin Group Port on U2B1
pgname1, pg1 = edb.siwave.create_pin_group_on_net('U2B1', 'AVIN1')
pgname2, pg2 = edb.siwave.create_pin_group_on_net('U2B1', 'GND')

terminal1 = pg1.create_port_terminal(50)
terminal2 = pg2.create_port_terminal(50)

terminal1.SetReferenceTerminal(terminal2)
terminal1.SetName('port_AVIN1')

# 儲存新的 AEDB
edb.save_edb_as(new_path)
```


![](/assets/2025-08-05_12-54-17.png)

![](/assets/2025-09-12_09-38-34.png)