將 AEDT 定義的全域變數傳遞並使用在自訂模組中
---

### 目的

在 AEDT 環境下，許多內建變數（如 `oDesktop`、`AddWarningMessage`）是直接以全域變數的形式提供。當我們將功能拆分到模組中時，這些變數不會自動被傳入。這段程式碼的目的是：讓自訂模組也能存取這些 AEDT 提供的變數，而不需要手動傳參數。

### 功能

* 透過 `sys.modules['__main__']` 動態存取主程式的命名空間。
* 在模組中取得 AEDT 的全域控制物件並執行功能。
* 避免在多個模組間重複傳遞 AEDT 的物件。

### 流程架構

1. `main.py` 是主程式，由 AEDT 執行，已內建全域變數如 `oDesktop`。
2. `main.py` 匯入自訂模組 `myutils`。
3. `myutils.py` 中透過 `sys.modules['__main__']` 取得主程式中的全域變數。
4. 在模組中的函式使用這些變數執行對 AEDT 的操作，例如顯示系統函式庫路徑。

### 補充說明

* `sys.modules['__main__']` 可以讓模組存取主程式的全域變數，這對於 AEDT 這種由 GUI 呼叫腳本並注入變數的環境特別有用。
* `getattr()` 是用來動態取得物件屬性的函式，可以避免因屬性不存在而發生錯誤。
* 這種方式讓程式更模組化，不需要在每次呼叫時都手動傳入 `oDesktop` 等物件。

### 範例程式

#### main.py

```python
import os
import sys

# 設定模組路徑，確保可以載入同資料夾中的模組
self_dir = os.path.dirname(os.path.abspath(__file__))
if self_dir not in sys.path:
    sys.path.append(self_dir)

# 匯入模組並執行函式
import myutils
myutils.func()
```

#### myutils.py

```python
import sys

# 從主程式（__main__）中取得 AEDT 提供的變數
main = sys.modules['__main__']
oDesktop = getattr(main, "oDesktop", None)
AddWarningMessage = getattr(main, "AddWarningMessage", None)

def func():
    # 使用 AEDT 的 API 顯示系統函式庫目錄
    AddWarningMessage(oDesktop.GetSysLibDirectory())
```
