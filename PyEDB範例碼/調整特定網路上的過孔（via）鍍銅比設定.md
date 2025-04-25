調整特定網路上的過孔（via）鍍銅比設定
---

調整特定網路上的過孔（via）鍍銅比設定

### 目的與功能
這段程式碼的目的是修改一個特定電子設計資料庫（.aedb 檔案）中，屬於特定網路（net）`V1P5_S3` 的所有過孔 padstack，其鍍銅比（hole plating ratio）設為 73%。最後儲存為新的設計檔案。

### 流程架構
1. 使用 `pyedb` 套件讀取原始的 `.aedb` 設計檔案。
2. 透過迴圈尋找所有屬於 `V1P5_S3` 網路的過孔（via）。
3. 將這些過孔所使用的 padstack 名稱收集起來（避免重複）。
4. 對這些 padstack 設定新的鍍銅比數值（73%）。
5. 將修改後的設計另存為新的檔案。

### 補充說明
- `pyedb` 是一個用來操作 Ansys EDB 檔案的 Python 套件，可以讓使用者程式化地編輯電路設計資料。
- `edb.padstacks.padstack_instances` 是一個字典，裡面包含所有的 padstack 實例（例如過孔）。透過判斷 `via.net_name` 可以篩選出屬於特定電源或訊號網路的元件。
- `padstack_definition` 是過孔實際使用的 padstack 名稱，可用來進一步修改其參數。
- `hole_plating_ratio` 表示過孔內部鍍銅的比例，影響電氣與熱傳導特性。
- `set()` 的使用可以避免 padstack 名稱重複設定。
- `edb.save_as()` 可將修改後的設計儲存成新檔案，避免覆蓋原始資料。

這段程式適合用在需要批次調整設計規格、或做版本管理的自動化流程中。

```python
from pyedb import Edb

edb = Edb(r"D:\demo\Galileo_G87173_20454.aedb", edbversion='2024.1')

x = set()
for via_id, via in edb.padstacks.padstack_instances.items():
    if via.net_name == 'V1P5_S3':
        x.add(via.padstack_definition)

for name in x:
    edb.padstacks.padstacks[name].hole_plating_ratio = 73

edb.save_as('d:/demo/test.aedb')
```

![2025-04-25_15-19-43](/assets/2025-04-25_15-19-43.png)