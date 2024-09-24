抓取Report資料曲線
---
下圖報告中包含五條資料曲線。如果我們想要在 Python 中讀取這五組曲線資料，過去常用的方法有兩種：

1. 輸出為 CSV 檔案，然後通過編寫程式碼來解析 CSV 檔案。
2. 使用 GetSolutionDataPerVariation() 函數。

以上兩種方法程式的複雜度較高，需要較多行程式碼才能將資料成功讀取到變數中。

![2024-05-01_17-29-30](/assets/2024-05-01_17-29-30.png)

現在，我們有了一個更為簡便的方法：直接利用 GetReportData() 函數即可一次性抓取報告中所有的曲線資料到一個字典結構的變數中，這樣就可以依序處理每一條曲線，大幅簡化程式的編寫過程。

```python
import matplotlib.pyplot as plt
import json
import sys
sys.path.append(r"C:\Program Files\AnsysEM\v241\Win64\PythonFiles\DesktopPlugin") #這裡需填寫正確完整路徑
import ScriptEnv
ScriptEnv.Initialize("", False, "", 50051)

oProject = oDesktop.GetActiveProject()
oDesign = oProject.GetActiveDesign()

# 獲取報告模組，通常用於設定和獲取報告數據
oModule = oDesign.GetModule('ReportSetup')

# 從模組中獲取名為 'DC Current Plot 1' 的報告數據，1 表示報告的類型
data = oModule.GetReportData('DC Current Plot 1', 1)
info = json.loads(data)  # 解析 JSON 格式的數據

# 遍歷解析後的數據中的 'traces' 部分
for trace in info['traces']:
    comps = trace['curves'][0]['comps']  # 獲取第一條曲線中的組件數據
    x, y = comps  # 組件列表中的第一個是 X 軸數據，第二個是 Y 軸數據
    plt.plot(x['vals'], y['vals'], label=y['name'])  # 繪製 X, Y 數據並設定圖例標籤為 Y 軸數據的名稱

plt.title(info['name'])  # 設定圖表標題為報告的名稱
plt.legend()  # 顯示圖例
plt.grid()  # 顯示網格
```

下圖為輸出結果

![2024-05-01_17-37-08](/assets/2024-05-01_17-37-08.png)

> :memo: **注意**
這個函數目前還不完整，有些資訊像是單位就顯示空字串。Scripting Help當中也還找不到這個函數的相關資訊。