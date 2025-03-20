HFSS 差分對建模
---

這段程式碼使用 Ansys AEDT (HFSS) 來建立並模擬一個簡單的高頻結構，主要用於分析差分信號的傳輸行為。首先，程式初始化 HFSS 2024.2 版本並設定模型單位為毫米，使用 Terminal 解法類型，並啟用自動因果材料設定。接著，建立一個新材料 "molding"，設定其導磁率為 3.0，介電損耗正切值為 0.02，然後使用這個材料建立包裝體（pkg）。此外，程式定義了一對差分信號導體（pos、neg）、接地層（gnd）及包圍結構的空氣盒（air_box），確保模擬邊界條件的正確性。

在邊界條件設定方面，程式將空氣盒指定為輻射邊界，以模擬開放空間中的電磁場分布。然後，在空氣盒的上下邊界分別設置波導埠（wave port），並將其與接地層 (gnd) 連接，以便進行差分信號分析。對於每個波導埠，程式自動取得其內部的正負端口，並將其分別設定為差分模式（diff1, diff2）和共模模式（comm1, comm2），這樣可以在模擬過程中直接分析差分訊號的行為。

最後，程式建立一個模擬設置，並定義頻率掃描範圍從 0.01 GHz 到 5 GHz，每次步進 0.05 GHz，同時設定計算頻率為 2 GHz，並將基底函數順序設為 -1（代表Mixed Order）。設定完成後，程式啟動 4 核心運行模擬，並從結果中提取 S 參數 "dB(St(diff2, diff1))"，然後繪製頻率響應曲線，以視覺化分析結果。這段程式碼的目的是進行差分信號的電磁模擬，並獲取其頻率響應特性，以評估其在不同頻率下的傳輸效果。

> [附註] **Pyaedt 版本為 0.14.0**
```python
from ansys.aedt.core import Hfss
import matplotlib.pyplot as plt

hfss = Hfss(version='2024.2')
hfss.modeler.model_units = 'mm'
hfss.solution_type = 'Terminal'
hfss.change_automatically_use_causal_materials()

m = hfss.materials.add_material('molding')
m.permeability = 3.0
m.dielectric_loss_tangent = 0.02

molding = hfss.modeler.create_box((-10,0,-1), (20,10,2), name='pkg', material='molding')
pos = hfss.modeler.create_box((0.5,0,0), (1,10,0.5), material='copper')
neg = hfss.modeler.create_box((-0.5,0,0), (-1,10,0.5), material='copper')
gnd = hfss.modeler.create_box((-10,0,-1), (20,10,-0.1), material='copper')
air_box = hfss.modeler.create_box((-10,0,-1), (20,10,5), material='air')

hfss.assign_radiation_boundary_to_objects(air_box)

port = hfss.wave_port(air_box.bottom_face_y, gnd)
t_pos, t_neg = port.children.keys()
hfss.set_differential_pair(t_pos, t_neg, differential_mode='diff1', common_mode='comm1')

port = hfss.wave_port(air_box.top_face_y, gnd)
t_pos, t_neg = port.children.keys()
hfss.set_differential_pair(t_pos, t_neg, differential_mode='diff2', common_mode='comm2')

setup = hfss.create_setup()
setup.create_linear_step_sweep('GHz', 0.01, 5, 0.05)
setup.props['Frequency'] = '2GHz'
setup.props['BasisOrder'] = -1
setup.update()

hfss.analyze(cores=4)

data = hfss.post.get_solution_data('dB(St(diff2, diff1))')
y = data.data_real()
x = data.primary_sweep_values

plt.grid()
plt.plot(x, y)

```

![2025-03-21_02-44-24](/assets/2025-03-21_02-44-24.png)

![2025-03-21_02-47-37](/assets/2025-03-21_02-47-37.png)