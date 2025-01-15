使用 EDB 實現 SIwave DC-IR 分析自動化
---
腳本專注於教學如何使用 Python 的 pyedb 模組操作電子設計數據庫（EDB），並通過 SIwave 執行直流DC-IR分析。透過這個腳本，學員將學習如何自動化處理 PCB 設計數據，包括檢索元件與網路資訊、生成電源樹，以及設定電壓源與電流源以進行電氣性能分析。

腳本會逐步演示如何從初始化 EDB 開始，載入設計數據後檢索所需資訊，如元件引腳位置和網路連接情況。接著，學員將學會清理未使用的元件和網路，以提高模擬效率。同時還會介紹如何使用方法來獲取直流連接的電源網路，並生成完整的電源樹。

最後，學員將學會如何保存修改後的設計、運行 SIwave 分析並匯出結果供後續分析使用。腳本還展示了如何清理臨時檔案以保持環境整潔。

```python
# 匯入所需模組
import os
import tempfile
import time
import pyedb
from pyedb.misc.downloads import download_file

# 建立臨時目錄並下載檔案
temp_dir = 'c:/demo'
targetfile = download_file("edb/ANSYS-HSD_V1.aedb", destination=temp_dir)
siwave_file = os.path.join(os.path.dirname(targetfile), "ANSYS-HSD_V1.siw")
aedt_file = targetfile[:-4] + "aedt"
print(targetfile)

# 啟動 Ansys Electronics Database (EDB)
if os.path.exists(aedt_file):
    os.remove(aedt_file)

# 選擇 EDB 版本
edb_version = "2024.1"
print(f"EDB 版本: {edb_version}")
edb = pyedb.Edb(edbpath=targetfile, edbversion=edb_version)

# 列出網路與元件的數量
print("網路數量: {}".format(len(edb.nets.netlist)))
start = time.time()
print("元件數量: {}".format(len(edb.components.instances.keys())))
print("處理時間: {:.2f} 秒".format(time.time() - start))

# 獲取特定元件的所有引腳位置
pins = edb.components["U2"].pins
count = 0
for pin in edb.components["U2"].pins.values():
    if count < 10:  # 僅列印前 10 個引腳座標
        print(pin.position)
    elif count == 10:
        print("...還有更多。")
    count += 1

# 獲取與特定元件相關的網路連接資訊
connections = edb.components.get_component_net_connection_info("U2")
n_print = 0  # 設定列印的最大行數
print_max = 15
for m in range(len(connections["pin_name"])):
    ref_des = connections["refdes"][m]
    pin_name = connections["pin_name"][m]
    net_name = connections["net_name"][m]
    if net_name != "" and (n_print < print_max):
        print(f"{ref_des}, pin {pin_name} -> 網路 \"{net_name}\"")
        n_print += 1
    elif n_print == print_max:
        print("...還有更多。")
        n_print += 1

# 計算電氣連接
rats = edb.components.get_rats()

# 獲取所有直流連接的電源網路
GROUND_NETS = ["GND", "GND_DP"]
dc_connected_net_list = edb.nets.get_dcconnected_net_list(GROUND_NETS)
for pnets in dc_connected_net_list:
    print(pnets)

# 生成電源樹
VRM = "U1"
OUTPUT_NET = "AVCC_1V3"
powertree_df, component_list_columns, net_group = edb.nets.get_powertree(OUTPUT_NET, GROUND_NETS)

# 列印電源樹資訊
print_columns = ["refdes", "pin_name", "component_partname"]
ncol = [component_list_columns.index(c) for c in print_columns]
print("\t".join(print_columns).replace("pin_name", "pin"))
for el in powertree_df:
    s = ""
    count = 0
    for e in el:
        if count in ncol:
            s += f"{e}\t"
        count += 1
    print(s.rstrip())

# 移除未使用的元件
edb.components.delete_single_pin_rlc()
edb.components.delete("C380")  # 顯式刪除特定元件
edb.nets.delete("PDEN")  # 顯式刪除特定網路

# 列印堆疊結構的頂部和底部層資訊
top, top_el, bot, bot_el = edb.stackup.limits()
print(f"頂層名稱: \"{top}\", 高度: {top_el * 1e3:.2f} mm")
print(f"底層名稱: \"{bot}\", 高度: {bot_el * 1e3:.2f} mm")

# 設置 SIwave DCIR 分析
edb.siwave.create_voltage_source_on_net("U1", "AVCC_1V3", "U1", "GND", 1.3, 0, "V1")
edb.siwave.create_current_source_on_net("IC2", "NetD3_2", "IC2", "GND", 1.0, 0, "I1")
setup = edb.siwave.add_siwave_dc_analysis("myDCIR_4")
setup.use_dc_custom_settings = True
setup.set_dc_slider = 0
setup.add_source_terminal_to_ground("V1", 1)

# 保存修改並執行分析
edb.save_edb()
edb.nets.plot(None, "1_Top", plot_components_on_top=True)
siw_file = edb.solve_siwave()

# 匯出 DC-IR 分析結果
outputs = edb.export_siwave_dc_results(siw_file, setup.name)

# 關閉 EDB
edb.close_edb()
```
#### 版圖輸出
![2025-01-16_04-59-22](/assets/2025-01-16_04-59-22.png)

#### 資料輸出
![2025-01-16_05-00-34](/assets/2025-01-16_05-00-34.png)

#### HTML報告
![2025-01-16_05-02-32](/assets/2025-01-16_05-02-32.png)