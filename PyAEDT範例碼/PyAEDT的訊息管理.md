PyAEDT的訊息管理
---

當程式發生錯誤時，合理的輸出訊息可以迅速指出問題發生的位置和原因，尤其是在複雜的系統中。例如，使用print來顯示變數的當前狀態或者執行到某個特定步驟的標記，可以幫助開發者理解錯誤發生的上下文。此外，進階的日誌管理工具如Python中的logging模組，允許開發者設定日誌的嚴重性等級（如INFO、WARNING、ERROR等），以及決定輸出到控制台或文件，這樣便於後期分析和長期存儲。

當執行 pyaedt 時，所有呼叫 API 的相關訊息都會記錄到 pyaedt.aedt_logger.pyaedt_logger 中。這些訊息會同時輸出到兩個地方：一個是位於 "C:\Users\username\AppData\Local\Temp\pyaedt_username.log"（username 是電腦帳號）的日誌文件，另一個是 IDE 的控制台，方便即時查看和診斷。


![2024-08-04_09-42-12](/assets/2024-08-04_09-42-12.png)

![2024-08-04_09-35-25](/assets/2024-08-04_09-35-25_cqmr3cee3.png)

開發者也可以呼叫pyaedt.aedt_logger.pyaedt_logger物件的方法將訊息加入到log當中。

### 訊息類別
在 ANSYS AEDT 中，訊息可以分為三個主要的類別：Global、Project 和 Design。以下是對這三個類別的詳細說明：

#### Global 訊息 
**Global 訊息** 是指全局層級的訊息，這些訊息通常涉及到整個 AEDT 應用程序的操作或狀態變化。Global 訊息適用於記錄影響整個工作環境的事件，例如應用程序啟動或關閉、全局設置的變更等。

#### Project 訊息 
**Project 訊息** 是與特定專案相關的訊息。這些訊息記錄的是專案層級的事件和操作，例如專案的打開、關閉、保存、專案設定的變更等。Project 訊息能幫助使用者追蹤與特定專案相關的所有活動和變更。

#### Design 訊息 
**Design 訊息** 是與特定設計相關的訊息。這些訊息記錄的是設計層級的事件和操作，例如設計的建立、修改、模擬運行結果等。Design 訊息能幫助使用者追蹤與特定設計相關的所有活動和變更。
這些訊息類別在 AEDT 的訊息管理器和日誌系統中非常重要，因為它們幫助使用者組織和過濾訊息，以便更有效地管理和診斷專案和設計中的問題。

![2024-08-04_08-28-22](/assets/2024-08-04_08-28-22_zb4lrvqpt.png)

在 ANSYS AEDT 的日誌系統中，錯誤訊息也可以根據嚴重程度進行分類。常見的錯誤等級包括：Info、Warning、Error 和 Fatal。以下是每個等級的詳細說明：

### 訊息等級 
 
1. **Info** ：信息訊息，用於記錄一般性的信息或操作，例如程序啟動、配置加載等。這些訊息不表示錯誤或警告。
 
2. **Warning** ：警告訊息，表示可能存在問題，但不會阻止程序繼續運行。這些訊息提醒用戶注意潛在的問題。
 
3. **Error** ：錯誤訊息，表示發生了阻止某些功能正常運行的問題。這些訊息需要用戶進行調查和修復。
 
4. **Fatal** ：致命錯誤訊息，表示發生了嚴重的問題，導致程序無法繼續運行。這些訊息通常會導致程序崩潰或終止。

### aedt_logger

`aedt_logger` 是PyAEDT當中用於管理和記錄 ANSYS AEDT（Ansys Electronics Desktop）中的訊息和日誌的工具。它允許用戶在不同層級（Global、Project、Design）和不同等級（Info、Warning、Error、Fatal）進行訊息記錄和管理。以下是 `aedt_logger` 的主要用途和功能：
### 主要用途 
 
1. **訊息記錄和分類** ：
  - 根據訊息的嚴重程度（Info、Warning、Error、Fatal）分類記錄訊息。

  - 根據訊息的範圍（Global、Project、Design）分類記錄訊息。
 
2. **日誌管理** ：
  - 將訊息寫入日誌文件，以便後續分析和查詢。

  - 將訊息輸出到標準輸出（stdout），便於即時查看。
 
3. **錯誤診斷和調試** ：
  - 記錄錯誤和警告訊息，幫助用戶診斷和修復問題。

  - 提供調試訊息，幫助開發人員追蹤程式執行過程中的細節。
 
4. **訊息檢索和過濾** ：
  - 支援從特定專案和設計中檢索訊息。

  - 支援按訊息等級過濾訊息，以便用戶快速找到需要關注的問題。

### 主要的訊息輸出方法

在 PyAEDT 中，`pyaedt.aedt_logger.pyaedt_logger` 提供了多種方法來輸出訊息，這些訊息可以記錄到日誌文件中，也可以輸出到控制台。以下是主要的訊息輸出方法及其使用示例：
 
 
1. **`add_info_message`** ：用於記錄信息訊息。
 
2. **`add_warning_message`** ：用於記錄警告訊息。
 
3. **`add_error_message`** ：用於記錄錯誤訊息。
 
4. **`add_debug_message`** ：用於記錄調試訊息。

#### Python範例
```python
import os
import pyaedt
from pyaedt import Hfss
from pyaedt.aedt_logger import AedtLogger

# 使用 logger 記錄不同類型的訊息
pyaedt.aedt_logger.pyaedt_logger.add_info_message('這是一條信息訊息')
pyaedt.aedt_logger.pyaedt_logger.add_warning_message('這是一條警告訊息')
pyaedt.aedt_logger.pyaedt_logger.add_error_message('這是一條錯誤訊息')
pyaedt.aedt_logger.pyaedt_logger.add_debug_message('這是一條調試訊息')

# 建立 HFSS 專案實例
hfss = Hfss()

# 添加設計操作並記錄訊息
hfss.modeler.create_box([0, 0, 0], [10, 10, 10], "MyBox", "copper")
pyaedt.aedt_logger.pyaedt_logger.add_info_message('已經在 HFSS 中創建一個銅盒子')

# 完成操作後記錄訊息
pyaedt.aedt_logger.pyaedt_logger.add_info_message('HFSS 操作完成')
```

![2024-08-05_04-30-52](/assets/2024-08-05_04-30-52_01215naa6.png)