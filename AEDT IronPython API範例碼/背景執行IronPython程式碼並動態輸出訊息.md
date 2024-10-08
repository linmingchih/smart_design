背景執行IronPython程式碼並動態輸出訊息
---
通常在 AEDT GUI 中執行 IronPython 腳本，但若需在無 GUI 的情況下運行，可使用 ansysedt -feature=beta -ng runscriptandexit example.py，該指令會將執行過程中的訊息輸出到 example.log。為了實現動態訊息監控，以下程式使用多執行緒方式，在背景模式下執行 AEDT IronPython 腳本的同時，監控日誌文件的變化，並將其即時輸出到控制台，從而實現兩個操作的並行處理。

首先，run_command 函數使用 subprocess.Popen 執行外部指令並等待其完成。當指令執行結束後，會設置一個事件 command_done_event，表示命令已完成執行。

follow_log 函數則持續打開並監控指定的日誌文件，通過移動文件指針到文件末尾來避免讀取舊的內容，只打印新增的日誌內容。此監控過程會一直持續，直到命令執行完成且文件內容全部讀取為止。

程式使用兩個執行緒來同時進行命令執行和日誌文件監控，並透過事件 command_done_event 來協調這兩者的結束。主程式會在兩個執行緒都結束後才退出，確保所有任務都已完成。這個設計適合在需要監控長時間運行的命令時使用，確保不會錯過任何日誌輸出。

### 主程式
```python
import subprocess
import threading
import time
import os

ironpython_path = 'd:/demo2/example.py'

def run_command(command):
    """執行外部指令的函數，並等待完成。"""
    process = subprocess.Popen(command, shell=True)
    process.wait()  # 等待指令執行完畢
    command_done_event.set()  # 設置事件，表示指令執行已完成

def follow_log(file):
    """持續監控log文件並打印新增的內容。"""
    with open(file, 'r') as f:
        f.seek(0, 2)  # 移動到文件的末尾
        while not command_done_event.is_set() or f.tell() != os.fstat(f.fileno()).st_size:
            line = f.readline()
            if not line:
                time.sleep(0.5)  # 短暫休眠，避免過度佔用CPU
                continue
            print(line, end='')

# 創建一個事件來跟踪命令是否完成
command_done_event = threading.Event()

# 執行指令的部分
command = f"ansysedt -feature=beta -ng -runscriptandexit {ironpython_path}"
command_thread = threading.Thread(target=run_command, args=(command,))
command_thread.start()

# 監控log文件的部分
log_file = ironpython_path.replace('.py', '.log')
log_thread = threading.Thread(target=follow_log, args=(log_file,))
log_thread.start()

# 等待所有線程結束
command_thread.join()
log_thread.join()
```

### Iron Python 腳本： `example.py`
```python
import time
import ScriptEnv
ScriptEnv.Initialize("Ansoft.ElectronicsDesktop")
oDesktop.RestoreWindow()
for i in range(10):
    oProject = oDesktop.NewProject()
    AddWarningMessage(oProject.GetName())
    time.sleep(1)

```
### 訊息逐段輸出
![log_follower](/assets/log_follower.gif)