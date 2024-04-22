輸出AEDT所有開啟HFSS設計的S參數
---

如果您想要從AEDT中的所有開啟專案導出每個專案下的所有HFSS設計的S參數，您可以使用以下腳本進行處理。您需要將以下程式碼保存為 `exportS.py`，然後在AEDT中執行它。

![2024-04-22_14-39-05](/assets/2024-04-22_14-39-05_yi0d08m2y.png)

```python
from win32com import client

for project_name in oDesktop.GetProjectList():
    oProject = oDesktop.SetActiveProject(project_name)
    
    for oDesign in oProject.GetDesigns():
        try:
            design_name = oDesign.GetName()
            oModule = oDesign.GetModule("BoundarySetup")
            number = oModule.GetNumExcitations()
            oModule = oDesign.GetModule("Solutions")
            
            for setup in oModule.GetValidISolutionList():
                if 'Sweep' in setup:
                    oModule.ExportNetworkData("", [setup], 3, "c:/{}_{}.s{}p".format(project_name, design_name, number), ['All'], True, 50, "S", -1, 0, 15, True, True, False)
        except:
            print('"{}-{}" failed to export Touchstone!'.format(project_name, design_name))```
