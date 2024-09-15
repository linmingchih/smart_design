Workshop Lab Example Code
---

### Lab 0. 環境安裝

``` bash
rmdir /S /Q c:\myvenv
cd C:\Program Files\AnsysEM\v241\Win64\commonfiles\CPython\3_10\winx64\Release\python
.\python -m venv c:\myvenv
cd c:\myvenv\Scripts
activate
pip install pyaedt
pip install ansys-optislang-core
pip install spyder
pip list
echo 'Installation Finished'
```


### Lab 1. Python Node 設定
```python
if not 'OSL_REGULAR_EXECUTION' in locals(): 
    OSL_REGULAR_EXECUTION = False


if not OSL_REGULAR_EXECUTION:
    x1 = 0.1
    x2 = 0.1

y = (x1 -1)**2 + (x2 -3)**2

```

### Lab 2. PyAEDT 建模及設定
```python
w = 0.5
dw = 0.1
t = 0.1
gap = 0.5
h = 0.3
sw = 1
sl = 2
n = 10

def get_cell(x):
    return [(x,sl,0),(x+sw,sl,0),(x+sw,0,0),(x+2*sw,0,0)]

pts = [(0,0,0), (2*sw,0,0)]
for i in range(n):
    x = pts[-1][0]
    pts += get_cell(x)

x, y, z = pts[-1]
pts.append((x+sw, y, z))

from pyaedt import Hfss
hfss = Hfss(version='2024.1')

hfss.modeler.model_units = 'mm'
line = hfss.modeler.create_polyline(pts,
                                    xsection_type='Isosceles Trapezoid',
                                    xsection_height=t,
                                    xsection_width=w,
                                    xsection_topwidth=w-dw,
                                    material='copper')

x0, y0, z0, x1, y1, z1 = line.bounding_box

box = hfss.modeler.create_box((0, y0-y1-w/2,-t/2), 
                              (x1, 3*(y1-y0), -h),
                              material = 'FR4_epoxy')

gnd = hfss.modeler.create_object_from_face(box.bottom_face_z)
hfss.modeler.thicken_sheet(gnd, 0.01)
gnd.material_name = 'copper'
region = hfss.modeler.create_region([0,0,0,0,1000,0])

port1 = hfss.wave_port(region.bottom_face_x, gnd.name)
port2 = hfss.wave_port(region.top_face_x, gnd.name)

setup = hfss.create_setup()
setup.props['Frequency'] = '2GHz'
setup.create_linear_step_sweep('GHz',0.001,2,0.1)

hfss.analyze(cores=4)
data = hfss.post.get_solution_data('dB(S(2,1))')
sdd21 = data.data_real()
freq = data.primary_sweep_values

hfss.post.create_report('dB(S(2,1))')
```

### Lab 3. PyAEDT嵌入optiSLang當中

#### python node
```python
import subprocess
import psutil
import json

from pyvariant import list_2_variant_xy_data

if 'OSL_REGULAR_EXECUTION' not in locals(): 
    OSL_REGULAR_EXECUTION = False


if not OSL_REGULAR_EXECUTION:
    w = 0.5
    dw = 0.1
    t = 0.1
    gap = 0.5
    h = 0.3
    sw = 1
    sl = 2
    n = 10

process = subprocess.Popen(
    [r'C:\myvenv\Scripts\python.exe', 
    'c:\demo\serpentine_2.py', 
    str(w), 
    str(dw),
    str(t),
    str(gap),
    str(h),
    str(sw),
    str(sl),
    str(n)],
    text=True,
    stdout=subprocess.PIPE,
    stderr=subprocess.PIPE
)

try:
    stdout, stderr = process.communicate(timeout=120)
    if process.returncode == 0:
        print("Success:", stdout)
        try:
            with open('c:/demo/serpentine.json') as f:
                x, y = json.load(f)

            variant_y = list_2_variant_xy_data(y, x)
        except Exception as e:
            print(f"Error parsing output: {e}")
    else:
        print(f"Error running script: {stderr}")
except subprocess.TimeoutExpired:
    print("Process timed out")
    process.terminate()

    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == "ansysedt.exe":
            proc.kill()
            print(f"Terminated {proc.info['name']} with PID {proc.info['pid']}")

```

#### serpentine_2.py
```python
import sys, json
w, dw, t, gap, h, sw, sl, n = map(float, sys.argv[1:])

# w = 0.5
# dw = 0.1
# t = 0.1
# gap = 0.5
# h = 0.3
# sw = 1
# sl = 2
# n = 10

def get_cell(x):
    return [(x,sl,0),(x+sw,sl,0),(x+sw,0,0),(x+2*sw,0,0)]

pts = [(0,0,0), (2*sw,0,0)]
for i in range(int(n)):
    x = pts[-1][0]
    pts += get_cell(x)

x, y, z = pts[-1]
pts.append((x+sw, y, z))


from pyaedt import Hfss

hfss = Hfss(version='2024.1')

hfss.modeler.model_units = 'mm'
line = hfss.modeler.create_polyline(pts,
                                    xsection_type='Isosceles Trapezoid',
                                    xsection_height=t,
                                    xsection_width=w,
                                    xsection_topwidth=w-dw,
                                    material='copper')

x0, y0, z0, x1, y1, z1 = line.bounding_box


box = hfss.modeler.create_box((0, y0-y1-w/2,-t/2), 
                              (x1, 3*(y1-y0), -h),
                              material = 'FR4_epoxy')

gnd = hfss.modeler.create_object_from_face(box.bottom_face_z)
hfss.modeler.thicken_sheet(gnd, 0.01)
gnd.material_name = 'copper'
region = hfss.modeler.create_region([0,0,0,0,1000,0])

port1 = hfss.wave_port(region.bottom_face_x, gnd.name)
port2 = hfss.wave_port(region.top_face_x, gnd.name)

setup = hfss.create_setup()
setup.props['Frequency'] = '2GHz'
setup.create_linear_step_sweep('GHz',0.001,2,0.1)

hfss.analyze(cores=4)
data = hfss.post.get_solution_data('dB(S(2,1))')
y = data.data_real()
x = data.primary_sweep_values

hfss.post.create_report('dB(S(2,1))')

with open('c:/demo/serpentine.json', 'w') as f:
    json.dump((x, y), f)
    
hfss.close_project()

```

> 完成專案下載
![optislang](/assets/serpentine_1D.zip)

### Lab 4. PyOptiSLang建立MOP模型

```python
text = '''
if not 'OSL_REGULAR_EXECUTION' in locals(): 
    OSL_REGULAR_EXECUTION = False


if not OSL_REGULAR_EXECUTION:
    x1 = 0.1
    x2 = 0.1

y = (x1 -1)**2 + (x2 -3)**2

'''

with open('c:/demo/test.py', 'w') as f:
    f.write(text)

from ansys.optislang.core import Optislang
from ansys.optislang.core import node_types
from ansys.optislang.core.project_parametric import ObjectiveCriterion
from ansys.optislang.core.tcp.osl_server import TcpOslServer
osl_server = TcpOslServer()
osl_server.new()
para = osl_server.create_node(node_types.AMOP.id)
python = osl_server.create_node(node_types.Python2.id, parent_uid=para)

osl_server.set_actor_property(python, 'AllowSpaceInFilePath', True)
prop = osl_server.get_actor_properties(python)
prop['Path']['path']['split_path']['head'] = 'c:/demo'
prop['Path']['path']['split_path']['tail'] = 'test.py'

osl_server.set_actor_property(python, 'Path', prop['Path'])
x = osl_server.get_actor_properties(python)

osl_server.connect_nodes(para, "IODesign", python, "IDesign")
osl_server.connect_nodes(python, "ODesign", para, "IIDesign")

osl_server.register_location_as_parameter(python, 'x1', 'x1', 0.1)
osl_server.register_location_as_parameter(python, 'x2', 'x2', 0.1)

osl_server.register_location_as_response(python, 'y', 'y', 0.1)
info = osl_server.get_actor_properties(para)

container = info['ParameterManager']['parameter_container']
container[0]['deterministic_property']['lower_bound'] = -5
container[0]['deterministic_property']['upper_bound'] = 5

container = info['ParameterManager']['parameter_container']
container[1]['deterministic_property']['lower_bound'] = -5
container[1]['deterministic_property']['upper_bound'] = 5

osl_server.set_actor_property(para, 'ParameterManager', info['ParameterManager'])

osl_server.save_as('c:/demo/example.opf')

osl_server.add_criterion(para, 'min', 'y', 'obj_0')


osl_server.dispose()

#%%

with Optislang(project_path='c:/demo/example.opf') as osl:
    osl.application.project.start()

```

### Lab 5. PyOptisLang生成一鍵最佳化專案
> OCO.opf框架下載
[oco.opf](/assets/oco.opf)

```python
template_opf_path = 'c:/demo/oco.opf'
opf_path = 'c:/demo/oco_finished.opf'

text = '''
if not 'OSL_REGULAR_EXECUTION' in locals(): 
    OSL_REGULAR_EXECUTION = False

if not OSL_REGULAR_EXECUTION:
    x1 = 0.1
    x2 = 0.1

y = (x1 -1)**2 + (x2 -3)**2

'''

with open('c:/demo/test.py', 'w') as f:
    f.write(text)

from ansys.optislang.core import Optislang
from ansys.optislang.core.tcp.osl_server import TcpOslServer
osl_server = TcpOslServer()
osl_server.open(template_opf_path)

tree_props = osl_server.get_full_project_tree_with_properties()

oco = tree_props['projects'][0]['system']['nodes'][0]['uid']
python = tree_props['projects'][0]['system']['nodes'][0]['nodes'][0]['uid']

osl_server.set_actor_property(python, 'AllowSpaceInFilePath', True)
prop = osl_server.get_actor_properties(python)
prop['Path']['path']['split_path']['head'] = 'd:/demo'
prop['Path']['path']['split_path']['tail'] = 'test.py'

osl_server.set_actor_property(python, 'Path', prop['Path'])
x = osl_server.get_actor_properties(python)


osl_server.register_location_as_parameter(python, 'x1', 'x1', 0.1)
osl_server.register_location_as_parameter(python, 'x2', 'x2', 0.1)

osl_server.register_location_as_response(python, 'y', 'y', 0.1)
info = osl_server.get_actor_properties(oco)

container = info['ParameterManager']['parameter_container']
container[0]['deterministic_property']['lower_bound'] = -5
container[0]['deterministic_property']['upper_bound'] = 5

container = info['ParameterManager']['parameter_container']
container[1]['deterministic_property']['lower_bound'] = -5
container[1]['deterministic_property']['upper_bound'] = 5

osl_server.add_criterion(oco, 'min', 'y', 'obj_0')

osl_server.set_actor_property(oco, 'ParameterManager', info['ParameterManager'])

osl_server.save_as(opf_path)
osl_server.dispose()

#%%
with Optislang(project_path=opf_path) as osl:
    osl.application.project.start()


```




