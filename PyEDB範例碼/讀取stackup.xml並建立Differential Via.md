讀取stackup.xml並建立Differential Via
---
這段腳本的目的在於使用 ANSYS AEDT 的 Edb 模組，為多層 PCB 信號層自動生成一個帶有特定形狀和參數的平面結構以及針腳佈局。腳本先定義了所需的孔徑、焊盤直徑、反焊盤直徑、間隔及間隔角度等幾何參數。然後，通過讀取現有的堆疊層結構，腳本為每個信號層創建了接地平面並且設置了一些矩形和圓形孔洞，模擬特定的過孔結構。接著，腳本使用已定義的 padstack，並將過孔放置在指定的位置，包括針對不同角度的接地過孔佈局。最後，腳本生成隨機命名的 AEDB 檔案，並將設計保存到該檔案中。
```python
dss = 0.3e-3

d_drill = 0.05e-3
d_pad = 0.15e-3
d_anti = 0.2e-3
d_sg = 0.4e-3 
degree_sg = [-45, 0, 45]

import os
import random
import string
from pyedb import Edb
from ansys.aedt.core import Hfss3dLayout
from math import sin, cos, radians

def generate_random_filename():
    # Generate 8 random alphanumeric characters
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    # Construct the full file path
    filename = f'd:/demo/{random_string}.aedb'
    return filename


edb = Edb(edbversion='2024.1')
edb.core_stackup.load(r"D:\demo\layers.xml")

signal_layers = list(edb.stackup.signal_layers.keys())

for layer in signal_layers:
    plane = edb.modeler.create_rectangle(layer, 'GND', (-1e-3,-0.5e-3), (1e-3, 0.5e-3))
    void1 = edb.modeler.create_rectangle(layer, 'GND', (-dss/2, -d_anti/2), (dss/2, d_anti/2))
    void2 = edb.modeler.create_circle(layer, -dss/2, 0, d_anti/2, net_name='GND')
    void3 = edb.modeler.create_circle(layer, dss/2, 0, d_anti/2, net_name='GND')
    plane.subtract([void1, void2, void3])
    #edb.modeler.
    #edb.modeler.add_void(plane, [void])

mypadstack = edb.padstacks.create_padstack('mypadstack',
                                           holediam=d_drill,
                                           paddiam=d_pad,
                                           antipaddiam=d_anti,
                                           startlayer=signal_layers[0], 
                                           endlayer=signal_layers[-1],
                                           )

#%%
edb.padstacks.place_padstack((dss/2, 0), 'mypadstack', net_name='pos_net')
edb.padstacks.place_padstack((-dss/2, 0), 'mypadstack', net_name='neg_net')

for theta in degree_sg:
    theta = radians(theta)
    edb.padstacks.place_padstack((dss/2+d_sg*cos(theta), d_sg*sin(theta)), 'mypadstack', net_name='GND')

for theta in degree_sg:
    theta = radians(theta)
    edb.padstacks.place_padstack((-dss/2-d_sg*cos(theta), d_sg*sin(theta)), 'mypadstack', net_name='GND')

edb_path = generate_random_filename()
edb.save_edb_as(edb_path)
```

![2024-09-21_19-07-37](/assets/2024-09-21_19-07-37.png)