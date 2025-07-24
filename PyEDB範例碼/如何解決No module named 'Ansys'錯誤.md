如何解決No module named 'Ansys'錯誤
---

在Spyder編輯PyEDB程式碼時，第一次可以順利執行，但第二次執行時會發生：

```
Error Message: No module named 'Ansys'
```
一個方法是重啟Console。但是頗為麻煩。

在第二次執行 `Edb(aedb_path, edbversion)` 時才發生，是因為 **Spyder 的 UMR（User Module Reloader）機制** 把 `Ansys.*` 這些 **COM 模組** 從 Python 的 module cache 中移除了，但這類 COM 元件 **無法被重新載入**，導致之後再次執行會失敗。

![2025-07-24_20-00-36](/assets/2025-07-24_20-00-36.png)

### ✅ 問題來源分析（技術層面）

* `pyedb` 會透過 `clr.AddReference()` 引入 .NET COM 元件，例如 `Ansys.Ansoft.Edb`。
* Spyder 的 UMR 會在你執行腳本後，自動把這些模組從記憶體卸載，以便「重新載入更新後的程式碼」。
* 但 COM 類模組一旦卸載，**無法被 Python 動態重新載入**，這就造成第二次執行時找不到 `Ansys` 命名空間。


### ✅ 解法：**永遠取消勾選 Enable UMR**

請依照以下步驟操作：

1. 在 Spyder 中進入：

   ```
   Tools → Preferences → Python interpreter
   ```
2. 取消勾選 `Enable UMR`
3. 點擊 `Apply`，然後 `OK`。
4. 重啟 Console

這樣每次執行程式時，Spyder **不會再卸載模組**，就能維持 COM 模組正常運作。

![2025-07-24_20-00-52](/assets/2025-07-24_20-00-52.png)


