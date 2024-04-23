### 在匯入的Layout元件當中加上Ports


```python
oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.GetActiveEditor()

design_name = oDesign.GetName().split(';')[1]
u1 = oProject.SetActiveDesign("{}:U1".format(design_name))
u1_id = u1.GetName().split('/')[1].split(';')[0]
u1_module = u1.GetModule("Excitations")
ports = u1_module.GetAllPortsList()

port_list = ['{}:{}'.format(u1_id, i) for i in ports]

oProject.SetActiveDesign(design_name)
oEditor.CreatePortInstancePorts(["NAME:elements"] + port_list)

```

![2024-04-23_04-34-51](/assets/2024-04-23_04-34-51.png)


### 其他