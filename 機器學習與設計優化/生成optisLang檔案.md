生成optisLang檔案
---
OPF檔案生成

```python
script_path = r"D:\OneDrive - ANSYS, Inc\Customer2024\2024_06_03_MTK_AI\script.py"

import os, re
from numpy import arange, linspace
from ansys.optislang.core import Optislang
from ansys.optislang.core import node_types
from ansys.optislang.core.project_parametric import ObjectiveCriterion
from ansys.optislang.core.tcp.osl_server import TcpOslServer

osl_server = TcpOslServer(ini_timeout=120)

osl_server.new()
para_node = osl_server.create_node(node_types.AMOP.id)
python_node = osl_server.create_node(node_types.Python2.id, parent_uid=para_node)

osl_server.set_actor_property(python_node, 'AllowSpaceInFilePath', True)
prop = osl_server.get_actor_properties(python_node)
prop['Path']['path']['split_path']['head'] = os.path.dirname(script_path)
prop['Path']['path']['split_path']['tail'] = os.path.basename(script_path)

osl_server.set_actor_property(python_node, 'Path', prop['Path'])
x = osl_server.get_actor_properties(python_node)

osl_server.connect_nodes(para_node, "IODesign", python_node, "IDesign")
osl_server.connect_nodes(python_node, "ODesign", para_node, "IIDesign")



def get_inout(script_path):
    with open(script_path) as f:
        text = f.readlines()
    
    parameters = []
    responses = []
    flag = False
    
    for line in text:
        if len(line.strip()) == 0:
            continue
        
        if 'OSL_REGULAR_EXECUTION:' in line:
            flag = True
            continue
        
        elif flag and line[0:4] == '    ':
            assignment, _range = line.strip().split('#')
            parameter, initial_value = [i.strip() for i in assignment.split('=')]
            _range = eval(_range)
            initial_value = float(initial_value)
            match _range:
                case int():
                    parameters.append((parameter, initial_value, 'Constant' , _range))
                case float():
                    parameters.append((parameter, initial_value, 'Constant' , _range))
                case (x, y):
                    parameters.append((parameter, initial_value, 'Continuous' , (x, y)))
                case list():
                    parameters.append((parameter, initial_value, 'Discrete' , _range))
        
        elif flag and line[0] != '':
            flag = False
            
            
        elif re.search('#(\s+?|)response', line):
            assignment, comment = line.strip().split('#')
            response, _ = assignment.split('=')
            responses.append(response.strip())
        
    return parameters, responses
        
        
#%%     
parameters, responses = get_inout(script_path)

for key, initial_value, *_ in parameters:
    osl_server.register_location_as_parameter(python_node, key, key, initial_value)

for response in responses:
    osl_server.register_location_as_response(python_node, response, response, 0.1)


info = osl_server.get_actor_properties(para_node)
container = info['ParameterManager']['parameter_container']
info['AMopSettings']['num_designs_max'] = 50

for (key, initial_value, _type, _range), item in zip(parameters, container):
    if _type == 'Constant':
        item['const'] = True
    
    elif _type == 'Continuous':
        lower_bound, upper_bound = _range
        item['const'] = False
        item['deterministic_property']['domain_type'] = 'real'
        item['deterministic_property']['kind'] = 'continuous'        
        item['deterministic_property']['lower_bound'] = lower_bound
        item['deterministic_property']['upper_bound'] = upper_bound
    
    elif _type == 'Discrete':
        item['const'] = False
        item['deterministic_property']['domain_type'] = 'real'
        item['deterministic_property']['kind'] = 'ordinaldiscrete_value'
        item['deterministic_property']['discrete_states'] = _range      


osl_server.set_actor_property(para_node, 'ParameterManager', info['ParameterManager'])
osl_server.set_actor_property(para_node, 'AMopSettings', info['AMopSettings'])

osl_server.save_as('d:/demo3/example.opf')

#osl_server.add_criterion(para_node, 'min', 'y', 'obj_0')

osl_server.dispose()

#%%

with Optislang(project_path='d:/demo3/example.opf') as osl:
    osl.application.project.start()


```