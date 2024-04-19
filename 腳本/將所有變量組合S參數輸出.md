將所有變量組合S參數輸出
---

在HFSS/3D Layout 當中進行S參數模擬並使用參數掃描（Sweep）功能時，應確保先啟用“導出S參數”選項。這樣做可確保在每次模擬完成後，自動生成相應的S參數檔案，從而便於後續的數據處理和分析。

![2024-04-19_13-03-36](/assets/2024-04-19_13-03-36_bz0hzjytz.png)

如果在開始模擬前忘記勾選此選項，您可以在整個模擬完成之後使用以下Python腳本導出所有參數的S參數檔案。請將下方代碼複製並保存為 Sweep_S_Export.py 文件，然後執行該文件即可。

### HFSS版本
```python
import os

oDesktop.ClearMessages("", "", 2)
oProject = oDesktop.GetActiveProject()
directory = oProject.GetPath()

oDesign = oProject.GetActiveDesign()
oModule = oDesign.GetModule("BoundarySetup")
num = oModule.GetNumExcitations()

oModule_rs = oDesign.GetModule("ReportSetup")
oModule_sol = oDesign.GetModule("Solutions")
for solution in oModule_rs.GetAvailableSolutions('Standard'):
    solution_name = solution.replace(':','_').replace(' ','')
    
    for i in oModule_sol.GetAvailableVariations(solution):
        snp_path = os.path.join(directory,'{}-{}.s{}p'.format(solution_name, i, num))
        #oDesign.ExportNetworkData(i, [solution], 3, snp_path, ["All"], True, 50, "S", -1, 0, 15, True, True, False)
        
        try:
            oModule_sol.ExportNetworkData(i, [solution], 3, snp_path, ["All"], True, 50, "S", -1, 0, 15, True, True, False)
            AddWarningMessage(snp_path)
        except:
            pass

```


### HFSS 3D Layout版本
```python

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


