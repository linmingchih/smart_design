取得License使用狀態
---
在大公司中，多個研究人員使用ANSYS軟體時，授權的管理是一個重要的問題。一般作法是由中央授權伺服器統一管理，這可以提高效率並確保授權的正確使用。當所有的授權都被使用時，任何新的嘗試啟動軟件的動作都會因為沒有可用的授權而失敗。

要知道誰正在使用何種授權，可以使用 `lmutil` 命令來遠端擷取授權使用的詳細訊息。`lmutil` 是一個命令行工具，可以用來查詢授權伺服器上的授權狀態。這包括哪些人正在使用哪些授權，以及他們使用授權的時間長短等信息。

例如，如果你想知道目前哪些授權正在使用中，以及是誰在使用這些授權，你可以在本地終端執行如下命令：

```bash
lmutil lmstat -a -c port@hostname
```

這裡的 `port@hostname` 應該替換為具體的授權伺服器的端口和主機名。這個命令會返回當前所有活躍的授權和它們的使用者信息，這樣管理者就可以輕鬆地查看哪些授權正在被使用，以及由哪些研究人員使用。

這樣的做法不僅可以幫助管理者更有效地監控和調配授權資源，還能在授權不足時作出及時的調整或擴充。

### 用Python簡化資訊

返回的資訊比較多且複雜，以下python程式重新整理，開發者可以根據需求自行修改。

這段程式碼的目的是從特定的ANSYS EM軟件安裝中找出授權使用的情況。首先，程式會掃描環境變數以找出ANSYS EM的安裝路徑。然後，利用這個路徑來找到 lmutil.exe 工具，這是用來查詢授權服務器狀態的命令行工具。

程式指定了一個授權服務器的地址，並使用 subprocess.run 執行 lmutil 命令以獲得授權使用的詳細信息。這些信息被輸出並進一步分析，以解析出每個軟件增量（license increment）的使用狀況，包括發行的總授權數、正在使用的授權數以及具體使用者的信息。

最後，程式進行排序並格式化輸出，列出所有軟件增量的授權使用情況，並為正在使用的增量打印出具體的使用者名稱和機器地址。這對於管理和監控軟件授權使用非常有用，特別是在需要確保授權合理分配和使用的組織環境中。

```python
import os
import subprocess

for key, item in os.environ.items():
    if key.startswith('ANSYSEM_ROOT'):
        ansysem_path = item
        
assert ansysem_path, "Can't Find ANSYSEM Installation"

lmutil = os.path.join(ansysem_path, r'licensingclient\winx64\lmutil.exe')
server = '1055@127.0.0.1'

result = subprocess.run([lmutil, "lmstat", '-a', '-c', server], capture_output=True, text=True)

print("stdout:", result.stdout)

#%%
import re
from collections import defaultdict
pattern = 'Users of (.*):.*Total of (\d+) licenses issued;  Total of (\d+) licenses in use'

data = []
info = defaultdict(list)
for line in result.stdout.splitlines():
    m = re.match(pattern, line)
    
    if m:
        flag = False
        increment, total, inuse = m.groups()
        data.append((int(inuse), int(total), increment))
        if int(inuse):
            print(line)
            flag = True
            continue
        
    if flag and 'start' in line:
        name, machine = line.strip().split()[:2]
        info[increment].append(f'\t{name}@{machine}')
    
data.sort()
for inuse, total, increment in data:
    print(increment, f'{inuse}/{total}')
    if increment in info:
        print('\n'.join(info[increment]))
```

![2024-05-18_11-38-35](/assets/2024-05-18_11-38-35.png)
