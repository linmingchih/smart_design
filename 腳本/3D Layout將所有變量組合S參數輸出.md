3D Layout將所有變量組合S參數輸出
---

在進行3D Layout模擬並使用參數掃描（Sweep）功能時，應確保先啟用“導出S參數”選項。這樣做可確保在每次模擬完成後，自動生成相應的S參數檔案，從而便於後續的數據處理和分析。

![2024-04-19_13-03-36](/assets/2024-04-19_13-03-36_bz0hzjytz.png)

如果在開始模擬前忘記勾選此選項，您可以使用以下Python腳本手動導出所有參數的S參數檔案。請將下方代碼複製並保存為 3D_Layout_Sweep_S_Export.py 文件，然後執行此腳本即可導出所需的檔案。這樣即使在模擬後才意識到忘記勾選相應選項，也能確保數據不會遺失。

```python
# from win32com import client
# oApp = client.Dispatch("Ansoft.ElectronicsDesktop.2024.1")
# oDesktop = oApp.GetAppDesktop()
# oDesktop.RestoreWindow()

import os

oDesktop.ClearMessages("", "", 2)
oProject = oDesktop.GetActiveProject()
directory = oProject.GetPath()

oDesign = oProject.GetActiveDesign()
oModule = oDesign.GetModule("Excitations")
num = len(oModule.GetAllPortsList())

oModule = oDesign.GetModule("SolveSetups")
for solution in oModule.GetAllSolutionNames():
    solution_name = solution.replace(':','_').replace(' ','')
    
    for i in oModule.ListVariations(solution):
        snp_path = os.path.join(directory,'{}-{}.s{}p'.format(solution_name, i, num))
        oDesign.ExportNetworkData(i, [solution], 3, snp_path, ["All"], True, 50, "S", -1, 0, 15, True, True, False)
        AddWarningMessage(snp_path)
```

![2024-04-19_12-55-07](/assets/2024-04-19_12-55-07.png)