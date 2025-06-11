修改專案中所有port的名稱
---


這段程式碼的主要功能是將SIwave當前開啟的專案中，所有port名稱統一加上前綴詞 `new_`，達到批次重新命名的效果。

### 功能

* 取得目前開啟的專案（Project）。
* 列出所有屬於「ports」類別的元件名稱。
* 對每一個元件進行重新命名，加上新的前綴。
* 顯示每次重新命名的結果（可能是成功或失敗的訊息）。

### 流程架構

1. 透過 `oApp.GetActiveProject()` 取得目前使用中的專案物件 `oDoc`。
2. 呼叫 `oDoc.ScrGetComponentList('ports')` 取得所有「port」類型元件的名稱列表。
3. 使用 `for` 迴圈逐一處理這些名稱：

   * 每個名稱前加上 `new_` 作為新名稱。
   * 用 `oDoc.ScrEditCktElemName` 函式修改元件名稱，參數包含原始名稱、元件類型（這裡是 `'port'`）、以及新名稱。
   * 將函式執行結果列印出來以供確認。

### 補充說明

* `ScrGetComponentList('ports')` 是一個特殊 API，回傳的是屬於「ports」類別的元件名稱清單，應用在特定軟體的專案環境中。
* `ScrEditCktElemName` 則是一個用來更改元件名稱的函式，這裡需傳入舊名稱、類別（例如 port）、以及新名稱。
* 此段程式適合用於需要統一命名規則的工程中，例如電路圖、模擬模型、EDA 工具等。

### 範例程式

```python
# 取得目前開啟的專案物件
oDoc = oApp.GetActiveProject()

# 對所有 port 元件進行重新命名
for old_name in oDoc.ScrGetComponentList('ports'):
    new_name = 'new_' + old_name  # 加上前綴
    x = oDoc.ScrEditCktElemName(old_name, 'port', new_name)  # 嘗試重新命名
    print(x)  # 印出執行結果
```
### 輸出結果

需存檔關閉重啟專案之後，Components當中Port名稱才會更新。

![2025-06-11_13-25-08](/assets/2025-06-11_13-25-08.png)