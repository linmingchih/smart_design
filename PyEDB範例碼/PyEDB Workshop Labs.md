PyEDB Workshop Labs
---
>:link: **範例edb下載**
[example_edb.aedb](assets/example_edb.aedb.zip)

### Lab 1. 以阻值分類所有電阻
```python
from collections import defaultdict
from pyedb import Edb

edb = Edb("C:\demo\example_edb.aedb", edbversion='2024.1')
resistors = edb.components.resistors

table = defaultdict(list)
for name, obj in resistors.items():
    table[obj.value].append(name)
```
![2024-10-11_13-21-16](/assets/2024-10-11_13-21-16.png)


### Lab 2. 找出V3P3_S5上的去耦合電容名稱及電容值
```python
from collections import defaultdict
from pyedb import Edb

edb = Edb("C:\demo\example_edb.aedb", edbversion='2024.1')

group1 = edb.components.get_components_from_nets('V3P3_S5')
group2 = edb.components.get_components_from_nets('GND')

decaps = []
for name in set(group1) & set(group2):
    obj = edb.components.get_component_by_name(name)
    if obj.type == 'Capacitor':
        decaps.append((name, obj.value))
```

![2024-10-11_13-29-51](/assets/2024-10-11_13-29-51.png)

### Lab 3. 建立新材料並設定疊構
```python
from pyedb import Edb

edb = Edb(edbversion='2024.1')

material_info = {('metal1', 'conductor'): 5e8,
                 ('metal2', 'conductor'): 5e8,
                 ('epoxy1', 'ds'):(4, 0.02, 1),
                 ('epoxy2', 'ds'):(3.8, 0.015, 1)}


layers_info = {('layer1', 'signal'):('0.05mm', 'metal1', 1.6, '0.6um', '3.1'),
               ('dielectric12', 'dielectric'):('0.28mm', 'epoxy1'),
               ('layer2', 'signal'):('0.05mm', 'metal2', 1.7, '0.8um', '3.4'),
               ('dielectric23', 'dielectric'):('0.43mm', 'epoxy2'),
               ('layer3', 'signal'):('0.05mm', 'metal2', 1.7, '0.8um', '3.4'),
               ('dielectric34', 'dielectric'):('0.28mm', 'epoxy1'),
               ('layer4', 'signal'):('0.05mm', 'metal1', 1.6, '0.6um', '3.1')}


for (name, _type), prop in material_info.items():
    if _type == 'conductor':
        conductivity = prop
        edb.materials.add_conductor_material(name, conductivity)
    elif _type == 'ds':
        permittivity, loss_tangent, test_frequency = prop
        edb.materials.add_djordjevicsarkar_dielectric(name, permittivity, loss_tangent, test_frequency)

for (name, _type), prop in layers_info.items():
    if _type == 'signal':
        thickness, material, etch_factor, radius, ratio = prop
        layer = edb.stackup.add_layer(name, 
                                      layer_type=_type, 
                                      material=material, 
                                      thickness=thickness,
                                      enable_roughness=True,
                                      method='add_on_bottom')
        layer.etch_factor=etch_factor
        layer.assign_roughness_model("huray", radius, ratio, apply_on_surface="all")
    
    elif _type == 'dielectric':
        thickness, material = prop
        edb.stackup.add_layer(name, 
                              layer_type=_type, 
                              material=material, 
                              thickness=thickness,
                              method='add_on_bottom')



edb.save_as('c:/demo/lab3.aedb')
edb.stackup.export_stackup('c:/demo/lab3.xml')
edb.close_edb()
```
![2024-10-11_13-46-39](/assets/2024-10-11_13-46-39.png)

### Lab 4. 建立差分對結構並設置WavePort
```python
from pyedb import Edb
from functools import partial

edb = Edb(edbversion='2024.1')
edb.core_stackup.load('c:/demo/lab3.xml')

create_trace = partial(edb.modeler.create_trace, layer_name='layer2', width='1mm', start_cap_style='Flat', end_cap_style='Flat')
tp = create_trace([('0mm','-1mm'), ('10mm', '-1mm')], net_name='pos')
tn = create_trace([('0mm','1mm'), ('10mm', '1mm')], net_name='neg')

edb.modeler.create_rectangle('layer1', 'GND', ('0mm', '-5mm'), ('10mm', '5mm'))
edb.modeler.create_rectangle('layer3', 'GND', ('0mm', '-5mm'), ('10mm', '5mm'))

edb.core_hfss.create_differential_wave_port(tp, ('0mm', '-1mm'), tn, ('0mm', '1mm'), horizontal_extent_factor=2)
edb.core_hfss.create_differential_wave_port(tp, ('10mm', '-1mm'), tn, ('10mm', '1mm'), horizontal_extent_factor=2)

edb.save_as('c:/demo/lab4.aedb')
edb.close_edb()
```
![2024-10-11_14-15-21](/assets/2024-10-11_14-15-21.png)

### Lab 5. 設置 3D Layout SI 模擬
```python
from pyedb import Edb
from ansys.aedt.core import Hfss3dLayout
edb = Edb('c:/demo/lab4.aedb', edbversion='2024.1')
setup = edb.core_hfss.configure_hfss_analysis_setup()

sim_setup = edb.new_simulation_configuration()
sim_setup.solver_type = sim_setup.SOLVER_TYPE.Hfss3dLayout
sim_setup.ac_settings.start_freq = "0GHz"
sim_setup.ac_settings.stop_freq = "5GHz"
sim_setup.ac_settings.step_freq = "0.1GHz"
edb.build_simulation_project(sim_setup)
edb.save_edb_as('c:/demo/lab5.aedb')
edb.close_edb()

hfss = Hfss3dLayout('c:/demo/lab5.aedb', version="2024.1")
hfss.set_export_touchstone(True, 'c:/demo')
hfss.analyze()
hfss.close_desktop()
```
![2024-10-11_14-46-15](/assets/2024-10-11_14-46-15.png)

### Lab 6. 設置Siwave SYZ SI模擬
```python
controller_name = 'U2A5'
dram_name = 'U1B5'
nets = [f'M_DQ<{i}>' for i in range(8)]

import pyaedt
from pyaedt import Hfss3dLayout
from pyedb import Edb

edb = Edb('c:/demo/example_edb.aedb', edbversion='2024.1')

controller = edb.components[controller_name]
gnd_pins = [j for i, j in controller.pins.items() if j.net.name=='GND']
pg_gnd = edb.core_components.create_pingroup_from_pins(gnd_pins)
edb.core_components.create_port_on_component(controller_name, nets, reference_net='GND')

dram = edb.components[dram_name]
gnd_pins = [j for i, j in dram.pins.items() if j.net.name=='GND']
dram_gnd = edb.core_components.create_pingroup_from_pins(gnd_pins)
edb.core_components.create_port_on_component(dram_name, nets, reference_net='GND')

setup1 = edb.create_siwave_syz_setup()

setup1.add_frequency_sweep()
edb.save_as('c:/demo/lab6.aedb')
edb.close_edb()

hfss = Hfss3dLayout(specified_version='2024.1', 
                    non_graphical=True, 
                    projectname='c:/demo/lab6.aedb', 
                    remove_lock=True)
hfss.analyze()
hfss.export_touchstone()
hfss.close_project()
```

![2024-10-11_15-00-14](/assets/2024-10-11_15-00-14.png)
