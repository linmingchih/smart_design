利用檔案監測與設定檔修改自動化啟用 AEDT Beta 功能
---

在 Ansys Electronics Desktop (AEDT) 當中，某些 **Beta 功能** 需要使用者在介面中手動勾選才能啟用。然而，**AEDT 並沒有提供公開 API 來直接更改或控制 Beta 功能**。

若要達成自動化啟用，必須從檔案層級進行處理，找出 AEDT 實際修改的設定檔並進行編輯。如何找到這些檔案呢？本文將介紹一個有效的方法。

### 1. 工具選擇

* **Process Monitor (ProcMon)**：即時追蹤程式的檔案寫入行為，協助找出 AEDT 修改的檔案。

![](/assets/2025-09-22_13-19-07.png)

* **Git 或其他版本控管工具**：比對勾選前後的設定檔，快速定位差異。



### 2. 操作流程

1. **設定 ProcMon 過濾器**

   * Process Name 設定為 `ansysedt.exe` → Include
   * Operation 設定為 `WriteFile` → Include

2. **在 AEDT 勾選 Beta 功能**

   * 啟動 AEDT，手動勾選或取消 Beta Function。
   * 在 ProcMon 中觀察到相關的檔案寫入紀錄。

3. **確認設定檔路徑**

   * 依據 ProcMon 顯示的紀錄，可定位到特定 XML 檔案，例如：
     `config/AAPhWvmVEUgTEC_user.XML`

![](/assets/2025-09-22_13-15-25.png)

4. **比對檔案差異**

   * 使用 Git 或其他工具進行 diff。
   * 可觀察到 `<EnabledBetaOptions>` 節點被修改，例如 `NumItems` 變更，以及新增多個 `<VALUE>` 條目。


![](/assets/2025-09-22_13-11-12.png)

### 3. 自動化啟用方式

由於 AEDT **沒有提供 API**，唯一可行的方法是用 **Python 直接修改設定檔**：

* 編輯 XML 中的 `<EnabledBetaOptions>` 節點。
* 更新 `NumItems` 數值，並新增或刪除 `<VALUE>` 條目。
* 透過此方式即可批次啟用或停用特定 Beta 功能。

### 4. 優勢

* **可追溯性**：利用 ProcMon 精確定位修改檔案。
* **可版本化**：使用 Git 清楚記錄 Beta 功能的變動歷程。
* **可自動化**：不需依賴 UI 勾選，直接透過修改 XML 達成部署或批次設定。

