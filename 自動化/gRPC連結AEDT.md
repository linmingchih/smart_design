如何在Linux環境中開發AEDT的Classical API Python腳本
---
**Linux/Windows適用**

由於Linux不支持win32com模組，您可以使用gRPC（Google Remote Procedure Call）技術。從AEDT 2023R1版本開始代替。AEDT2023R1之後支援了gRPC模式，這為Linux用戶提供了一種新的IDE連接AEDT進行程式開發的方式。

> :link:**參考連結**<br>[Troubleshooting — PyAEDT (pyansys.com)](https://aedt.docs.pyansys.com/version/stable/Getting_started/Troubleshooting.html#run-pyaedt)

### 如何使用gRPC在Linux上連接AEDT： 
1. **確認版本支援** ：首先，您需要確保您使用的AEDT版本是2023R1或更高版本，因為這些版本支持gRPC。 
2. **啟動AEDT的gRPC服務** ：在Windows機器上，您可以通過命令行啟動AEDT的gRPC服務。打開命令提示符或PowerShell，輸入以下命令來啟動AEDT並開啟gRPC服務：

```bash
ansysedt.exe -grpcsrv 50051
```



其中`50051`是gRPC服務的端口號，您可以根據需要更改此端口號。從AEDT 2023R2版本開始，PyAEDT默認在開啟AEDT時會自動創建gRPC session。不須再人工輸入命令。

![2024-04-24_15-23-03](/assets/2024-04-24_15-23-03.png)


3. **在Linux上IDE啟用PyAEDT連接** ：在您的Linux系統上，在IDE當中開啟python空白腳本並輸入以下程式碼，按下執行鍵。如果成功執行，AEDT當中會建立一個新專案。

```python
import sys
sys.path.append(r"C:\Program Files\AnsysEM\v241\Win64\PythonFiles\DesktopPlugin")
import ScriptEnv
ScriptEnv.Initialize("", False, "", 50051)
oDesktop.NewProject()
```
4. **編寫和測試Python腳本** ：之後便可以在Linux系統上IDE當中輕鬆編寫Python腳本，並透過gRPC與AEDT交互，進行設計建模、分析設定和資料擷取等操作。
