Lab4 結合PyAEDT
---
### PyAEDT部分
```python
import sys
sys.path.append(r'C:\0416\Lib\site-packages')

from ansys.aedt.core import Icepak

icepak = Icepak(version='2025.2', non_graphical=True)

x1 = 10
x2 = 1
c1 = icepak.modeler.create_cylinder('XY', (0,0,0), '0.5cm', f'{x1}cm', material="Al-Extruded")
icepak.assign_source(
    assignment=c1.top_face_z.id, 
    thermal_condition='Total Power', 
    assignment_value=f'{x2}W')

icepak.assign_stationary_wall(c1.bottom_face_z.id, 
                              "Temperature",
                              temperature=0)

icepak.monitor.assign_face_monitor(c1.top_face_z.id, monitor_name='m1')
setup = icepak.create_setup()
icepak.analyze(cores=12, tasks=12)
data = icepak.post.get_solution_data('m1.Temperature')
y = float(data.data_real()[0])
icepak.release_desktop()

```

### PyOptiSLang部分
```python
script_path = 'c:/demo/icepak.py'
opf_path = 'c:/demo/lab3.opf'

from ansys.optislang.core import Optislang
import ansys.optislang.core.node_types as node_types
from ansys.optislang.core.nodes import DesignFlow
from ansys.optislang.core.project_parametric import (
    ComparisonType,
    ConstraintCriterion,
    ObjectiveCriterion,
    OptimizationParameter,
)


with Optislang(ini_timeout=60) as osl:
    root_system = osl.application.project.root_system
    amop = root_system.create_node(node_types.AMOP)
    design_export = root_system.create_node(node_types.DesignExport)
    
    amop_slot = amop.get_output_slots(name='ODesigns')[0]
    design_export_slot = design_export.get_input_slots(name='IDesigns')[0]
    amop_slot.connect_to(design_export_slot)
    
    python_node = amop.create_node(node_types.Python2, design_flow=DesignFlow.RECEIVE_SEND)
    prop = python_node.get_property('Path')
    prop['path']['split_path']['tail'] = script_path
    python_node.set_property('Path', prop)
    
    python_node.register_location_as_parameter('x1', 'x1', 10)
    python_node.register_location_as_parameter('x2', 'x2', 1)
    python_node.register_location_as_response('y', 'y', 5)
    
    parameters = amop.parameter_manager.get_parameters()
    parameters[0].range = [10.0, 20.0]
    parameters[1].range = [1.0, 5.0]
    
    amop.parameter_manager.modify_parameter(parameters[0])
    amop.parameter_manager.modify_parameter(parameters[1])
    
    criterion = ObjectiveCriterion(name="obj", expression="y", criterion=ComparisonType.MIN)
    amop.criteria_manager.add_criterion(criterion)
    
    osl.application.save_as(opf_path)
    osl.application.project.start()


```