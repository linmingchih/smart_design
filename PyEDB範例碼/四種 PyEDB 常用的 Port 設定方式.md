四種 PyEDB 常用的 Port 設定方式
---

這段程式碼示範如何使用 PyEDB 套件，在不同情境下為 PCB 中的元件與走線建立 Port，並將結果儲存成新的 AEDB 檔案。這對於後續進行 HFSS 模擬非常重要。

### 功能

* 載入並設定現有 AEDB 檔案與版本。
* 建立四種不同類型的 Port：

  1. **Component Coax Port**：針對元件特定 pin 建立同軸 Port。
  2. **Component Circuit Port**：針對元件兩個 pin 之間建立電路 Port。
  3. **Trace Gap Port**：在特定走線起點建立 Gap 類型邊緣 Port。
  4. **Trace Wave Port**：在特定走線起點建立 Wave 類型邊緣 Port。
* 儲存修改後的 AEDB 檔案。

### 流程架構

1. **初始化**：設定 AEDB 檔案路徑與 HFSS 相容的版本，建立 Edb 物件。
2. **元件 Port 建立**：

   * U3A1：以特定 pin 建立 coax port。
   * C3A18：將元件 disable，並在兩個 pin 間建立 circuit port。
3. **走線 Port 建立**：

   * RLIM1\_2：設定兩端端接風格，於起點建立 gap port。
   * SS1\_2：設定兩端端接風格，於起點建立 wave port。
4. **儲存結果**：將修改後的設計另存為新檔案。

### 補充說明

* `set_solder_ball`：會啟用 BGA 類元件的焊球模擬，讓 port 可以正確對應至球腳位置。
* `create_coax_port_on_component`：用於快速對某個 component pin 建立 HFSS 同軸 Port，常用於 power rail 測試。
* `create_circuit_port_on_pin`：用於在兩個 pins 之間建立電氣測試 Port。
* `create_edge_port`：為走線端點建立邊緣 Port，`port_type` 可指定為 'Gap' 或 'Wave'。
* `get_end_cap_style` 與 `set_end_cap_style`：這些方法用來控制走線端點的處理方式，如加開或平面終止，對 Port 的建立有影響。

### 範例程式

```python
from my_tools import scan
from pyedb import Edb

# 設定 AEDB 檔案與版本
edb_path = "D:/demo/Galileo_G87173_20454.aedb"
new_path = "D:/demo/example.aedb"
edb = Edb(edb_path, edbversion='2024.1')

# 設定元件 U3A1 並建立 coax port
u3 = edb.components.components['U3A1']
edb.components.set_solder_ball('U3A1')
edb.hfss.create_coax_port_on_component('U3A1', ['BST1_2'])

# 設定元件 C3A18 並建立 circuit port
c3 = edb.components.components['C3A18']
c3.enabled = False
p1, p2 = c3.pins.values()
edb.hfss.create_circuit_port_on_pin(p1, p2)

# 對走線 RLIM1_2 建立 gap(edge) port
trace_rlim = next(t for t in edb.modeler.paths if t.net_name == 'RLIM1_2')
_, start_style, stop_style = trace_rlim.get_end_cap_style()
trace_rlim.set_end_cap_style(type(start_style).Flat, stop_style)
trace_rlim.create_edge_port('port_1', port_type="Gap", position='Start')

# 對走線 SS1_2 建立 wave port
trace_ss = next(t for t in edb.modeler.paths if t.net_name == 'SS1_2')
_, start_style, stop_style = trace_ss.get_end_cap_style()
trace_ss.set_end_cap_style(type(start_style).Flat, stop_style)
trace_ss.create_edge_port('port_2', port_type="Wave", position='Start')

# 儲存為新的 AEDB 檔案
edb.save_edb_as(new_path)
```

![](/assets/2025-08-05_12-54-17.png)