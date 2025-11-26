自動調整並設定 EDB 檔案中所有有孔徑的 Padstack 參數
---

這段程式碼的主要目的是讀取一個 EDB（Ansys Electronics Database）電路板設計檔案，篩選出具有孔徑的 padstack，將其孔徑擴大 2mil，並統一設定孔鍍厚度和材料，最後儲存為新的 EDB 檔案。

### 功能

* 讀取指定版本的 EDB 檔案。
* 定義單位轉換：mil 與 meter 之間的轉換。
* 篩選出孔徑大於 0 的 padstack。
* 對這些 padstack：

  * 將孔徑加大 2mil。
  * 設定鍍層厚度為 1mil。
  * 設定材料為 copper。
* 將修改後的設計另存為新的 EDB 檔案。

### 流程架構

1. **初始化 EDB 對象**：透過 `pyedb` 套件載入指定路徑的 .aedb 檔案。
2. **定義 mil/meter 轉換函式**：方便後續處理孔徑數值。
3. **篩選並收集 padstack 資訊**：

   * 檢查每個 padstack 的 `hole_diameter` 是否大於 0。
   * 若符合條件，將其名稱、物件與轉換後的孔徑存入 `data` 字典。
4. **修改 padstack 屬性**：

   * 對每個記錄進行設定：增加孔徑、設定鍍層厚度、材料。
5. **儲存檔案**：將結果另存為新的 .aedb。

### 補充說明

* `padstack.hole_diameter` 是以 meter 為單位，因此需轉為 mil 方便理解與操作。
* 字串格式如 `'2mil'` 是 pyedb 接受的輸入格式，可以直接用來設定屬性。
* `except` 區塊沒有指定錯誤類型，實務上建議補上明確錯誤類型以避免忽略其他錯誤。
* `padstack.material` 若原本不存在也可直接指定為 copper。

### 範例程式

```python
from pyedb import Edb

# 載入 EDB 檔案
edb = Edb(r"D:\\demo3\\Galileo_G87173_204.aedb", version='2024.1')

# 單位轉換函式
def mil_to_meter(mil: float) -> float:
    return mil * 0.0000254

def meter_to_mil(meter: float) -> float:
    return meter / 0.0000254

# 收集有孔徑的 padstack
data = {}
for padstack_name, padstack in edb.padstacks.padstacks.items():
    try:
        if padstack.hole_diameter > 0:
            data[padstack_name] = (padstack, meter_to_mil(padstack.hole_diameter))
            print(padstack_name, meter_to_mil(padstack.hole_diameter))
    except:
        print(padstack_name, 'useless')

# 修改 padstack 屬性
for padstack_name, (padstack, value) in data.items():
    padstack.hole_diameter = f'{value+2}mil'             # 增加 2mil
    padstack.hole_plating_thickness = '1mil'             # 鍍層厚度
    padstack.material = 'copper'                         # 材料

# 儲存新的 EDB
edb.save_edb_as('d:/demo3/test.aedb')
```

![](/assets/2025-11-26_22-15-24.png)