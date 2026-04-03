將100000個rects轉成pins設pingroup及port
---

有時候我們需要將layout上的rects轉成pins，並且設pingroup及port，以下是範例程式碼，轉換所花時間約15秒左右：

### create.py
```python
from pyedb import Edb

edb = Edb(version='2024.1')

edb.stackup.add_layer('top', thickness='1um')

for i in range(10):
    for j in range(10):
        x1, y1 = (f'{10*i}um', f'{10*j}um')
        if i % 2 == 0:
            net_name = 'VDD'
        else:
            net_name = 'VSS'
            
        edb.modeler.create_rectangle('top', 
                                     net_name, 
                                     center_point = (x1, y1), 
                                     width = '5um',
                                     height = '5um', 
                                     representation_type='CenterWidthHeight')


edb.save_edb_as('d:/demo/test_100.aedb')        

```


### convert_and_port_setting.py
```python
import time
 
 
from pyedb import Edb
edb = Edb('d:/demo/test_100k.aedb', version='2024.1')
 
from System.Collections.Generic import List
from Ansys.Ansoft.Edb.Cell.Primitive import Primitive
 
t0 = time.time()
rectangles = edb.layout.rectangles
 
dotnet_list = List[Primitive]()
 
for c in rectangles:
    if hasattr(c, "_edb_object") and c._edb_object:
        dotnet_list.Add(c._edb_object)
 
ok = edb.layout._edb_object.ConvertPrimitivestoVias(dotnet_list, True)
 
 
VDD_pins = [i for i in edb.padstacks.instances.values() if i.net_name == 'VDD']
VSS_pins = [i for i in edb.padstacks.instances.values() if i.net_name == 'VSS'] 
u1 = edb.components.create(VDD_pins+VSS_pins, 'comp1')
pg1 = edb.components.create_pingroup_from_pins(VDD_pins)
pg2 = edb.components.create_pingroup_from_pins(VSS_pins)
edb.excitation_manager.create_circuit_port_on_pin_group(pg1.GetName(), pg2.GetName())
edb.save_edb_as('d:/demo/test20.aedb')
 
t1 = time.time() - t0
```
![](/assets/2026-04-03_14-38-52.jpg)