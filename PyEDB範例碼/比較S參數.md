使用scikit-rf繪製多組S參數檔案的比較圖
---

這段程式碼會將指定的兩個 S-Parameter 檔案 (以 `.s2p` 格式儲存) 匯入並比較它們的 S21 (即從第 1 埠到第 2 埠的傳輸參數) 的特性。以下是程式碼的主要步驟和功能：
### 程式碼說明 
 
1. **匯入必要的模組** : 
  - `skrf` 用於處理 S-Parameter 檔案。
 
  - `matplotlib.pyplot` 用於繪製圖表。
 
  - `numpy` 用於數值計算。
 
2. **指定 S-Parameter 檔案路徑** : 
  - 使用 `file_paths` 列表定義 S-Parameter 檔案的位置。
 
3. **匯入 S-Parameter 檔案** : 
  - 使用 `rf.Network` 讀取檔案，並將每個 `Network` 實例存儲在 `networks` 列表中。
 
4. **繪製 S21 比較圖** : 
  - 使用 `network.f` 取得頻率資訊，並以 GHz 為單位。
 
  - 使用 `network.s[:, 1, 0]` 提取 S21 的值，並轉換為 dB。

  - 每條曲線用檔案名稱作為標籤。
 
5. **圖表格式化** :
  - 設定標題、座標軸標籤、圖例與格線。

### 執行注意事項 
 
1. **檔案路徑** :
確保 `file_paths` 中的檔案路徑正確，且檔案存在。
 
2. **S-Parameter 檔案格式** :
檔案應為 `.s2p` 格式，且包含有效的 S-Parameter 資料。
 
3. **Python 環境** :
確保安裝了 `scikit-rf` (`skrf`)、`matplotlib` 和 `numpy` 模組，使用以下命令安裝：

```bash
pip install scikit-rf matplotlib numpy
```
 
4. **輸出圖表** :
  - 圖表顯示兩條曲線，分別代表兩個 S-Parameter 檔案的 S21 參數隨頻率變化的情況。

### 執行結果 

執行此程式碼後，將會產生一個比較圖，顯示兩個檔案的 S21 特性。這有助於分析不同設計或情境下的信號傳輸性能。

```python
import skrf as rf
import matplotlib.pyplot as plt
import numpy as np

# S-parameter 檔案路徑
file_paths = [
    r"D:\OneDrive - ANSYS, Inc\Models\S_Parameter\3_RXIN2_3_RXIN0.s2p",
    r"D:\OneDrive - ANSYS, Inc\Models\S_Parameter\3_RXIN2_3_RXIN1.s2p",
]

# 匯入並處理每個檔案
networks = [rf.Network(file) for file in file_paths]

# 繪製 S21 的比較圖
plt.figure(figsize=(10, 6))
for network, file_path in zip(networks, file_paths):
    label = file_path.split("\\")[-1]  # 使用檔案名作為標籤
    plt.plot(network.f / 1e9, 20 * np.log10(abs(network.s[:, 1, 0])), label=label)  # S21 in dB

# 圖表設定
plt.title("Comparison of S21 Across Different S-Parameter Files")
plt.xlabel("Frequency (GHz)")
plt.ylabel("S21 (dB)")
plt.legend()
plt.grid(True)
plt.show()
```
### 執行結果

![2025-01-15_04-41-33](/assets/2025-01-15_04-41-33.png)