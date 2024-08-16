IDE Iron Python連結AEDT/SIwave
---

在使用VS Code、PyCharm或Spyder等Python集成開發環境（IDE）編寫PyAEDT程式碼時，IDE所提供的自動完成、語法檢查和偵錯等功能極大地優化了開發體驗。然而，當在IDE內直接運行針對AEDT API所編寫的Python程式碼時，會遭遇無法與AEDT建立連接的問題，導致程式碼無法成功執行。

此類連接問題可以透過引入win32com庫來克服。這個庫提供了一種機制，允許IDE內的Python程式與ANSYS AEDT或SIwave進行互動。通過在腳本開頭部分添加必要的win32com呼叫，開發者便能在IDE環境中運行、檢查和偵錯AEDT API編寫的腳本，這對於腳本的開發和優化特別實用。

下面的程式碼示例展示了如何利用win32com庫連結到ANSYS的各種應用程式，例如HFSS和SIwave，從而實現從編寫到執行的流暢過渡。
 
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