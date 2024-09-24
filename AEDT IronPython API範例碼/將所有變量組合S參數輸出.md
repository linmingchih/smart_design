將所有變量組合S參數輸出
---

在HFSS/3D Layout 當中進行S參數模擬並使用參數掃描（Sweep）功能時，應確保先啟用“導出S參數”選項。這樣做可確保在每組變量模擬完成後，軟體自動輸出相應的S參數檔案，從而便於後續的數據處理和分析。勾選選項「Save as default」，系統會將當前的設置儲存為默認選擇。下次您在做Sweep模擬時，系統便會自動輸出S參數。

![2024-04-19_13-03-36](/assets/2024-04-19_13-03-36_bz0hzjytz.png)

如果在開始模擬前忘記勾選此選項，您可以在整個模擬完成之後使用以下Python腳本導出所有參數的S參數檔案。請將下方代碼複製並保存為 Sweep_S_Export.py 文件，然後執行該文件即可。

![2024-04-19_12-55-07](/assets/2024-04-19_12-55-07.png)

### HFSS 版本

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
        
        try:
            oModule_sol.ExportNetworkData(i, [solution], 3, snp_path, ["All"], True, 50, "S", -1, 0, 15, True, True, False)
            AddWarningMessage(snp_path)
        except:
            pass

```


### HFSS 3D Layout 版本

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

### HFSS 版本2

變數數量過多，會使得變數組合形成的檔名過長進而導致輸出失敗，以下版本用編號作為檔名，另外生成.csv檔案紀錄變數組合與檔名對應關係方便查找。

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
design_name = oDesign.GetName()

oModule = oDesign.GetModule("BoundarySetup")
num = oModule.GetNumExcitations()

oModule_rs = oDesign.GetModule("ReportSetup")
oModule_sol = oDesign.GetModule("Solutions")

with open(os.path.join(directory, '{}_statistics.csv'.format(design_name)), 'w') as f:
    for solution in oModule_rs.GetAvailableSolutions('Standard'):
        solution_name = solution.replace(':','_').replace(' ','')

        for n, variable in enumerate(oModule_sol.GetAvailableVariations(solution)):
            snp_path = os.path.join(directory,'{}_{}_{:03}.s{}p'.format(design_name, solution_name, n, num))
            
            try:
                oModule_sol.ExportNetworkData(variable, [solution], 3, snp_path, ["All"], True, 50, "S", -1, 0, 15, True, True, False)
                f.writelines('{:4}, {}\n'.format(variable, snp_path))
                AddWarningMessage(snp_path)
            except:
                pass
```


