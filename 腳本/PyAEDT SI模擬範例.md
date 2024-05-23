PyAEDT SI模擬範例
---

這段程式碼的目的和功能是自動化使用Ansys HFSS（High Frequency Structure Simulator）對一個指定的PB板（Printed Circuit Board）進行3D電磁模擬。以下是對這段程式碼的詳細說明：
### 程式碼的目的
- 讀取一個指定的PCB板文件
- 定義並切割出特定信號和地網
- 使用Ansys HFSS進行3D電磁模擬，設定模擬參數
- 輸出模擬結果（Touchstone文件）
### 程式碼的功能 
1. **讀取PCB板文件** ： 
- 使用`pyedb`庫讀取並操作PCB板文件。 
2. **定義信號和地網** ： 
- 定義一組信號網（`signal_nets`）和地網（`gnd_nets`），這些網絡將被用於模擬。 
3. **切割PCB板** ：
- 切割出包含指定信號和地網的PCB板部分。 
4. **匯入HFSS進行模擬** ：
- 使用HFSS的3D Layout模組進行模擬，並對特定元件進行配置。 
5. **設置模擬參數並運行模擬** ：
- 設置模擬的Adaptive解算頻率和掃頻參數。
- 運行模擬並輸出結果。

![2024-05-24_03-20-40](/assets/2024-05-24_03-20-40.png)

### 範例碼
- AEDT2024.1
- pyaedt 9.1

```python
brd_path = r"D:\demo2\example.brd"
components = ['U2A5', 'U1A1', 'U1B5']
signal_nets = [f'M_DQ<{i}>' for i in range(0, 16)]
gnd_nets = ['GND']

from pyaedt import Hfss3dLayout
import pyedb
from pyedb import Edb
edb = Edb(brd_path)

directory = edb.directory
edb.cutout(signal_list=signal_nets, reference_list=gnd_nets, extent_type="Conforming")
edb.save_edb()
edb.close_edb()

hfss = Hfss3dLayout(specified_version='2024.1')
hfss.import_edb(directory)


ports = []
for comp_name in components:
    print(comp_name)
    comp = hfss.modeler.components[comp_name]
    comp.set_die_type(die_type=1, orientation=1)
    comp.set_solderball()

    ports.append(hfss.create_ports_on_component_by_nets(comp_name, signal_nets))

setup = hfss.create_setup()
afd = setup['AdaptiveSettings']['SingleFrequencyDataList']['AdaptiveFrequencyData']
afd['AdaptiveFrequency'] = '1GHz'
afd['MaxDelta'] = '0.02'
afd['MaxPasses'] = 5

sweep = setup.add_sweep()
sweep.change_range("LinearCount", 0, 2, 101)
setup.update()

hfss.analyze_setup(cores=6)
hfss.export_touchstone()
```
### S參數輸出

![2024-05-24_03-31-51](/assets/2024-05-24_03-31-51.png)
