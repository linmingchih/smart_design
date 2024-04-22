使用 Python 查詢 ANSYS 授權服務器情況
---

ANSYS License Server 是用於管理和分配 ANSYS 軟件授權的系統。它允許用戶通過網絡訪問授權，確保合法使用軟件。此服務器通過特定端口與客戶端通信，管理授權的激活和追踪。利用授權管理工具如 lmutil，管理者可以查詢服務器狀態，監控授權使用情況，從而有效配置和最佳化資源分配。

假設機器A作為License Server運行，用於管理和發放軟件授權。若要在機器B上查詢機器A的授權使用情況，首先需要確保兩台機器位於同一網域中，並在機器B上安裝lmutil工具。使用lmutil工具，機器B可以通過網絡聯絡機器A，進行授權狀態的查詢。查詢命令執行後，結果會被重定向並寫入機器B上的日誌文件中。用戶隨後可以打開這個日誌文件，讀取並分析授權的使用狀況，以便進行適當的管理和調整。

>:memo: **附註** <br> A跟B可以是同一台機器。有安裝ANSYS軟體的機器都可以找到`ANSYS Inc\Shared Files\licensing`目錄，當中便可以找到lmutil工具。

要用Python完成這項任務，您可以按照以下步驟操作：

#### 1. 將存放lmutil的目錄添加到系統的Path環境變數中
這可以通過在Python中使用 `os` 模塊來動態地添加，或者您可以在系統設置中手動設定。

#### 2. 使用 `subprocess` 模塊執行命令

這個步驟可以使用 `subprocess` 模塊來執行 `lmutil` 命令並將輸出重定向到日誌文件。

#### 3. 讀取和分析 `license_usage.log` 文件
這可以通過Python標準的文件處理功能來完成。

### 範例碼
以下是這些步驟的Python腳本示例：

```python
import os
import subprocess

# 步驟1：將ANSYS授權服務器目錄添加到Path環境變數
ansys_path = "C:\\Program Files\\ANSYS Inc\\Shared Files\\licensing\\winx64"
os.environ["PATH"] += os.pathsep + ansys_path

# 步驟2：執行lmutil命令
command = "lmutil lmstat -a -c 1055@127.0.0.1"
log_file = "license_usage.log"
with open(log_file, "w") as output_file:
    subprocess.run(command, stdout=output_file, stderr=subprocess.STDOUT, shell=True)

# 步驟3：讀取和分析license_usage.log文件
def analyze_license_usage(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.readlines()
            # 在這裡加入分析代碼
            for line in data:
                print(line.strip())  # 簡單的列印每行來展示
    except FileNotFoundError:
        print("未找到文件:", file_path)

# 執行分析函數
analyze_license_usage(log_file)
```
