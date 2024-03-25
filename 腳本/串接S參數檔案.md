串接S參數檔案
---
### 需求
串接多個S參數

![2024-03-25_13-34-36](/assets/2024-03-25_13-34-36.png)

### 使用方式 
在AEDT當中執行`cascade_Touchstone.py`腳本，如下圖視窗開啟。
1. 選擇S參數檔案
2. 並指定檔案數量
3. 按下Create輸出SPICE檔檔案

在AEDT Circuit環境匯入SPICE即可。

![2024-03-25_13-38-50](/assets/2024-03-25_13-38-50.png)

### S參數檔案要求
1. S參數檔案的ports數量必須為偶數。
2. S參數前半部的ports為輸入，後半部的ports為輸出。

> :link: **下載**
>[cascade_Touchstone.py](/assets/cascade_Touchstone.py)