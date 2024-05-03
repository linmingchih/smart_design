自動網表暫態模擬並輸出CSV檔案
---

假設在 d:/demo 目錄下有多個用於SI Transient模擬的網表（.cir 檔案），我們需要對每個網表進行模擬，並將所有節點的波形數據輸出為 CSV 檔案。通常的處理方式是將這些網表導入至 AEDT Circuit Netlist，進行模擬。模擬完成後，將所有節點的電壓數據加入報告中，最後將這些數據輸出到 CSV 檔案。當需要處理大量檔案時，這個過程會變得相當繁瑣。透過執行腳本，我們可以自動化這一流程，依次處理所有檔案，大大提升效率。
>:link: **範例下載**
[run_netlist.zip](/assets/run_netlist.zip)<br> 將檔案複製到d:/demo目錄，在AEDT當中執行`run.py`，程式會依序導入a1.cir, a2.cir模擬，並輸出a1.csv，a2.csv到d:/demo目錄當中。

![2024-05-03_19-39-21](/assets/2024-05-03_19-39-21.png)

```python
import os

# 指定要操作的目錄路徑
directory = 'd:/demo'

# 清除ANSYS桌面的消息
oDesktop.ClearMessages("", "", 2)
# 改變當前工作目錄至指定的目錄
os.chdir(directory)
# 遍歷目錄中的文件
for cir in os.listdir(directory):
    # 判斷文件是否為.cir檔案
    if not cir.endswith('.cir'):
        continue
    
    # 構造完整的.cir和.csv文件路徑
    cir_path = os.path.join(directory, cir)
    csv_path = cir_path.replace('.cir', '.csv')
    
    # 打開.cir檔案專案
    oDesktop.OpenProject(cir_path)
    # 獲取當前活動的專案
    oProject = oDesktop.GetActiveProject()
    # 獲取當前活動的設計
    oDesign = oProject.GetActiveDesign()
    
    # 執行全部分析
    oDesign.AnalyzeAll()
    # 獲取報告設置模塊
    oModule = oDesign.GetModule("ReportSetup")
    # 獲取分類
    oModule.GetAllCategories("Standard", "Data Table", "TRAN", "",)
    # 獲取量度
    quantities = oModule.GetAllQuantities("Standard", "Data Table", "TRAN", "", 'Voltage')
    
    # 創建報告
    oModule.CreateReport("Transient Voltage Table", "Standard", "Data Table", "TRAN", 
        [
            "NAME:Context",
            "SimValueContext:=", [1,0,2,0,False,False,-1,1,0,1,1,"",0,0,"DE",False,"0"]
        ], 
        [
            "Time:=", ["All"]
        ], 
        [
            "X Component:=", "Time",
            "Y Component:=", quantities
        ])
    
    # 導出報告到文件
    oModule.ExportToFile("Transient Voltage Table", csv_path, False)
    # 添加警告消息提示保存成功
    AddWarningMessage('save {}!'.format(csv_path))
    # 關閉專案
    oProject.Close()
```