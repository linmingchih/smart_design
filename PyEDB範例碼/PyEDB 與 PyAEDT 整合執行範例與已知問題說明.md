PyEDB 與 PyAEDT 整合執行範例與已知問題說明
---

在使用 Ansys 的 Python 自動化工具時，許多開發工程師會希望能夠在同一支程式中，同時操作 **PyEDB**（用於 PCB 幾何與結構編輯）以及 **PyAEDT**（用於模擬設定與求解）。來完成此任務，以下程式碼是一個簡單，示範如何將這兩者整合成單一流程，並說明目前存在的限制與對應解法。



### 🔧 範例：整合執行 PyEDB 與 PyAEDT

這是理想中的整合範例程式碼，展示如何使用 PyEDB 建立 EDB 專案，然後使用 PyAEDT 開啟該專案進行模擬設定。

```python
# 建立並編輯 EDB 專案
from pyedb import Edb

edb = Edb(version='2024.1')
edb.stackup.add_layer_top('Top')
edb.modeler.create_trace([(0,0), (10,0)], 'Top')

edb.save_edb_as('d:/demo8/test.aedb')
edb.close_edb()

# 嘗試使用 HFSS 3D Layout 開啟同一個專案
from pyaedt import Hfss3dLayout

hfss = Hfss3dLayout('d:/demo8/test.aedb', version='2025.1', remove_lock=True)
```

 然而，執行上述程式碼時，通常會遇到錯誤，無法成功開啟 EDB 專案進行模擬設定。以下說明問題原因及解決方案。

### ⚠️ 問題說明

執行上述程式時，會出現類似以下錯誤訊息：

```
PyAEDT ERROR: **************************************************************
ERROR:Global:**************************************************************
PyAEDT ERROR:   File "...\runpy.py", line 196, in _run_module_as_main
```

造成錯誤的主因在於 **`edb.close_edb()` 並未完全釋放系統資源**，導致後續的 **PyAEDT (HFSS3dLayout)** 無法順利開啟同一個 `.aedb` 專案。此問題已被 RD 團隊確認並正在修正中。



### ✅ 臨時解決方案：分開執行兩段程式

為避免資源衝突，建議將 PyEDB 與 PyAEDT 的操作分成兩個獨立腳本，並由主程式以 **`subprocess`** 呼叫執行。

#### 1️⃣ edb_example.py

```python
from pyedb import Edb

edb = Edb(version='2024.1')

edb.stackup.add_layer_top('Top')
edb.modeler.create_trace([(0,0), (10,0)], 'Top')

edb.save_edb_as('d:/demo8/test.aedb')
edb.close_edb()
```

#### 2️⃣ aedt_example.py

```python
from pyaedt import Hfss3dLayout

hfss = Hfss3dLayout('d:/demo8/test.aedb', version='2025.1', remove_lock=True)

```



#### 3️⃣ main.py — 使用 subprocess 呼叫兩個腳本

```python
import subprocess
import sys

python_exe = sys.executable
aedb_path = 'd:/demo8/test.aedb'
subprocess.Popen([python_exe, 'edb_example.py']).wait()
subprocess.Popen([python_exe, 'aedt_example.py']).wait()
```
注意：請確保 `main.py`, `edb_example.py` 與 `aedt_example.py` 位於相同目錄下，並且路徑 `d:/demo8/test.aedb` 可被正確存取。且使用 `sys.executable` 來確保呼叫的 Python 解譯器與當前環境一致。

![](/assets/2025-11-02_08-56-08.png)

### 可選：傳遞參數給子腳本

如果需要傳遞參數給子腳本，可以使用 `subprocess.Popen` 的 `args` 參數來實現。舉例:
```python
subprocess.Popen([python_exe, 'aedt_example.py', aedb_path]).wait()
``` 

aedt_example.py 中可以使用 `sys.argv` 來接收參數:
```python
import sys

aedb_path = sys.argv[1]
hfss = Hfss3dLayout(aedb_path, version='2025.1', remove_lock=True)
``` 

### 📘 結論

目前建議：

1. **避免在同一 Python Session 中同時呼叫 PyEDB 與 PyAEDT。**
2. 透過 **兩個獨立腳本** 並以 **subprocess** 方式串接，可確保資源正確釋放。
3. 若後續版本修正此問題，可再考慮整合至單一流程。

此方法可穩定執行 PyEDB 與 PyAEDT 操作，確保模型正確建立與模擬順利進行。
