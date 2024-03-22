IDE Iron Python連結AEDT/SIwave
---
使用 win32com 函式庫來連接和操作 ANSYS AEDT/SIwave 來編輯Iron Python是一種常見的方法，尤其是在自動化或批次任務時。

#### AEDT HFSS
```python
from win32com import client
oApp = client.Dispatch("Ansoft.ElectronicsDesktop.2024.1")
oDesktop = oApp.GetAppDesktop()
oDesktop.RestoreWindow()

oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.SetActiveEditor("3D Modeler")
```

#### AEDT 3D Layout
```python
from win32com import client
oApp = client.Dispatch("Ansoft.ElectronicsDesktop.2024.1")
oDesktop = oApp.GetAppDesktop()
oDesktop.RestoreWindow()

oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()
oEditor = oDesign.GetActiveEditor()
```

#### SIwave
```python
from win32com import client

oApp = client.Dispatch("SIwave.Application.2024.1")
oApp.RestoreWindow()
oDoc = oApp.GetActiveProject()
```