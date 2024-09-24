自動網表暫態模擬並輸出CSV檔案
---

假設在 d:/demo 目錄下有多個用於SI Transient模擬的網表（.sp 檔案），我們需要對每個網表進行模擬，並將所有節點的波形數據輸出為 CSV 檔案。通常的處理方式是將這些網表導入至 AEDT Circuit Netlist，進行模擬。模擬完成後，將所有節點的電壓數據加入報告中，最後將這些數據輸出到 CSV 檔案。當需要處理大量檔案時，這個過程會變得相當繁瑣。透過執行腳本，我們可以自動化這一流程，依次處理所有檔案，大大提升效率。
>:link: **範例下載**
[run_netlist.zip](/assets/run_netlist.zip)<br> 將檔案複製到d:/demo目錄，在AEDT當中執行`run.py`，程式會依序導入a1.cir, a2.cir模擬，並輸出a1.csv，a2.csv到d:/demo目錄當中。

![2024-05-03_19-39-21](/assets/2024-05-03_19-39-21.png)

```python
import os

abspath = os.path.abspath(__file__)
directory = os.path.dirname(abspath)
os.chdir(directory)

oDesktop.ClearMessages("", "", 2)

for cir in os.listdir(directory):
    if not cir.endswith('.sp'):
        continue
    
    cir_path = os.path.join(directory, cir)
    csv_path = cir_path.replace('.sp', '.csv')
    
    oDesktop.OpenProject(cir_path)
    oProject = oDesktop.GetActiveProject()
    oDesign = oProject.GetActiveDesign()
    
    oDesign.AnalyzeAll()
    oModule = oDesign.GetModule("ReportSetup")
    oModule.GetAllCategories("Standard", "Data Table", "TRAN", "",)
    quantities = oModule.GetAllQuantities("Standard", "Data Table", "TRAN", "", 'Voltage')
    
    oModule.CreateReport("Transient Voltage Table", "Standard", "Data Table", "TRAN", 
     	[
    		"NAME:Context",
    		"SimValueContext:="	, [1,0,2,0,False,False,-1,1,0,1,1,"",0,0,"DE",False,"0"]
     	], 
     	[
    		"Time:="		, ["All"]
     	], 
     	[
    		"X Component:="		, "Time",
    		"Y Component:="		, quantities
     	])
    
    oModule.ExportToFile("Transient Voltage Table", csv_path, False)
    AddWarningMessage('save {}!'.format(csv_path))
    oProject.Close()

```