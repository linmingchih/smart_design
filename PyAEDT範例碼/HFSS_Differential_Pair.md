HFSS Differential Pair
---
```python
import pyaedt
print(pyaedt.version)

# this script is developed on pyaedt.version == 0.10.1

l = 10
w = 0.5
t = 0.1
gap = 0.5
h = 0.3

from pyaedt import Hfss

hfss = Hfss(version='2024.1')

hfss.modeler.model_units = 'mm'
hfss.modeler.create_polyline([(0,0,0), (l,0,0)],
                             xsection_type='Rectangle',
                             xsection_height=t,
                             xsection_width=w,
                             material='copper')

hfss.modeler.create_polyline([(0,w+gap,0), (l,w+gap,0)],
                             xsection_type='Rectangle',
                             xsection_height=t,
                             xsection_width=w,
                             material='copper')

box = hfss.modeler.create_box((0,-1-w/2,-t/2), 
                              (l, 2*w+gap+2, -h),
                              material = 'FR4_epoxy')

gnd = hfss.modeler.create_object_from_face(box.bottom_face_z)
hfss.modeler.thicken_sheet(gnd, 0.01)
gnd.material_name = 'copper'
region = hfss.modeler.create_region([0,0,0,0,500,0])

port1 = hfss.wave_port(region.bottom_face_x, gnd.name)
port2 = hfss.wave_port(region.top_face_x, gnd.name)
#%%
hfss.set_differential_pair(*[i for i in port1.object_properties.children],differential_mode='d1')
hfss.set_differential_pair(*[i for i in port2.object_properties.children],differential_mode='d2')

setup = hfss.create_setup()
setup.create_linear_step_sweep('GHz',0.001,2,0.1)

hfss.analyze(core=4)
data = hfss.post.get_solution_data('dB(St(d2,d1))')
sdd21 = data.data_real()
freq = data.primary_sweep_values

hfss.post.create_report('dB(St(d2,d1))')

import matplotlib.pyplot as plt
plt.plot(freq, sdd21)
plt.grid()
plt.show()
```

![2024-09-12_10-44-39](/assets/2024-09-12_10-44-39.png)