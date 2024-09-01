預防AEDT出現無預期崩潰
---
在使用 PyOptiSLang 連接 PyAEDT 進行建模時，若遇到設定的參數值組合導致生成不合理的結構，會導致模擬無法進行，無法回傳模擬值。或是當 AEDT 崩潰，如下圖錯誤訊息所示，可能會導致 OptiSLang 停止，無法繼續進行其他樣本點的模擬，從而無法蒐集足夠的數據來建立數學模型。

![2024-09-01_04-23-07](/assets/2024-09-01_04-23-07.png)

為了解決這個問題，您可以考慮以下幾種方法：
 
1. **錯誤處理機制** ：在 PyOptislang當中的Python碼中增加錯誤處理邏輯，例如在每個模擬步驟後檢查 AEDT 是否成功完成計算。如果發現錯誤，可以跳過該樣本點並繼續進行下一個樣本的模擬。
 
2. **設定合理的參數範圍** ：確保在設計實驗時，參數的範圍限制在合理的範疇內，以避免生成不可行的結構。
 
3. **自動重啟或恢復機制** ：當 AEDT 崩潰時，自動嘗試重啟 AEDT 並恢復模擬。如果該點仍然無法計算，則標記該樣本點為無效點。

### 保護程式碼

這段程式碼中的保護機制主要包含以下三個部分：`subprocess.run`、`try-except` 錯誤處理機制以及 `timeout` 與 `proc-kill` 機制。 
1. **`subprocess.run`** ：
這個方法用來啟動一個外部程序並且在Python中進行互動。在這裡，它被用來執行一個獨立的Python腳本，該腳本以PyAEDT進行模擬運算。這種做法使得模擬運算可以在主程式之外進行，並允許主程式捕捉和處理腳本的標準輸出（stdout）和錯誤信息（stderr）。這樣可以防止主程式因腳本錯誤而崩潰。
 
2. **`try-except`** ：
這個部分用來捕捉和處理在執行外部腳本過程中可能發生的錯誤。主要是通過 `communicate` 方法來等待外部腳本的執行結果，並在遇到問題（如超時、腳本執行失敗）時，通過 `except` 來捕捉錯誤並執行相應的處理。這樣做可以保證即使腳本執行失敗，主程式也能穩定運行，不會因為未處理的錯誤而中斷。
 
3. **`timeout` 與 `proc-kill`** ：
如果外部腳本在指定時間（如120秒）內未完成，則會觸發 `TimeoutExpired` 例外，程式會終止這個過程（process），以避免長時間掛起或無限等待。隨後，程式會使用 `psutil` 模組檢查是否有遺留的 `ansysedt.exe` 進程，並將其強制終止，這樣可以確保系統資源不被占用並且清理可能導致的AEDT崩潰的殘餘進程，確保後續模擬的正常進行。

![2024-09-01_04-40-57](/assets/2024-09-01_04-40-57_7lt28j09s.png)

#### optiSLang當中的python
```python
import subprocess
import psutil
import json

from pyvariant import list_2_variant_xy_data

if 'OSL_REGULAR_EXECUTION' not in locals(): 
    OSL_REGULAR_EXECUTION = False

if not OSL_REGULAR_EXECUTION:
    length = 8.0
    width = 2.0
    thickness = 0.2
    gap = 1.0

try:
    result = subprocess.run(
        [r'C:\Users\mlin\.ansys_python_venvs\2024_8_14\Scripts\python.exe', 
        'd:/demo7/test.py', 
        str(length), 
        str(width),
        str(thickness),
        str(gap)],
        text=True,
        capture_output=True,
        timeout=120
    )
    
    if result.returncode == 0:
        print("Success:", result.stdout)
        try:
            with open('d:/demo7/data.json') as f:
                x, y = json.load(f)
            variant_y = list_2_variant_xy_data(y, x)
        except Exception as e:
            print(f"Error parsing output: {e}")
    else:
        print(f"Error running script: {result.stderr}")

except subprocess.TimeoutExpired:
    print("Process timed out")
    
    for proc in psutil.process_iter(['pid', 'name']):
        if proc.info['name'] == "ansysedt.exe":
            proc.kill()
            print(f"Terminated {proc.info['name']} with PID {proc.info['pid']}")

except Exception as e:
    print("An error occurred:", e)

```

#### pyaedt程式碼

```python
import sys
from pyaedt import Hfss
import json

hfss = Hfss(project=r"D:\demo7\pair.aedt", 
            design='HFSSDesign1',
            version='2024.1',
            remove_lock=True)
#%%
print(sys.executable)
print(sys.argv)
length, width, thickness, gap = sys.argv[1:] 

hfss.variable_manager.set_variable('length', f'{length}mm')
hfss.variable_manager.set_variable('width', f'{width}mm')
hfss.variable_manager.set_variable('thickness', f'{thickness}mm')
hfss.variable_manager.set_variable('gap', f'{gap}mm')

hfss.analyze_setup()

data = hfss.post.get_solution_data('dB(S21)')


y = data.data_real()
x = data.primary_sweep_values
print(x, y)
with open('d:/demo7/data.json', 'w') as f:
    json.dump((x, y), f)
```
#### 輸出數據集
當失敗時(紅色標籤)，會繼續其他樣本點模擬(綠色標籤)，不會卡住。
![2024-09-01_04-42-48](/assets/2024-09-01_04-42-48.png)

