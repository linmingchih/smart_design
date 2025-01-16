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
 
- 利用`Hfss3dLayout`類（來自`pyaedt`）打開這個AEDB檔案，進行非圖形化模式的SIwave模擬器（SIwave Solver）布局模擬。

- 執行所有設定的分析，並將結果導出為Touchstone檔案格式，這是一種常用於描述電子元件頻率特性的文件格式。

- 最後關閉HFSS項目。

#### 總結 

這段程式碼涵蓋了從數據庫讀取電子組件、設定模擬參數、進行模擬分析到導出結果的整個流程。這對於需要在PCB或IC封裝設計上進行電磁相容性和訊號完整性分析的工程師來說是非常有用的。這種自動化工具能大幅提高設計的效率和準確性。

```python
# 定義控制器名稱和記憶體名稱
controller_name = 'U2A5'
dram_name = 'U1B5'

# 定義訊號網路名稱 (從M_DQ<0>到M_DQ<7>)
nets = [f'M_DQ<{i}>' for i in range(8)]

# 指定AEDB專案路徑
aedb_path = 'd:/demo4/test37.aedb'

# 匯入必要的模組
from pyaedt import Hfss3dLayout
from pyedb import Edb


# 初始化 EDB，載入指定的.aedb檔案
edb = Edb(r"D:\OneDrive - ANSYS, Inc\Models\EDB\Galileo_G87173_20454.aedb", edbversion='2024.1')

# 對控制器和記憶體進行處理
for comp_name in [controller_name, dram_name]:
    # 取得元件物件
    comp = edb.components[comp_name]
    # 找出與接地 (GND) 相關的接腳
    gnd_pins = [pin_name for pin_name, pin_obj in comp.pins.items() if pin_obj.net.name == 'GND']
    
    # 建立接地的接腳群組 (Pin Group)
    _, pg_gnd = edb.siwave.create_pin_group(comp_name, gnd_pins, comp_name + '_ref')
    # 為接地群組建立端子，並設定特性阻抗為50歐姆
    termial_gnd = pg_gnd.create_port_terminal(50)
    
    # 處理與訊號網路相關的接腳
    for i, j in comp.pins.items():
        if j.net.name in nets:
            # 建立訊號接腳群組
            _, pg_sig = edb.siwave.create_pin_group(comp_name, [i], f'p_{i}')
            # 為訊號群組建立端子，並設定特性阻抗為50歐姆
            termial_sig = pg_sig.create_port_terminal(50)
            # 將訊號端子參考設為接地端子
            termial_sig.SetReferenceTerminal(termial_gnd)

# 建立Siwave Syz設置
setup1 = edb.create_siwave_syz_setup()

# 設定頻率掃描範圍
sweep = setup1.add_frequency_sweep()
frequency_list = [
    ["linear count", "0", "1kHz", 1],      # 線性掃描，從0到1kHz，共1點
    ["log scale", "1kHz", "0.1GHz", 10],  # 對數掃描，從1kHz到0.1GHz，共10點
    ["linear scale", "0.1GHz", "10GHz", "0.1GHz"],  # 線性掃描，從0.1GHz到10GHz，步進0.1GHz
]
sweep.set_frequencies(frequency_list)

# 儲存修改後的AEDB專案
edb.save_as(aedb_path)
# 關閉EDB專案
edb.close_edb()

# 初始化HFSS 3D Layout模組，並指定非圖形模式
hfss = Hfss3dLayout(specified_version='2024.1', 
                    non_graphical=True, 
                    projectname=aedb_path, 
                    remove_lock=True)

# 開始分析
hfss.analyze()
# 將結果匯出為Touchstone格式
hfss.export_touchstone()
# 關閉HFSS專案
hfss.close_project()

```
#### 輸出S參數
![2024-08-12_16-11-29](/assets/2024-08-12_16-11-29.png)