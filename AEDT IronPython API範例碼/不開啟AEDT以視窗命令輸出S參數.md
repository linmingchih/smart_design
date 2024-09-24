不開啟AEDT以視窗命令輸出S參數
---
這個程式的主要目的是在不開啟 AEDT 的圖形用戶界面的情況下，透過命令列執行一個 Python 腳本來輸出 S 參數。使用 -ng 參數是為了確保 AEDT 在無圖形模式下運行，這通常用於批次處理和自動化任務，以減少資源消耗並提高效率。

#### Windows 範例指令
```batch
ansysedt -ng -BatchExtract d:\demo\extractS.py D:\demo\example.aedt
```

#### Linux 範例指令
```batch
ansysedt -ng -BatchExtract ~/demo/extractS.py ~/demo/example.aedt
```

> **:memo: 注意事項**
確保在使用此腳本之前，AEDT 檔案 `example.aedt` 已經包含了模擬結果。此外，使用 `-ng` 選項運行時，不會有任何圖形界面出現，這是自動化批處理時理想的選擇。執行之後會在.aedt目錄當中輸出S參數檔案。


#### Python 腳本功能 `extractS.py`

這個 Python 腳本的功能是從 AEDT 模型中提取 S 參數，並將其儲存為一個 `.sNp` 檔案，其中 `N` 代表端口數量。腳本的主要步驟如下： 
1. **獲取設計物件** ：首先獲取活動項目和設計名稱。 
2. **尋找激勵與分析設置** ：尋找關聯的激勵與分析設置。 
3. **組合解決方案名稱** ：格式化解決方案名稱以對應特定的設置和頻率掃描。 
4. **導出 S 參數** ：使用 `ExportNetworkData` 方法將 S 參數數據導出到指定的路徑。



```python
import os
oProject = oDesktop.GetActiveProject()
design_name = oProject.GetChildNames()[0]

oDesign = oProject.GetChildObject(design_name)

excitation = oDesign.GetChildObject('Excitations')
num = len(excitation.GetChildNames())

analysis = oDesign.GetChildObject('Analysis')
setup_name = analysis.GetChildNames()[0]
setup_obj = analysis.GetChildObject(setup_name)
sweep_name = setup_obj.GetChildNames()[0]

solution = '{}:{}'.format(setup_name, sweep_name)

snp_path = os.path.join(oProject.GetPath(), oProject.GetName() + '.s{}p'.format(num))

oDesign.ExportNetworkData("", [solution], 3, snp_path, ['all'], True, 50, "S", -1, 0, 15, True, True, True)
```